import json

from sqlalchemy.orm import Session

from .chunk import Chunk
from .gemini_service import create_embedding
from .similarity import cosine_similarity


def retrieve_relevant_chunks(
    question: str,
    db: Session,
    top_k: int = 3
):

    # Create embedding for the user's question
    question_embedding = create_embedding(question)

    # Get all chunks from PostgreSQL
    chunks = db.query(Chunk).all()

    scores = []

    # Compare question embedding with every chunk embedding
    for chunk in chunks:

        chunk_embedding = json.loads(chunk.embedding)

        similarity = cosine_similarity(
            question_embedding,
            chunk_embedding
        )

        scores.append(
            (
                similarity,
                chunk.content
            )
        )

    # Highest similarity first
    scores.sort(
        key=lambda x: x[0],
        reverse=True
    )

    # Return top matching chunks
    return [
        content
        for _, content in scores[:top_k]
    ]