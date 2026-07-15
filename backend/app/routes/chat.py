"""
routes/chat.py
The route orchestrates: load state, call the service, save state, respond.
It never talks to the Anthropic SDK directly and never leaks internals
(tracebacks, provider error text) to the client.
"""
from os import system

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas import ChatRequest, ChatResponse, ResponseMessage
from app.services.llm import generate_reply, LLMError, SYSTEM
from app.services.rag import retrieve

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

    if any(word in req.message.lower() for word in [
        "document",
        "file",
        "pdf",
        "txt",
        "report",
        "chapter"
    ]):
        context = "\n\n".join(retrieve(db, req.message))
        print("=" * 80)
        print("RETRIEVED CONTEXT:")
        print(context)
        print("=" * 80)
    else:
        context = ""

    system = SYSTEM

    # RAG: pull the chunks most relevant to this question and staple them onto
    # the system prompt. The "answer ONLY from this context" instruction is what
    # separates grounded retrieval from a model that hallucinates confidently —
    # if the answer isn't in the uploaded documents, it must say it doesn't know.
    context = "\n---\n".join(retrieve(db, req.message))

    if context.strip():
        system = (
            SYSTEM
            + """
You are a helpful AI assistant.

Use the document context below to answer document-related questions.

If the user's question is a normal conversation
(example: hi, hello, thanks, can I upload another document?),
answer naturally.

If the user asks about the uploaded document and the answer
is not present in the context, say:
"I don't know based on the uploaded document."

Context:
"""
            + context
        )
    else:
        system = SYSTEM

    if context.strip():
        history[-1]["content"] = f"""
Document Context:

{context}

User Question:

{req.message}
"""

    try:
        reply = generate_reply(history, system=system)
    except LLMError:
        db.rollback()
        raise HTTPException(
            status_code=502,
            detail="Assistant unavailable, please retry",
        )

    crud.save_message(db, conv.id, "ai", reply)
    db.commit()

    return ChatResponse(
        user=ResponseMessage(role="user", content=req.message),
        reply=reply,
        conversation_id=str(conv.id),
    )
