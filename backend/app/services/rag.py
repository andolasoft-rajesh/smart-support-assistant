"""
services/rag.py
The document pipeline, lifted from Day 9's notebook into the product.

Same idea as the notebook — split text into overlapping chunks, embed each
chunk, keep them — but the chunks now land as rows in PostgreSQL (pgvector)
instead of a JSON file. Each stage is a plain function; the upload route just
chains them: extract text -> chunk_text -> store_chunks (embed + insert).
"""
import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Chunk, Document
from app.services.llm import embed_query, embed_texts

# Chunk sizing, in characters. Small overlap so a sentence split across a
# boundary still shows up whole in one of the two neighbouring chunks.
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def get_document_text(db: Session, filename: str) -> str:
    """
    Return the complete text of one uploaded document.
    """

    document = db.execute(
        select(Document).where(Document.filename == filename)
    ).scalar_one_or_none()

    if document is None:
        return ""

    chunks = db.execute(
        select(Chunk.content)
        .where(Chunk.document_id == document.id)
        .order_by(Chunk.chunk_index)
    ).scalars().all()

    return "\n".join(chunks)

def get_latest_document(db):
    """
    Return the most recently uploaded document, or None if none exist.
    """
    return db.execute(
        select(Document).order_by(Document.uploaded_at.desc())
    ).scalar_one_or_none()

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
        chunk = text[start: start + size].strip()
        if chunk:
            chunks.append(chunk)
    return chunks


def store_chunks(db: Session, document: str, chunks: list[str]) -> int:
    """
    Embed each chunk and insert it to the `documents` and `chunks` tables.
    Returns the number of chunks stored.

    The caller owns the transaction boundary: we add + flush here, the route
    commits once at the end so an embedding failure rolls the whole upload back.
    """
    if not chunks:
        return 0

    embeddings = embed_texts(chunks)

    existing = db.execute(
        select(Document).where(Document.filename == document)
    ).scalar_one_or_none()

    if existing:
        db.query(Chunk).filter(Chunk.document_id ==
                               existing.id).delete(synchronize_session=False)
        db.delete(existing)
        db.flush()

    doc = Document(filename=document)
    db.add(doc)
    db.flush()

    for chunk_index, (content, embedding) in enumerate(zip(chunks, embeddings), start=1):
        db.add(
            Chunk(
                document_id=doc.id,
                chunk_index=chunk_index,
                content=content,
                embedding=embedding,
            )
        )

    db.flush()
    return len(chunks)


def retrieve(db: Session, question: str, k: int = 4) -> list[str]:
    """
    Find the k chunks most similar to `question` and return their text.

    This is the retrieval half of RAG — the arrow that connects ingest
    (store_chunks) to chat. We embed the question with the SAME model used to
    embed the chunks, then let pgvector rank rows by cosine distance:

        ORDER BY embedding <=> query_embedding LIMIT k

    The `<=>` operator (Chunk.embedding.cosine_distance) is cosine distance —
    smaller means closer, so the first k rows are the best matches. Returns an
    empty list when nothing has been ingested yet.
    """
    try:
        q_emb = embed_query(question)
        latest_doc = db.execute(
            select(Document).order_by(Document.uploaded_at.desc())
        ).scalar_one_or_none()

        if latest_doc is None:
            return []

        rows = db.execute(
            select(Chunk.content)
            .where(Chunk.document_id == latest_doc.id)
            .order_by(Chunk.embedding.cosine_distance(q_emb))
            .limit(k)
        ).scalars().all()

        return list(rows)
    except Exception as exc:
        logging.warning(
            "RAG retrieval disabled; pgvector operator unavailable: %s",
            exc,
        )
        return []
