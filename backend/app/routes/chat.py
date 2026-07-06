"""
routes/chat.py
The route orchestrates: load state, call the service, save state, respond.
It never talks to the Anthropic SDK directly and never leaks internals
(tracebacks, provider error text) to the client.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas import ChatRequest, ChatResponse, ResponseMessage
from app.services.llm import generate_reply, LLMError

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    try:
        conv = crud.get_or_create_conversation(db, req.conversation_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid conversation_id")
    except LookupError:
        raise HTTPException(status_code=404, detail="Conversation not found")

    crud.save_message(db, conv.id, "user", req.message)
    history = crud.load_history(db, conv.id)

    try:
        reply = generate_reply(history)
    except LLMError:
        db.rollback()
        raise HTTPException(status_code=502, detail="Assistant unavailable, please retry")

    crud.save_message(db, conv.id, "ai", reply)
    db.commit()

    return ChatResponse(
        user=ResponseMessage(role="user", content=req.message),
        reply=reply,
        conversation_id=str(conv.id),
    )
