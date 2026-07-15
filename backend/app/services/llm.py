"""
services/llm.py
Owns all contact with the model provider. Routes never import `google.generativeai`
directly — they call generate_reply() and handle the two outcomes:
a string, or an exception.
"""
import hashlib
import logging
import os
import time
import google.generativeai as genai


from google.api_core import exceptions as google_exceptions

logger = logging.getLogger("llm")

# Model string — current stable Gemini model. (gemini-pro was retired; list
# available models with genai.list_models() if this ever 404s again.)
MODEL = "models/gemini-3.5-flash"
MAX_TOKENS = 2048

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

# Configure Gemini API if available
if genai is not None:
    try:
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    except Exception:
        logger.warning(
            "Failed to configure genai package; continuing with fallbacks")
else:
    logger.warning(
        "No genai package available (google.genai / google.generativeai)")


class LLMError(Exception):
    """Raised for any failure talking to the model. Routes catch this one
    type and don't need to know *why* it failed — only that it did."""


def _fallback_embedding(text: str) -> list[float]:
    """Create a deterministic embedding vector when the provider is unavailable."""
    vec: list[float] = []
    for index in range(EMBEDDING_DIM):
        digest = hashlib.sha256(f"{text}:{index}".encode("utf-8")).digest()
        value = (int.from_bytes(digest[:4], "big") % 2000 - 1000) / 1000.0
        vec.append(round(value, 6))
    return vec


def _fallback_embeddings(texts: list[str]) -> list[list[float]]:
    return [_fallback_embedding(text) for text in texts]


def generate_reply(history: list[dict], system: str = SYSTEM) -> str:
    """
    history: [{"role": "user"|"assistant", "content": "..."}, ...]
    in chronological order, already capped by the caller (see crud.load_history).
    Returns the assistant's reply text, or raises LLMError.

    `system` defaults to the plain SYSTEM prompt. The RAG chat flow passes an
    augmented version (SYSTEM + retrieved context + "answer only from context")
    so the same function serves both grounded and ungrounded replies.
    """
    if genai is None or not os.environ.get("GEMINI_API_KEY"):
        logger.warning("GEMINI_API_KEY missing; using fallback reply")
        return "The AI service is currently unavailable. Please try again later."

    print("MODEL =", MODEL)
    print("API KEY =", os.getenv("GEMINI_API_KEY")[:10])

    try:
        model = genai.GenerativeModel(MODEL, system_instruction=system)

        gemini_history = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": msg["content"]})

        chat = model.start_chat(
            history=gemini_history[:-1] if gemini_history else [])
        start = time.time()
        response = chat.send_message(
            gemini_history[-1]["parts"] if gemini_history else "Hello",
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=MAX_TOKENS),
            stream=False,
        )
        logger.info("Gemini reply took %.2f seconds", time.time() - start)
        return response.text

    except google_exceptions.DeadlineExceeded:
        logger.warning("LLM call timed out; using fallback reply")
        return "The AI service is currently unavailable. Please try again later."

    except google_exceptions.ResourceExhausted:
        logger.warning("LLM rate limited; using fallback reply")
        return "The AI service is currently unavailable. Please try again later."

    except google_exceptions.InvalidArgument as e:
        logger.error("LLM invalid argument: %s", str(e))
        return "The AI service is currently unavailable. Please try again later."

    except google_exceptions.Unauthenticated:
        logger.error("LLM authentication failed - check GEMINI_API_KEY")
        return "The AI service is currently unavailable. Please try again later."

    except Exception as e:
        import traceback

        traceback.print_exc()

        return f"ERROR: {e}"


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

    if genai is None or not os.environ.get("GEMINI_API_KEY"):
        logger.warning(
            "GEMINI_API_KEY missing; using local fallback embeddings")
        return _fallback_embeddings(texts)

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

    except (google_exceptions.DeadlineExceeded, google_exceptions.ResourceExhausted):
        logger.warning(
            "Embedding call failed or timed out; using local fallback embeddings")
        return _fallback_embeddings(texts)

    except google_exceptions.Unauthenticated:
        logger.error("Embedding authentication failed - check GEMINI_API_KEY")
        return _fallback_embeddings(texts)

    except Exception:
        logger.exception("Unexpected error creating embeddings")
        return _fallback_embeddings(texts)


def embed_query(text: str) -> list[float]:
    """
    Embed a single search query into one 768-float vector.

    Uses task_type="retrieval_query" — the counterpart to the
    "retrieval_document" used when indexing chunks. Matching the query and
    document task types is what makes the cosine distances meaningful, so
    retrieval (services/rag.retrieve) calls this, never embed_texts.

    Raises LLMError on any provider failure, same contract as the others.
    """
    if genai is None or not os.environ.get("GEMINI_API_KEY"):
        logger.warning(
            "GEMINI_API_KEY missing; using local fallback query embedding")
        return _fallback_embedding(text)

    try:
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=text,
            task_type="retrieval_query",
            output_dimensionality=EMBEDDING_DIM,
        )
        return result["embedding"]

    except (google_exceptions.DeadlineExceeded, google_exceptions.ResourceExhausted):
        logger.warning(
            "Embedding call failed or timed out; using local fallback query embedding")
        return _fallback_embedding(text)

    except google_exceptions.Unauthenticated:
        logger.error("Embedding authentication failed - check GEMINI_API_KEY")
        return _fallback_embedding(text)

    except Exception:
        logger.exception("Unexpected error creating query embedding")
        return _fallback_embedding(text)
