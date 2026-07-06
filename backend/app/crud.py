import uuid

from sqlalchemy.orm import Session

from app.models import Conversation, Message


def get_or_create_conversation(db: Session, conversation_id: str | None) -> Conversation:
    if not conversation_id:
        conversation = Conversation()
        db.add(conversation)
        db.flush()
        return conversation

    try:
        conversation_uuid = uuid.UUID(conversation_id)
    except ValueError as error:
        raise ValueError("Invalid conversation_id") from error

    conversation = db.query(Conversation).filter(Conversation.id == conversation_uuid).first()
    if not conversation:
        raise LookupError("Conversation not found")
    return conversation


def save_message(db: Session, conversation_id, role: str, content: str) -> Message:
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
    )
    db.add(message)
    db.flush()
    return message


def load_history(db: Session, conversation_id, limit: int = 20) -> list[dict]:
    rows = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
        .all()
    )

    rows.reverse()

    history = []
    for row in rows:
        role = "assistant" if row.role in {"ai", "assistant"} else "user"
        history.append({"role": role, "content": row.content})

    return history
