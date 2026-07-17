# Architecture — Smart Support Assistant

## Overview

Smart Support Assistant is a Retrieval-Augmented Generation (RAG) application that allows users to upload PDF or TXT documents, store them in a PostgreSQL database with vector embeddings, and interact with them through an AI-powered chat interface.

The application retrieves the most relevant document chunks using semantic search and sends them, along with the user's question, to Google Gemini to generate accurate, context-aware responses.

---

# System Architecture

```
                    USER (Browser)
                           │
                     HTTP / JSON
                           │
        ┌─────────────────────────────────┐
        │        Frontend (Next.js)        │
        │---------------------------------│
        │ • Chat Window                   │
        │ • Document Upload               │
        │ • Summary Feature               │
        │ • Message History               │
        └─────────────────────────────────┘
                           │
                     REST API Calls
                           │
        ┌─────────────────────────────────┐
        │      Backend (FastAPI)          │
        │---------------------------------│
        │ Routes                          │
        │ • /chat                         │
        │ • /documents                    │
        │ • /features                     │
        │                                 │
        │ Services                        │
        │ • llm.py                        │
        │ • rag.py                        │
        │ • chunker.py                    │
        │ • file_extractor.py             │
        └─────────────────────────────────┘
             │                     │
             │                     │
     SQLAlchemy ORM          Google Gemini API
             │                     │
             │                     │
      PostgreSQL + pgvector   Chat & Embeddings
```

---

# Application Workflow

## 1. Document Upload Pipeline

When a user uploads a PDF or TXT document:

1. The frontend sends the file to the FastAPI backend.
2. The backend extracts the document text.
3. The text is divided into smaller overlapping chunks.
4. Each chunk is converted into a vector embedding using Google Gemini.
5. Chunks and embeddings are stored inside PostgreSQL using pgvector.
6. If the same document already exists, previous chunks are removed before inserting the new ones.

**Workflow**

```
Upload File
      │
      ▼
Extract Text
      │
      ▼
Create Chunks
      │
      ▼
Generate Embeddings
      │
      ▼
Store in PostgreSQL
```

---

## 2. Chat Workflow (RAG)

Whenever the user asks a question:

1. The user's question is converted into an embedding.
2. PostgreSQL performs vector similarity search.
3. The most relevant document chunks are retrieved.
4. Retrieved context and conversation history are combined.
5. Google Gemini generates a grounded response.
6. The response is displayed in the chat interface.

**Workflow**

```
User Question
      │
      ▼
Create Query Embedding
      │
      ▼
Vector Search
      │
      ▼
Retrieve Relevant Chunks
      │
      ▼
Build Prompt
      │
      ▼
Google Gemini
      │
      ▼
AI Response
```

---

# Project Structure

## Backend

### app/main.py

Application entry point.

Responsibilities:

- Creates FastAPI application
- Configures CORS
- Registers API routes
- Starts the backend server

---

### app/database.py

Database configuration.

Responsibilities:

- Creates SQLAlchemy engine
- Creates database sessions
- Connects FastAPI with PostgreSQL

---

### app/models.py

Defines all database models.

Contains:

- Document
- Chunk
- Conversation
- Message

---

### app/schemas.py

Defines all request and response models using Pydantic.

Examples:

- ChatRequest
- ChatResponse
- UploadResponse
- SummaryResponse

---

### app/crud.py

Database access layer.

Responsibilities:

- Save conversations
- Save messages
- Store documents
- Retrieve document data
- Delete existing document chunks

---

## Routes

### routes/chat.py

Handles chat operations.

Endpoints:

- POST /chat

Responsibilities:

- Accept user messages
- Load conversation history
- Retrieve relevant document chunks
- Generate AI responses

---

### routes/documents.py

Handles document management.

Endpoints:

- POST /documents/upload
- GET /documents

Responsibilities:

- Upload PDF/TXT files
- Extract text
- Create chunks
- Store embeddings

---

### routes/feature.py

Handles additional AI features.

Responsibilities:

- Generate document summaries
- Return structured JSON responses

---

## Services

### services/llm.py

Communicates with Google Gemini.

Responsibilities:

- Generate AI responses
- Create embeddings
- Handle LLM exceptions

---

### services/rag.py

Implements Retrieval-Augmented Generation.

Responsibilities:

- Store embeddings
- Retrieve relevant chunks
- Build context for LLM

---

## Frontend

### components/ChatWindow.tsx

Main application interface.

Responsibilities:

- Chat interface
- Upload documents
- Display AI responses
- Summary feature

---

### components/MessageInput.tsx

Handles:

- User input
- File uploads
- Summary button

---

### components/MessageList.tsx

Displays conversation history.

---

# Database Design

The application stores information in four primary tables.

## Documents

Stores uploaded document information.

Fields:

- id
- filename

---

## Chunks

Stores document chunks and embeddings.

Fields:

- id
- document_id
- content
- embedding

---

## Conversations

Stores conversation sessions.

Fields:

- id
- created_at

---

## Messages

Stores all user and assistant messages.

Fields:

- id
- conversation_id
- role
- content

---

# Technologies Used

| Layer | Technology |
|---------|------------|
| Frontend | Next.js, React, TypeScript |
| Backend | FastAPI |
| Database | PostgreSQL |
| Vector Database | pgvector |
| ORM | SQLAlchemy |
| AI Model | Google Gemini |
| Embeddings | Gemini Embedding API |
| Containerization | Docker & Docker Compose |

---

# Key Features

- AI-powered document chat
- Retrieval-Augmented Generation (RAG)
- PDF and TXT document support
- Semantic vector search
- Conversation history
- Document summarization
- Duplicate document replacement
- Dockerized full-stack deployment

---

# Future Improvements

- Source citation for retrieved document chunks
- Streaming AI responses
- Authentication and user management
- Multi-document filtering
- Hybrid keyword + semantic search
- Faster vector indexing for large datasets
- Conversation export
- Cloud deployment (AWS/Azure/GCP)

---

# Overall Architecture Flow

```
                 User
                  │
                  ▼
        Next.js Frontend
                  │
                  ▼
          FastAPI Backend
                  │
      ┌───────────┴───────────┐
      ▼                       ▼
 PostgreSQL + pgvector    Google Gemini
      ▲                       │
      └───────────┬───────────┘
                  ▼
          AI Generated Reply
                  │
                  ▼
              Frontend UI
```