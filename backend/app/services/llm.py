"""
services/llm.py
Owns all contact with the model provider. Routes never import `google.generativeai`
directly — they call generate_reply() and handle the two outcomes:
a string, or an exception.
"""
import os
import logging

import google.generativeai as genai
from google.api_core import exceptions as google_exceptions

logger = logging.getLogger("llm")

# Model string — current stable Gemini model. (gemini-pro was retired; list
# available models with genai.list_models() if this ever 404s again.)
MODEL = "gemini-2.5-flash"
MAX_TOKENS = 500

# Embedding model. gemini-embedding-001 defaults to 3072-dim vectors but
# supports Matryoshka truncation via output_dimensionality — we ask for 768 so
# the vector matches the Vector(...) column in models.Chunk. This lives here as
# the single source of truth for both the embed calls and the DB schema.
# (text-embedding-004 was retired; list models with genai.list_models() if this
# ever 404s again.)
EMBEDDING_MODEL = "models/gemini-embedding-001"
EMBEDDING_DIM = 768

# System prompt lives here, server-side, so it's one place for the whole
# team — never sent from the client, never editable by the user.
SYSTEM = (
    "You are a helpful support assistant. Answer concisely. "
    "If you do not know something, say so plainly instead of guessing."
)

# Configure Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))


class LLMError(Exception):
    """Raised for any failure talking to the model. Routes catch this one
    type and don't need to know *why* it failed — only that it did."""


def generate_reply(
    history: list[dict], system: str = SYSTEM, max_tokens: int = MAX_TOKENS
) -> str:
    """
    history: [{"role": "user"|"assistant", "content": "..."}, ...]
    in chronological order, already capped by the caller (see crud.load_history).
    Returns the assistant's reply text, or raises LLMError.

    `system` defaults to the plain SYSTEM prompt. The RAG chat flow passes an
    augmented version (SYSTEM + retrieved context + "answer only from context")
    so the same function serves both grounded and ungrounded replies.

    `max_tokens` caps the output. It defaults to MAX_TOKENS (chat-sized), but
    callers that need a longer, complete response — e.g. the summarize feature,
    whose JSON must not be cut off mid-object — pass a larger budget. This
    matters extra for a thinking model like gemini-2.5-flash: internal thinking
    tokens also draw from this budget, so too small a cap yields truncated or
    empty output.
    """
    try:
        model = genai.GenerativeModel(MODEL, system_instruction=system)

        # Convert history format for Gemini (role must be "user" or "model")
        gemini_history = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": msg["content"]})

        chat = model.start_chat(history=gemini_history[:-1] if gemini_history else [])
        response = chat.send_message(
            gemini_history[-1]["parts"] if gemini_history else "Hello",
            generation_config=genai.types.GenerationConfig(max_output_tokens=max_tokens),
            stream=False,
        )

        return response.text

    except google_exceptions.DeadlineExceeded:
        logger.warning("LLM call timed out")
        raise LLMError("timeout")

    except google_exceptions.ResourceExhausted:
        logger.warning("LLM rate limited")
        raise LLMError("rate_limited")

    except google_exceptions.InvalidArgument as e:
        logger.error("LLM invalid argument: %s", str(e))
        raise LLMError("invalid_request")

    except google_exceptions.Unauthenticated:
        logger.error("LLM authentication failed - check GEMINI_API_KEY")
        raise LLMError("auth_error")

    except Exception:
        # last-resort catch: never let an unexpected exception leak a
        # traceback (or a raw error string) up to the user
        logger.exception("Unexpected error calling LLM")
        raise LLMError("unknown")


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Embed a batch of strings, returning one 768-float vector per input,
    in the same order. Used by the document pipeline (services/rag.py)
    to turn chunks into vectors before storing them.

    Raises LLMError on any provider failure — same contract as
    generate_reply(), so routes catch one exception type.
    """
    if not texts:
        return []

    try:
        # retrieval_document = the text is a corpus document being indexed
        # (queries at search time use task_type="retrieval_query").
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=texts,
            task_type="retrieval_document",
            output_dimensionality=EMBEDDING_DIM,
        )
        return result["embedding"]

    except google_exceptions.ResourceExhausted:
        logger.warning("Embedding rate limited")
        raise LLMError("rate_limited")

    except google_exceptions.Unauthenticated:
        logger.error("Embedding authentication failed - check GEMINI_API_KEY")
        raise LLMError("auth_error")

    except Exception:
        logger.exception("Unexpected error creating embeddings")
        raise LLMError("unknown")


def embed_query(text: str) -> list[float]:
    """
    Embed a single search query into one 768-float vector.

    Uses task_type="retrieval_query" — the counterpart to the
    "retrieval_document" used when indexing chunks. Matching the query and
    document task types is what makes the cosine distances meaningful, so
    retrieval (services/rag.retrieve) calls this, never embed_texts.

    Raises LLMError on any provider failure, same contract as the others.
    """
    try:
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=text,
            task_type="retrieval_query",
            output_dimensionality=EMBEDDING_DIM,
        )
        return result["embedding"]

    except google_exceptions.ResourceExhausted:
        logger.warning("Embedding rate limited")
        raise LLMError("rate_limited")

    except google_exceptions.Unauthenticated:
        logger.error("Embedding authentication failed - check GEMINI_API_KEY")
        raise LLMError("auth_error")

    except Exception:
        logger.exception("Unexpected error creating query embedding")
        raise LLMError("unknown")
