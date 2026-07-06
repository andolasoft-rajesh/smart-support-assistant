import uuid
from sqlalchemy.orm import Session
from .models import Conversation, Message

HISTORY_LIMIT = 20


def get_or_create_conversation(db: Session, conversation_id):
    """Return an existing conversation, or create a new one if None was given."""
    if conversation_id is None:
        conv = Conversation()
        db.add(conv)
        db.commit()
        db.refresh(conv)
        return conv

    try:
        conv_uuid = uuid.UUID(str(conversation_id))
    except (ValueError, AttributeError):
        raise ValueError("conversation_id is not a valid UUID")

    conv = db.query(Conversation).filter(Conversation.id == conv_uuid).first()
    if conv is None:
        raise LookupError("Conversation not found")
    return conv


def save_message(db: Session, conversation_id, role: str, content: str):
    """Save a single message row. Flushes so it's visible to queries in
    the same transaction, but does not commit — caller controls that."""
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
    )
    db.add(message)
    db.flush()
    return message


def load_history(db: Session, conversation_id) -> list[dict]:
    """Load the last HISTORY_LIMIT messages for a conversation, oldest first."""
    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())
        .limit(HISTORY_LIMIT)
        .all()
    )
    messages.reverse()  # we fetched newest-first for the LIMIT, now flip to chronological
    return [{"role": m.role, "content": m.content} for m in messages]