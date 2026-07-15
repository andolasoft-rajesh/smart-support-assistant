import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

_PROMPT_PATH = Path(__file__).parent / "prompts" / "system_prompt.txt"
# NEW: Configurable chunk count for RAG
RETRIEVER_K = int(os.environ.get("RETRIEVER_K", 3))

def get_system_prompt() -> str:
    """Load the system prompt from config file."""
    return _PROMPT_PATH.read_text(encoding="utf-8").strip()