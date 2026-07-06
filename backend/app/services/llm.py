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


def generate_reply(history: list[dict]) -> str:
    """
    history: [{"role": "user"|"assistant", "content": "..."}, ...]
    in chronological order, already capped by the caller (see crud.load_history).
    Returns the assistant's reply text, or raises LLMError.
    """
    try:
        model = genai.GenerativeModel(MODEL, system_instruction=SYSTEM)
        
        # Convert history format for Gemini (role must be "user" or "model")
        gemini_history = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": msg["content"]})
        
        chat = model.start_chat(history=gemini_history[:-1] if gemini_history else [])
        response = chat.send_message(
            gemini_history[-1]["parts"] if gemini_history else "Hello",
            generation_config=genai.types.GenerationConfig(max_output_tokens=MAX_TOKENS),
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
