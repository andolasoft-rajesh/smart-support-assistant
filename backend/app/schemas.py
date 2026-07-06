from typing import Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ResponseMessage(BaseModel):
    role: str
    content: str


class ChatResponse(BaseModel):
    user: ResponseMessage
    reply: str
    conversation_id: str
