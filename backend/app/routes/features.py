import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import SummaryResponse
from app.llm import ask_llm
from app.rag import get_document_text
from app.prompts import SUMMARY_PROMPT


router = APIRouter(
    prefix="/features",
    tags=["Features"]
)


def parse_json_reply(raw: str):

    cleaned = raw.strip()

    # Remove markdown JSON fences if LLM adds them
    if cleaned.startswith("```"):
        cleaned = (
            cleaned
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

    try:
        return json.loads(cleaned)

    except json.JSONDecodeError:

        # Try extracting JSON object from text
        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start != -1 and end != -1:
            try:
                return json.loads(
                    cleaned[start:end + 1]
                )
            except:
                pass

    raise HTTPException(
        status_code=502,
        detail="Feature output was not valid JSON"
    )


@router.post("/summarize",response_model=SummaryResponse)
def summarize_document(
    document_id: str,
    db: Session = Depends(get_db)
):

    text = get_document_text(
        db,
        document_id
    )


    if not text.strip():

        raise HTTPException(
            status_code=404,
            detail="Document not found or empty"
        )


    prompt = SUMMARY_PROMPT + text


    try:

        raw_response = ask_llm(prompt)


    except Exception:

        raise HTTPException(
            status_code=502,
            detail="Assistant unavailable, please retry"
        )


    data = parse_json_reply(raw_response)


    return SummaryResponse(
        summary=data.get(
            "summary",
            ""
        ),
        key_points=data.get(
            "key_points",
            []
        )
    )