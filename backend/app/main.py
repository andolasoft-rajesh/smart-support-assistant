import os
import uuid
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .routes import documents
from . import document, chunk
from .retriever import retrieve_relevant_chunks
from app.llm import ask_llm
from app.models import Conversation, Message

from pydantic import BaseModel
from typing import Optional
from uuid import UUID

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

app = FastAPI(
    title="Smart Support Assistant",
    description="API for AI-powered customer support",
    version="1.0.0"
)
# ✅ RESPONSE MODEL
class ChatResponse(BaseModel):
    reply: str
    conversation_id: UUID

# pgvector ships as a PostgreSQL extension. It must exist before create_all()
# tries to build the Vector column on the chunks table.
with engine.begin() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    conn.execute(text(
        """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = 'chunks'
                  AND column_name = 'embedding'
            ) THEN
                ALTER TABLE public.chunks
                ALTER COLUMN embedding TYPE vector(768)
                USING embedding::vector;
                ADD COLUMN uploaded_at timestamp WITHOUT time zone DEFAULT now();
            END IF;
        END$$;
        """
    ))

    from app import models

    Base.metadata.create_all(bind=engine)

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(
    req: ChatRequest,
    db: Session = Depends(get_db)
):

    try:

        # First try normal conversation
        message = req.message.strip()

        # Get document context only for meaningful questions
        context_chunks = retrieve_relevant_chunks(
            message,
            db
        )

        if context_chunks:

            context = "\n\n".join(context_chunks)

            prompt = f"""
You are a helpful AI assistant.

Answer the user question.

If the uploaded document contains relevant information, use it.
If it does not contain the answer, answer normally.

Uploaded Document Context:
{context}

User Question:
{message}
"""

            reply = ask_llm(prompt)

        else:

            # Normal Gemini chat
            reply = ask_llm(message)

        # Create conversation if not provided
        conversation_id = req.conversation_id

        if not conversation_id:

            conversation = Conversation()

            db.add(conversation)
            db.commit()
            db.refresh(conversation)

            conversation_id = conversation.id

        # Save user message
        user_message = Message(
            conversation_id=conversation_id,
            role="user",
            content=message
        )

        db.add(user_message)

        # Save assistant reply
        assistant_message = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=reply
        )

        db.add(assistant_message)

        db.commit()

        return {
            "reply": reply,
            "conversation_id": conversation_id
        }

    except Exception as e:

        print("CHAT ERROR:", str(e))

        return {
            "error": str(e)
        }


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
