# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from app.database import Base, engine, SessionLocal
from app import models

app = FastAPI(
    title="Smart Support Assistant",
    description="API for AI-powered customer support",
    version="1.0.0"
)

<<<<<<< HEAD
=======
# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
>>>>>>> ec2e479b457726b350315e8d86cb0d4ac1480924

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    conversation_id: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
<<<<<<< HEAD
    db = SessionLocal()

    if req.conversation_id is not None:
        conversation = db.query(models.Conversation).filter(
            models.Conversation.id == req.conversation_id
        ).first()
    else:
        conversation = None

    if conversation is None:
        conversation = models.Conversation()
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        message = models.Message(
            conversation_id=conversation.id,
            role="user",
            content=req.message
        )

    db.add(message)
    db.commit()

    assistant_message = models.Message(
    conversation_id=conversation.id,
    role="assistant",
    content=f"Echo: {req.message}"
)
    db.add(assistant_message)
    db.commit()

=======
    
>>>>>>> ec2e479b457726b350315e8d86cb0d4ac1480924
    return ChatResponse(
        reply=f"Echo: {req.message}",
        conversation_id=str(conversation.id)
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
