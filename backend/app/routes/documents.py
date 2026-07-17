import io

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from pypdf import PdfReader
from sqlalchemy.exc import IntegrityError
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
    print("Uploading:", file.filename)

    raw = await file.read()
    print("File size:", len(raw))

    text = extract_text(file.filename, raw)
    print("Text length:", len(text))

    chunks = chunk_text(text)
    print("Chunks:", len(chunks))

    if not chunks:
        raise HTTPException(status_code=400, detail="No extractable text")

    count = store_chunks(db, file.filename, chunks)
    print("Stored:", count)

    db.commit()
    print("Commit successful")

    return UploadResponse(filename=file.filename, chunks=count)