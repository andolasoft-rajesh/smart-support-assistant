"""
services/rag.py
The document pipeline, lifted from Day 9's notebook into the product.

Same idea as the notebook — split text into overlapping chunks, embed each
chunk, keep them — but the chunks now land as rows in PostgreSQL (pgvector)
instead of a JSON file. Each stage is a plain function; the upload route just
chains them: extract text -> chunk_text -> store_chunks (embed + insert).
"""
from sqlalchemy.orm import Session

from app.models import Chunk
from app.services.llm import embed_texts

# Chunk sizing, in characters. Small overlap so a sentence split across a
# boundary still shows up whole in one of the two neighbouring chunks.
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Split text into overlapping windows of `size` characters, stepping forward
    by (size - overlap) each time. Returns the non-empty chunks in order.

    This is the Day 9 function; keeping the signature identical means the
    notebook and the product produce the same chunks for the same input.
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
    Returns the number of chunks stored.

    The caller owns the transaction boundary: we add + flush here, the route
    commits once at the end so an embedding failure rolls the whole upload back.
    """
    if not chunks:
        return 0

    embeddings = embed_texts(chunks)

    for content, embedding in zip(chunks, embeddings):
        db.add(Chunk(document=document, content=content, embedding=embedding))

    db.flush()
    return len(chunks)
