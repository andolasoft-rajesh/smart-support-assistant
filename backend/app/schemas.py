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
    sources: list[str] = [] # Add this field to return source filenames    

class ConversationSummary(BaseModel):
    conversation_id: str
    preview: str
    created_at: str


class ConversationListResponse(BaseModel):
    conversations: list[ConversationSummary]    

class HistoryMessage(BaseModel):
    role: str
    content: str


class HistoryResponse(BaseModel):
    messages: list[HistoryMessage]

class UploadResponse(BaseModel):
    filename: str
    chunks: int

class DocumentInfo(BaseModel):
    document: str
    chunk_count: int


class DocumentListResponse(BaseModel):
    documents: list[DocumentInfo]    


class SummaryResponse(BaseModel):
    summary: str
    key_points: list[str]    