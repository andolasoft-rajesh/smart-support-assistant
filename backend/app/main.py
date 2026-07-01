import uuid
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import Base, engine, get_db
from models import Conversation, Message

app = FastAPI(title="Smart Support Assistant")

Base.metadata.create_all(bind=engine)  # auto-create tables on startup


class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    conversation_id: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    # resolve or create conversation
    if req.conversation_id:
        conv = db.get(Conversation, uuid.UUID(req.conversation_id))
        if conv is None:
            conv = Conversation(id=uuid.UUID(req.conversation_id))
            db.add(conv)
    else:
        conv = Conversation()
        db.add(conv)

    db.flush()  # get conv.id without full commit

    # save user message
    user_msg = Message(conversation_id=conv.id, role="user", content=req.message)
    db.add(user_msg)

    # LLM call arrives Day 13 — echo for now
    reply_text = f"Echo: {req.message}"
    assistant_msg = Message(conversation_id=conv.id, role="assistant", content=reply_text)
    db.add(assistant_msg)

    db.commit()

    return ChatResponse(reply=reply_text, conversation_id=str(conv.id))