# backend/app/main.py
from dotenv import load_dotenv

# Load .env before importing anything that reads env vars at import time
# (services.llm calls genai.configure(api_key=...) on import).
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database import Base, engine
from app.routes.chat import router as chat_router
from app.routes.debug import router as debug_router
from app.routes.documents import router as documents_router
from app.routes.features import router as features_router

app = FastAPI(
    title="Smart Support Assistant",
    description="API for AI-powered customer support",
    version="1.0.0"
)

# pgvector ships as a PostgreSQL extension. It must exist before create_all()
# tries to build the Vector column on the chunks table.
with engine.begin() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))

Base.metadata.create_all(bind=engine)

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(chat_router)
app.include_router(documents_router)
app.include_router(features_router)
app.include_router(debug_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)