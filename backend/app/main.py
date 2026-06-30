from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI(title="Smart Support Assistant")
class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None
class ChatResponse(BaseModel):
    reply: str
    conversation_id: str@app.get("/health")
def health():
    return {"status": "ok"}
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    # LLM call arrives on Day 13 — return an echo for now
    return ChatResponse(reply=f"Echo: {req.message}", conversation_id=req.conversation_id or "new")