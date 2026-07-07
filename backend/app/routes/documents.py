"""
routes/documents.py
Receive an uploaded file, extract its text, and hand it to the pipeline.

The route only orchestrates: read bytes -> extract text -> chunk -> store.
Text extraction is format-specific (pdf vs plain text); everything after that
is format-agnostic and lives in services/rag.py.
"""
import io

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from pypdf import PdfReader
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UploadResponse
from app.services.llm import LLMError
from app.services.rag import chunk_text, store_chunks

router = APIRouter(prefix="/documents", tags=["documents"])


def extract_text(filename: str, raw: bytes) -> str:
    """Pull plain text out of the uploaded bytes based on the file type."""
    if filename.lower().endswith(".pdf"):
        reader = PdfReader(io.BytesIO(raw))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    # Anything else we treat as UTF-8 text; ignore undecodable bytes rather
    # than 500 on a stray character.
    return raw.decode("utf-8", errors="ignore")


@router.post("/upload", response_model=UploadResponse)
async def upload(file: UploadFile, db: Session = Depends(get_db)):
    raw = await file.read()
    text = extract_text(file.filename, raw)

    chunks = chunk_text(text)
    if not chunks:
        raise HTTPException(status_code=400, detail="No extractable text in file")

    try:
        count = store_chunks(db, file.filename, chunks)
    except LLMError:
        db.rollback()
        raise HTTPException(status_code=502, detail="Embedding failed, please retry")

    db.commit()
    return UploadResponse(filename=file.filename, chunks=count)
