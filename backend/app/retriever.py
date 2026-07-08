import ast

from sqlalchemy.orm import Session

from .document import Document
from .chunk import Chunk
from .gemini_service import create_embedding
from .similarity import cosine_similarity


def retrieve_relevant_chunks(
    question: str,
    db: Session,
    top_k: int = 3
):

    question_embedding = create_embedding(question)

    latest_document = (
        db.query(Document)
        .order_by(Document.uploaded_at.desc())
        .first()
    )

    if not latest_document:
        return []

    chunks = (
        db.query(Chunk)
        .filter(
            Chunk.document_id == latest_document.id
        )
        .all()
    )

    scored_chunks = []

    for chunk in chunks:

        if not chunk.embedding:
            continue

        chunk_embedding = ast.literal_eval(
            chunk.embedding
        )

        score = cosine_similarity(
            question_embedding,
            chunk_embedding
        )

        scored_chunks.append(
            (
                score,
                chunk.content
            )
        )

    scored_chunks.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [
        content
        for score, content in scored_chunks[:top_k]
        if score > 0.70
    ]