"""
routes/debug.py
Dev-only introspection for the Day 17 evaluation workflow.

When an eval case fails you need to know WHY. Two very different bugs look the
same from the outside:
  * retrieval problem — the answer's chunk was never retrieved (fix: chunk
    size / overlap / k / the embedding).
  * instruction problem — the right chunk WAS retrieved but the model ignored
    it (fix: tighten the prompt).

This endpoint returns exactly what retrieve() would feed the model for a
question, so the eval harness can print the retrieved chunks next to a failing
case and you can tell the two apart.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.rag import retrieve

router = APIRouter(prefix="/debug", tags=["debug"])


@router.get("/retrieve")
def debug_retrieve(q: str, k: int = 4, db: Session = Depends(get_db)):
    """Return the top-k chunks retrieve() would inject for question `q`."""
    chunks = retrieve(db, q, k=k)
    return {"question": q, "k": k, "count": len(chunks), "chunks": chunks}
