import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.database import Base
from app.services.llm import EMBEDDING_DIM

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    role = Column(String, nullable=False)   # "user" or "assistant"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")


class Chunk(Base):
    """One slice of an uploaded document, with its embedding.

    This is the product-side counterpart to Day 9's notebook: the same
    chunk/embed logic, but the rows live in PostgreSQL (via pgvector)
    instead of a JSON file, so we can do vector similarity search in SQL.
    """
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True)
    document = Column(String, nullable=False)          # source filename
    content = Column(Text, nullable=False)             # the chunk text
    embedding = Column(Vector(EMBEDDING_DIM))          # match the embedding model's dimension
    created_at = Column(DateTime, default=datetime.utcnow)