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

def retrieve_relevant_chunks(db: Session, query: str, top_k: int = 3) -> list[str]:
    """
    Embeds the user query and searches the database for the closest matching chunks.
    """
    if db.query(Chunk).first() is None:
        return []

    query_embedding = embed_texts([query])[0]

    results = (
        db.query(Chunk)
        .order_by(Chunk.embedding.cosine_distance(query_embedding))
        .limit(top_k)
        .all()
    )
    
    return [chunk.content for chunk in results]

# Add to the bottom of backend/app/services/rag.py

def get_document_text(db: Session, document_name: str) -> str:
    """Fetches all chunks for a document and stitches them back into full text."""
    chunks = db.query(Chunk).filter(Chunk.document == document_name).order_by(Chunk.id).all()
    if not chunks:
        return ""
    
    # Combine all chunk content into one massive string
    full_text = "\n".join([chunk.content for chunk in chunks])
    return full_text