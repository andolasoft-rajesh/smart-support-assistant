from typing import List, Optional

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


class UploadResponse(BaseModel):
    filename: str
    chunks: int

class DocumentInfo(BaseModel):
    filename: str
    chunks: int

class SummaryRequest(BaseModel):
    document: str


class SummaryResponse(BaseModel):
    summary: str
    key_points: List[str]
