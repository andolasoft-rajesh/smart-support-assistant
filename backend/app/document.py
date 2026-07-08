import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    filename = Column(
        String,
        unique=True,
        nullable=False
    )

    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    chunks = relationship(
        "Chunk",
        back_populates="document",
        cascade="all, delete"
    )