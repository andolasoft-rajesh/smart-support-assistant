import json
import logging
import time
from pathlib import Path

from google import genai
from google.genai import errors as genai_errors
from google.genai import types

from ..config import GEMINI_API_KEY, get_system_prompt

logger = logging.getLogger("llm")

MODEL = "gemini-3.5-flash"
MAX_TOKENS = 1000
EMBEDDING_MODEL = "gemini-embedding-001"

_client = genai.Client(api_key=GEMINI_API_KEY)


class LLMError(Exception):
    """Raised for any failure talking to the model. Routes catch this one
    type and don't need to know *why* it failed — only that it did."""


def _is_retryable_rate_limit_error(exc: Exception) -> bool:
    """Return True for the provider errors that usually need backoff."""
    text = str(exc).lower()
    return any(
        token in text
        for token in (
            "429",
            "rate limit",
            "quota",
            "too many requests",
            "resource exhausted",
            "service temporarily unavailable",
            "503",
            "retry later",
        )
    )


def _run_with_backoff(fn, operation_name: str, max_attempts: int = 4, base_delay: float = 2.0, max_delay: float = 30.0):
    """Retry transient rate-limit/server failures with exponential backoff."""
    delay = base_delay
    last_error = None

    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except Exception as exc:  # pragma: no cover - exercised via tests and real provider errors
            last_error = exc
            if not _is_retryable_rate_limit_error(exc) or attempt >= max_attempts:
                raise

            logger.warning(
                "%s hit a rate-limit/server error; retrying in %.1fs (attempt %d/%d)",
                operation_name,
                delay,
                attempt,
                max_attempts,
            )
            time.sleep(delay)
            delay = min(delay * 2, max_delay)

    raise last_error


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Embed a list of texts, returning one vector per input text, in the same order.
    Raises LLMError on failure — same pattern as generate_reply.
    """
    if not texts:
        return []

    try:
        embeddings = []
        for index, text in enumerate(texts, 1):
            response = _run_with_backoff(
                lambda text=text: _client.models.embed_content(
                    model=EMBEDDING_MODEL,
                    contents=text,
                ),
                operation_name=f"embedding {index}/{len(texts)}",
            )
            embeddings.append(response.embeddings[0].values)
        return embeddings

    except genai_errors.ClientError as exc:
        logger.error("Embedding client error: %s", str(exc))
        raise LLMError("client_error") from exc
    except genai_errors.ServerError as exc:
        logger.warning("Embedding server error: %s", str(exc))
        raise LLMError("server_error") from exc
    except LLMError:
        raise
    except Exception:
        logger.exception("Unexpected error embedding texts")
        raise LLMError("unknown")


def generate_reply(history: list[dict], context: str = "", max_tokens: int = MAX_TOKENS) -> str:
    """
    history: [{"role": "user"|"ai", "content": "..."}, ...]
    context: A string of concatenated document chunks to ground the LLM's answer.
    """
    if not history:
        raise LLMError("empty_history")

    try:
        contents = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            contents.append(types.Content(role=role, parts=[types.Part(text=msg["content"])]))

        system_instruction = get_system_prompt()
        if context:
            system_instruction += (
                "\n\n[CRITICAL CONTEXT FROM UPLOADED DOCUMENTS]\nUse the following document text "
                "to accurately answer the user's question. If the answer cannot be found in the "
                "provided context, you must honestly say 'I cannot find the answer in the provided "
                "documents.' Do not hallucinate or make up an answer outside of this context.\n\n"
                f"Context:\n{context}"
            )

        response = _run_with_backoff(
            lambda: _client.models.generate_content(
                model=MODEL,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    max_output_tokens=max_tokens,
                ),
            ),
            operation_name="generate_reply",
        )

        if not response.text:
            raise LLMError("empty_response")

        return response.text

    except genai_errors.ClientError as exc:
        logger.error("LLM client error: %s", str(exc))
        raise LLMError("client_error") from exc
    except genai_errors.ServerError as exc:
        logger.warning("LLM server error: %s", str(exc))
        raise LLMError("server_error") from exc
    except LLMError:
        raise
    except Exception:
        logger.exception("Unexpected error calling LLM")
        raise LLMError("unknown")


def extract_action_items(context_text: str) -> list[dict]:
    """Forces the LLM to extract tasks and parses the resulting JSON."""
    prompt_path = Path(__file__).parent.parent / "prompts" / "action_items.txt"
    sys_prompt = prompt_path.read_text(encoding="utf-8").strip()

    try:
        response = _run_with_backoff(
            lambda: _client.models.generate_content(
                model=MODEL,
                contents=f"Document text:\n{context_text}",
                config=types.GenerateContentConfig(
                    system_instruction=sys_prompt,
                    temperature=0.1,
                ),
            ),
            operation_name="extract_action_items",
        )

        if not response.text:
            raise LLMError("empty_response")

        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:-3].strip()
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:-3].strip()

        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            logger.error("Malformed JSON received: %s", raw_text)
            raise LLMError("malformed_json")

    except genai_errors.ClientError as exc:
        logger.error("Action item client error: %s", str(exc))
        raise LLMError("client_error") from exc
    except genai_errors.ServerError as exc:
        logger.warning("Action item server error: %s", str(exc))
        raise LLMError("server_error") from exc
    except LLMError:
        raise
    except Exception as exc:
        logger.exception("Unexpected error extracting action items")
        raise LLMError("unknown") from exc