import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")


_PROMPT_PATH = Path(__file__).parent / "prompts" / "system_prompt.txt"

def get_system_prompt() -> str:
    """Load the system prompt from config file."""
    return _PROMPT_PATH.read_text(encoding="utf-8").strip()