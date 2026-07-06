from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class ChatRequest(BaseModel):
    conversation_id:Optional[UUID]=None
    message: str

class ResponseMessage(BaseModel):
    role: str
    content: str


class ChatResponse(BaseModel):
    user: ResponseMessage
    reply: str
    conversation_id: str    