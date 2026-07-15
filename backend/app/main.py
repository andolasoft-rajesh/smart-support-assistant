from fastapi import FastAPI,Depends
from .schemas import ChatRequest
from .database import Base, engine,get_db
from . import models
from sqlalchemy.orm import Session
from .models import Conversation
from .routes.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
from .routes.documents import router as documents_router
from .routes.features import router as features_router

import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(chat_router)
app.include_router(documents_router)
app.include_router(features_router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "Welcome!"
    }

@app.get("/developer")
def developer():
    return {
        "developer": "Ankur"
    }

@app.get("/users/{user_id}")
def avout(user_id:int):
    return{
        "user_id":user_id
    }

@app.get("/search")
def developer(category:str, page:int):
    return {
        "category":category,
        "Page":page
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
