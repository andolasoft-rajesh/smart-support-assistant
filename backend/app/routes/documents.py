import io
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pypdf import PdfReader
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UploadResponse, DocumentListResponse
from app.services.llm import LLMError
from app.services.rag import chunk_text, store_chunks
from .. import crud
from app.models import Chunk

router = APIRouter(prefix="/documents", tags=["documents"])

def extract_text(filename: str, raw: bytes) -> str:
    if filename.lower().endswith(".pdf"):
        reader = PdfReader(io.BytesIO(raw))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return raw.decode("utf-8", errors="ignore")

# NEW: Route handles an array of UploadFiles
@router.post("/upload_multiple", response_model=List[UploadResponse])
async def upload_multiple(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    responses = []
    for file in files:
        raw = await file.read()
        text = extract_text(file.filename, raw)

        chunks = chunk_text(text)
        if not chunks:
            continue # Skip empty files

        try:
            count = store_chunks(db, file.filename, chunks)
            responses.append(UploadResponse(filename=file.filename, chunks=count))
        except LLMError:
            db.rollback()
            raise HTTPException(status_code=502, detail=f"Embedding failed for {file.filename}")

    db.commit()
    return responses

@router.get("", response_model=DocumentListResponse)
def list_documents(db: Session = Depends(get_db)):
    docs = crud.list_documents(db)
    return DocumentListResponse(documents=docs)


@router.delete("/{document_name}")
def delete_document(document_name: str, db: Session = Depends(get_db)):
    """Deletes all chunks belonging to a specific document."""
    # Find all chunks with this filename and delete them
    deleted_count = db.query(Chunk).filter(Chunk.document == document_name).delete()
    db.commit()
    
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Document not found")
        
    return {"detail": f"Document '{document_name}' deleted successfully."}    