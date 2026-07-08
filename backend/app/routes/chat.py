from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud
from ..database import get_db
from ..schemas import ChatRequest, ChatResponse, ResponseMessage, ConversationListResponse, HistoryResponse
from ..services.llm import generate_reply, LLMError
# FIX: Import the retrieval utility explicitly
from ..services.rag import retrieve_relevant_chunks

router = APIRouter()

@router.get("/conversations", response_model=ConversationListResponse)
def list_conversations(db: Session = Depends(get_db)):
    conversations = crud.list_recent_conversations(db, limit=10)
    return ConversationListResponse(conversations=conversations)


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

    # Fetch relevant vector chunks from our uploaded documents
    try:
        relevant_chunks = retrieve_relevant_chunks(db, req.message, top_k=3)
        context_string = "\n\n---\n\n".join(relevant_chunks)
    except Exception as e:
        print(f"Retrieval error: {e}")
        context_string = ""

    try:
        # Pass both history and retrieved context safely into our updated function
        reply = generate_reply(history, context=context_string)
    except LLMError:
        db.rollback()
        raise HTTPException(status_code=502, detail="Assistant unavailable, please retry")

    crud.save_message(db, conv.id, "assistant", reply)
    db.commit()

    return ChatResponse(
        user=ResponseMessage(role="user", content=req.message),
        reply=reply,
        conversation_id=str(conv.id),
    )


@router.get("/chat/{conversation_id}/history", response_model=HistoryResponse)
def get_history(conversation_id: str, db: Session = Depends(get_db)):
    try:
        conv = crud.get_or_create_conversation(db, conversation_id)
    except (ValueError, LookupError):
        raise HTTPException(status_code=404, detail="Conversation not found")

    history = crud.load_history(db, conv.id)
    return HistoryResponse(messages=history)


@router.delete("/chat/{conversation_id}")
def delete_conversation_route(conversation_id: str, db: Session = Depends(get_db)):
    try:
        crud.delete_conversation(db, conversation_id)
        return {"detail": "Conversation deleted successfully"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid conversation_id")
    except LookupError:
        raise HTTPException(status_code=404, detail="Conversation not found")