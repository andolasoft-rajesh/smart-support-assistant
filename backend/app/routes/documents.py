import json

from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..document import Document
from ..chunk import Chunk
from ..gemini_service import create_embedding
from ..services.file_extractor import extract_text
from ..services.chunker import create_chunks

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # Extract text
    text = extract_text(file.file, file.filename)

    # Create chunks
    chunks = create_chunks(text)

    # Delete existing document with same filename
    existing_document = db.query(Document).filter(
        Document.filename == file.filename
    ).first()

    if existing_document:
        db.delete(existing_document)
        db.commit()

    # Create new document
    document = Document(filename=file.filename)

    db.add(document)
    db.commit()
    db.refresh(document)

    # Save chunks with embeddings
    for index, chunk_text in enumerate(chunks):

        embedding = create_embedding(chunk_text)

        chunk = Chunk(
            document_id=document.id,
            chunk_index=index,
            content=chunk_text,
            embedding=json.dumps(embedding)
        )

        db.add(chunk)

    db.commit()

    return {
        "message": "Document uploaded successfully",
        "filename": file.filename,
        "chunks_saved": len(chunks)
    }


@router.get("/")
def list_documents(db: Session = Depends(get_db)):

    documents = db.query(Document).all()

    result = []

    for doc in documents:

        chunk_count = db.query(Chunk).filter(
            Chunk.document_id == doc.id
        ).count()

        result.append({
            "id": str(doc.id),
            "filename": doc.filename,
            "uploaded_at": doc.uploaded_at,
            "chunk_count": chunk_count
        })

    return result