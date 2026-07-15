"""
routes/features.py
AI features built on top of RAG (Day 16).

Every feature is the same recipe with a different prompt/schema:
    route -> fetch document text -> prompt demanding JSON -> parse -> return.

Structured output in production: we demand JSON, strip any markdown fences the
model wraps around it, parse with try/except, and return 502 on parse failure
rather than leaking a half-formed string to the client. This file ships the
summarization feature; FAQ and task extraction are the same shape with a
different prompt and response_model.
"""
import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import SummaryRequest, SummaryResponse
from app.services.llm import LLMError, generate_reply
from app.services.rag import get_document_text

router = APIRouter(prefix="/features", tags=["features"])


def parse_json_reply(raw: str) -> dict:
    """
    Parse the model's reply as JSON, tolerating the ```json ... ``` fences it
    often adds despite being told to return only JSON. Raises 502 on anything
    that isn't valid JSON — the caller never sees a malformed body.
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

    # Fallback: the model sometimes wraps the JSON in a sentence ("Here's the
    # summary: {...}. Hope that helps!"). Carve out the outermost object and
    # try once more before giving up.
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start != -1 and end > start:
        try:
            return json.loads(cleaned[start: end + 1])
        except json.JSONDecodeError:
            pass

    raise HTTPException(
        status_code=502, detail="Feature output was not valid JSON")


@router.post("/summary", response_model=SummaryResponse)
def summarize(req: SummaryRequest, db: Session = Depends(get_db)):
    text = get_document_text(db, req.document)
    if not text.strip():
        raise HTTPException(
            status_code=404, detail="Document not found or empty")

    prompt = (
        "Summarize this document. Respond with ONLY JSON: "
        '{"summary": "...", "key_points": ["..."]}\n\n' + text
    )

    try:
        raw = generate_reply(
            [{"role": "user", "content": prompt}],
        )
        print("RAW RESPONSE:")
        print(raw)

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=502, detail=str(e))

    data = parse_json_reply(raw)

    print("RAW RESPONSE:")
    print(raw)

    data = parse_json_reply(raw)
    return SummaryResponse(
        summary=data.get("summary", ""),
        key_points=data.get("key_points", []),
    )
