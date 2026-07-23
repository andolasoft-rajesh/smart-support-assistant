"""
routes/chat.py

The route orchestrates: load state, call the service, save state, respond.
It never talks to the LLM SDK directly and never leaks provider errors
to the client.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.models import Conversation, Message
from app.schemas import ChatRequest, ChatResponse, ResponseMessage
from app.services.llm import SYSTEM, LLMError, generate_reply
from app.services.rag import retrieve

router = APIRouter()


@router.get("/conversations")
def list_conversations(db: Session = Depends(get_db)):
    conversations = db.execute(
        select(Conversation).order_by(desc(Conversation.created_at))
    ).scalars().all()

    result = []

    for conv in conversations:
        first_message = db.execute(
            select(Message.content)
            .where(Message.conversation_id == conv.id)
            .order_by(Message.created_at)
            .limit(1)
        ).scalar_one_or_none()

        result.append(
            {
                "id": str(conv.id),
                "title": first_message[:40] if first_message else "New Chat",
                "created_at": conv.created_at,
            }
        )

    return result


@router.get("/chat/{conversation_id}")
def get_chat_history(
    conversation_id: str,
    db: Session = Depends(get_db),
):
    messages = db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    ).scalars().all()

    return [
        {
            "role": msg.role,
            "content": msg.content,
        }
        for msg in messages
    ]


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    try:
        conv = crud.get_or_create_conversation(db, req.conversation_id)

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid conversation_id",
        )

    except LookupError:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    crud.save_message(db, conv.id, "user", req.message)

    history = crud.load_history(db, conv.id)

    context = "\n---\n".join(retrieve(db, req.message))

    system = SYSTEM

    if context.strip():
        system += f"""

You are a helpful AI assistant.

Use the document context below to answer document-related questions.

If the answer is not present in the document, reply:

"I don't know based on the uploaded document."

Context:

{context}
"""

        history[-1]["content"] = f"""
Document Context:

{context}

User Question:

{req.message}
"""

    try:
        reply = generate_reply(
            history,
            system=system,
        )

    except LLMError:
        db.rollback()

        raise HTTPException(
            status_code=502,
            detail="Assistant unavailable, please retry",
        )

    crud.save_message(
        db,
        conv.id,
        "assistant",
        reply,
    )

    db.commit()

    return ChatResponse(
        user=ResponseMessage(
            role="user",
            content=req.message,
        ),
        reply=reply,
        conversation_id=str(conv.id),
    )
