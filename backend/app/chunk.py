import uuid

from sqlalchemy import Column, Text, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .database import Base


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    document_id = Column(
        UUID(as_uuid=True),
        ForeignKey("documents.id"),
        nullable=False
    )

    chunk_index = Column(
        Integer,
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    embedding = Column(
        Text,
        nullable=False
    )

    document = relationship(
        "Document",
        back_populates="chunks"
    )