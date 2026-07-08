import uuid
from .database import Base, engine
from .routes import documents
from . import document
from . import chunk
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.llm import ask_llm
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from app.database import Base, engine, get_db
from app.models import Conversation, Message

app = FastAPI(title="Smart Support Assistant")
Base.metadata.create_all(bind=engine)
app.include_router(documents.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):

    try:
        reply = ask_llm(req.message)
        return {"reply": reply}

    except Exception as e:
        print("ERROR OCCURRED:", str(e))
        return {"error": str(e)}
@app.get("/conversation/{conversation_id}")
def get_conversation(conversation_id: UUID, db: Session = Depends(get_db)):

    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).all()

    return {
        "conversation_id": str(conversation_id),
        "messages": [
            {
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at
            }
            for m in messages
        ]
    }