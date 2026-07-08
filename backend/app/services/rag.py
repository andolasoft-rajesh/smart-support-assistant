from sqlalchemy.orm import Session

from app.models import Chunk
from app.services.llm import embed_texts

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Split text into overlapping windows of `size` characters, stepping forward
    by (size - overlap) each time. Returns the non-empty chunks in order.
    """
    text = text.strip()
    if not text:
        return []

    step = max(1, size - overlap)
    chunks = []
    for start in range(0, len(text), step):
        chunk = text[start : start + size].strip()
        if chunk:
            chunks.append(chunk)
    return chunks


def store_chunks(db: Session, document: str, chunks: list[str]) -> int:
    """
    Embed each chunk and insert it as a row tied to `document`.
    If chunks already exist for this document name, delete them first
    so a re-upload replaces rather than duplicates.
    """
    if not chunks:
        return 0

    # Delete existing chunks for this document (delete-then-insert)
    db.query(Chunk).filter(Chunk.document == document).delete()

    embeddings = embed_texts(chunks)

    for content, embedding in zip(chunks, embeddings):
        db.add(Chunk(document=document, content=content, embedding=embedding))

    db.flush()
    return len(chunks)