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

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def get_document_text(db: Session, filename: str) -> str:
    """Return the complete text of one uploaded document."""

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


def get_latest_document(db: Session):
    """Return the most recently uploaded document."""

    return db.execute(
        select(Document).order_by(Document.uploaded_at.desc())
    ).scalar_one_or_none()


def chunk_text(
    text: str,
    size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[str]:
    """Split text into overlapping chunks."""

    text = text.strip()

    if not text:
        return []

    step = max(1, size - overlap)

    chunks = []

    for start in range(0, len(text), step):
        chunk = text[start:start + size].strip()

        if chunk:
            chunks.append(chunk)

    return chunks


def store_chunks(db: Session, document: str, chunks: list[str]) -> int:
    """
    Embed each chunk and store it in PostgreSQL.
    """

    if not chunks:
        return 0

    embeddings = embed_texts(chunks)

    existing = db.execute(
        select(Document).where(Document.filename == document)
    ).scalar_one_or_none()

    # If the document already exists, delete its chunks first
    if existing:
        db.query(Chunk).filter(
            Chunk.document_id == existing.id
        ).delete()

        db.delete(existing)
        db.flush()

    # Create a new document
    doc = Document(filename=document)
    db.add(doc)
    db.flush()

    # Store all chunks
    for chunk_index, (content, embedding) in enumerate(
        zip(chunks, embeddings),
        start=1,
    ):
        db.add(
            Chunk(
                document_id=doc.id,
                chunk_index=chunk_index,
                content=content,
                embedding=embedding,
            )
        )

    db.commit()

    return len(chunks)


def retrieve(db: Session, question: str, k: int = 4) -> list[str]:
    """
    Retrieve the most relevant chunks for the question.
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
