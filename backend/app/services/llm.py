import logging

from google import genai
from google.genai import types
from google.genai import errors as genai_errors

from ..config import GEMINI_API_KEY, get_system_prompt

logger = logging.getLogger("llm")

MODEL = "gemini-2.5-flash"
MAX_TOKENS = 500

_client = genai.Client(api_key=GEMINI_API_KEY)


class LLMError(Exception):
    """Raised for any failure talking to the model. Routes catch this one
    type and don't need to know *why* it failed — only that it did."""

EMBEDDING_MODEL = "gemini-embedding-001"


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Embed a list of texts, returning one vector per input text, in the same order.
    Raises LLMError on failure — same pattern as generate_reply.
    """
    if not texts:
        return []

    try:
        embeddings = []
        for text in texts:
            response = _client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=text,
            )
            embeddings.append(response.embeddings[0].values)
        return embeddings

    except genai_errors.ClientError as e:
        logger.error("Embedding client error: %s", str(e))
        raise LLMError("client_error")

    except genai_errors.ServerError as e:
        logger.warning("Embedding server error: %s", str(e))
        raise LLMError("server_error")

    except Exception:
        logger.exception("Unexpected error embedding texts")
        raise LLMError("unknown")    


def generate_reply(history: list[dict]) -> str:
    """
    history: [{"role": "user"|"ai", "content": "..."}, ...]
    in chronological order, already capped by the caller (see crud.load_history).
    Returns the assistant's reply text, or raises LLMError.
    """
    
    if not history:
        
        raise LLMError("empty_history")

    try:
        # Convert our stored roles to what Gemini expects: "user" or "model"
        
        contents = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            contents.append(
                types.Content(role=role, parts=[types.Part(text=msg["content"])])
            )
        

        
        response = _client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=get_system_prompt(),
                max_output_tokens=MAX_TOKENS,
            ),
        )
        

        if not response.text:
            
            raise LLMError("empty_response")

        return response.text

    except genai_errors.ClientError as e:
        # Covers bad/missing API key (401/403) and bad requests (400)
        
        logger.error("LLM client error: %s", str(e))
        raise LLMError("client_error")

    except genai_errors.ServerError as e:
        # Covers Gemini-side outages, timeouts, rate limits (5xx)
        
        logger.warning("LLM server error: %s", str(e))
        raise LLMError("server_error")

    except LLMError:
        raise  # don't let our own deliberate raise get caught by the next line

    except Exception as exc:
        # last-resort catch: never let an unexpected exception leak a
        # traceback (or raw provider error text) up to the user
        
        import traceback
        traceback.print_exc()
        logger.exception("Unexpected error calling LLM")
        raise LLMError("unknown")