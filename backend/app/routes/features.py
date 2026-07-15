# FILE: backend/app/routes/features.py

import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import SummaryResponse
from app.services.llm import LLMError, generate_reply
from app.services.rag import get_document_text

router = APIRouter(prefix="/features", tags=["features"])

def parse_json_reply(raw: str) -> dict:
    """
    Parse the model's reply as JSON, tolerating the ```json ... ``` fences it
    often adds despite being told to return only JSON.
    """
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = (
            cleaned.removeprefix("```json")
            .removeprefix("```")
            .removesuffix("```")
            .strip()
        )
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start != -1 and end > start:
        try:
            return json.loads(cleaned[start : end + 1])
        except json.JSONDecodeError:
            pass

    raise HTTPException(status_code=502, detail="Feature output was not valid JSON")


@router.post("/summarize", response_model=SummaryResponse)
def summarize(document: str, db: Session = Depends(get_db)):
    text = get_document_text(db, document)
    if not text.strip():
        raise HTTPException(status_code=404, detail="Document not found or empty")

    prompt = (
        "Summarize this document. Respond with ONLY JSON: "
        '{"summary": "...", "key_points": ["..."]}\n\n' + text
    )

    try:
        raw = generate_reply([{"role": "user", "content": prompt}], context="",max_tokens=2048)
    except LLMError:
        raise HTTPException(status_code=502, detail="Assistant unavailable, please retry")

    data = parse_json_reply(raw)
    return SummaryResponse(
        summary=data.get("summary", ""),
        key_points=data.get("key_points", []),
    )