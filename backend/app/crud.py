import uuid
from sqlalchemy.orm import Session
from .models import Conversation, Message, Chunk
from sqlalchemy import func

HISTORY_LIMIT = 20

def list_documents(db: Session):
    """Return each distinct document filename with its chunk count."""
    results = (
        db.query(Chunk.document, func.count(Chunk.id).label("chunk_count"))
        .group_by(Chunk.document)
        .order_by(Chunk.document)
        .all()
    )
    return [{"document": doc, "chunk_count": count} for doc, count in results]

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

def list_recent_conversations(db: Session, limit: int = 10):
    """
    Return the most recent conversations, each with the first user message
    as a short preview. Newest conversation first. Skips empty conversations.
    """
    # Fetch a larger batch initially to account for any empty ones we might skip
    conversations = (
        db.query(Conversation)
        .order_by(Conversation.created_at.desc())
        .limit(limit * 3) 
        .all()
    )

    summaries = []
    for conv in conversations:
        first_message = (
            db.query(Message)
            .filter(Message.conversation_id == conv.id, Message.role == "user")
            .order_by(Message.created_at.asc())
            .first()
        )
        
        # The Magic Fix: If there is no message yet, completely skip it
        if not first_message:
            continue
            
        summaries.append({
            "conversation_id": str(conv.id),
            "preview": first_message.content[:60],
            "created_at": conv.created_at.isoformat(),
        })

        # Stop once we have gathered the exact amount requested (10)
        if len(summaries) == limit:
            break

    return summaries

def delete_conversation(db: Session, conversation_id: str):
    """Delete a conversation and all of its associated messages."""
    try:
        conv_uuid = uuid.UUID(str(conversation_id))
    except (ValueError, AttributeError):
        raise ValueError("conversation_id is not a valid UUID")

    # Delete child messages first to avoid foreign key constraint errors
    db.query(Message).filter(Message.conversation_id == conv_uuid).delete()
    
    # Delete the parent conversation
    result = db.query(Conversation).filter(Conversation.id == conv_uuid).delete()
    db.commit()
    
    if result == 0:
        raise LookupError("Conversation not found")