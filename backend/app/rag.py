import os

from sqlalchemy.orm import Session

from app.models import Chunk
from app.gemini_service import create_embedding

TOP_K = int(os.getenv("TOP_K", 5))


def retrieve_relevant_chunks(
    query: str,
    db: Session,
    document_id=None,
    limit: int = TOP_K
):

    query_embedding = create_embedding(query)

    distance = Chunk.embedding.cosine_distance(
        query_embedding
    ).label("distance")

    query_result = db.query(
        Chunk,
        distance
    )

    if document_id:
        query_result = query_result.filter(
            Chunk.document_id == document_id
        )

    print("TOP_K:", limit)

    results = (
        query_result
        .order_by(distance)
        .limit(limit)
        .all()
    )

    print("DOCUMENT ID:", document_id)
    print("RESULT COUNT:", len(results))

    chunks = []

    for chunk, distance_value in results:

        similarity = 1 - distance_value

        print("----------------")
        print("Distance:", distance_value)
        print("Similarity:", similarity)
        print("Chunk:", chunk.content[:200])

        chunks.append(chunk.content)

    print("FINAL CHUNKS SENT:", len(chunks))

    return chunks


# -----------------------------
# Used by the Summarize feature
# -----------------------------
def get_document_text(
    db: Session,
    document_id,
):

    chunks = (
        db.query(Chunk)
        .filter(Chunk.document_id == document_id)
        .order_by(Chunk.chunk_index)
        .all()
    )

    if not chunks:
        return ""

    return "\n\n".join(chunk.content for chunk in chunks)