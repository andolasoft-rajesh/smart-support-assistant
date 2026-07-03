from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import ChatRequest
from ..models import Conversation, Message

router = APIRouter()


@router.post("/chat")
def chat(
    req: ChatRequest,
    db: Session = Depends(get_db)
):
    if req.conversation_id is None:

        conversation = Conversation()

        db.add(conversation)

    else:

        conversation = (
            db.query(Conversation)
            .filter(Conversation.id == req.conversation_id)
            .first()
        )

        if conversation is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found"
            )
        

    message = Message(
    conversation=conversation,
    role="user",
    content=req.message
)   
    db.add(message)
    db.commit()
    db.refresh(conversation)
    

    return {
    "conversation_id": str(conversation.id),
    "message": req.message
}