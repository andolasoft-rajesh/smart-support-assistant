import uuid
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from app.database import Base, engine, get_db
from app.models import Conversation, Message

app = FastAPI(title="Smart Support Assistant")

# create tables
Base.metadata.create_all(bind=engine)


# ✅ REQUEST MODEL (UUID-based)
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None


# ✅ RESPONSE MODEL
class ChatResponse(BaseModel):
    reply: str
    conversation_id: UUID


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)):

    # 1. find existing conversation if UUID provided
    conv = None

    if req.conversation_id:
        conv = db.get(Conversation, req.conversation_id)

    # 2. if not found → create new conversation
    if not conv:
        conv = Conversation()
        db.add(conv)
        db.flush()  # get UUID before commit

    # 3. save user message
    msg = Message(
        conversation_id=conv.id,
        role="user",
        content=req.message
    )

    db.add(msg)
    db.commit()

    # 4. response
    return ChatResponse(
        reply=f"Echo: {req.message}",
        conversation_id=conv.id
    )
@app.get("/conversation/{conversation_id}")
def get_conversation(conversation_id: str, db: Session = Depends(get_db)):

    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).all()

    return {
        "conversation_id": conversation_id,
        "messages": [
            {
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at
            }
            for m in messages
        ]
    }