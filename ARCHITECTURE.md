# 🏗️ Smart Support Assistant - System Architecture

## Overview

Smart Support Assistant is a full-stack AI-powered document question-answering system that uses Retrieval-Augmented Generation (RAG) to provide context-aware responses. Users can upload PDF or TXT documents, which are processed, indexed, and stored for semantic retrieval. When a user asks a question, the system retrieves the most relevant document content and uses a Large Language Model (LLM) to generate an accurate, grounded response.

---

# High-Level Architecture

```text
                    User
                      │
                      ▼
          React + TypeScript Frontend
                      │
                 REST API Requests
                      │
                      ▼
              FastAPI Backend
                      │
      ┌───────────────┼────────────────┐
      │               │                │
      ▼               ▼                ▼
Document Upload   Chat Request   Conversation History
      │               │                │
      ▼               ▼                ▼
Text Extraction  Query Embedding   PostgreSQL Database
      │               │
      ▼               ▼
Document Chunking  Vector Search
      │               │
      ▼               ▼
Gemini Embeddings  Relevant Chunks
      └───────────────┬────────────────┘
                      ▼
              Groq LLM Generation
                      │
                      ▼
             AI Response to User
```

---

# Module Overview

## Frontend

The frontend is developed using **React**, **TypeScript**, and **Vite**. It provides an intuitive interface where users can upload documents, ask questions, view conversation history, and interact with the AI assistant. The frontend communicates with the backend through REST APIs and displays responses in a chat-style interface.

---

## Backend

The backend is built with **FastAPI** and serves as the core of the application. It handles document uploads, processes user requests, manages conversations, performs semantic retrieval, and coordinates communication between the database, embedding service, and LLM before returning responses to the frontend.

---

## Document Processing

After a document is uploaded, the backend extracts its text content from PDF or TXT files. The extracted text is divided into smaller chunks, making it suitable for embedding generation and efficient semantic retrieval during question answering.

---

## Embedding Generation

Each document chunk is converted into a vector embedding using the **Google Gemini Embedding API**. These embeddings capture the semantic meaning of the text and enable similarity-based retrieval instead of traditional keyword matching.

---

## Vector Database

The application uses **PostgreSQL** with **pgvector** to store document metadata, conversation history, and vector embeddings. During chat, the system performs similarity search on stored embeddings to retrieve the most relevant document chunks.

---

## Retrieval-Augmented Generation (RAG)

When a user submits a question, the backend converts the query into an embedding and performs semantic similarity search against stored document vectors. The retrieved context is then supplied to the LLM, ensuring that responses are based on the uploaded documents rather than relying only on the model's general knowledge.

---

## Large Language Model

The application uses the **Groq LLM** to generate natural language responses. The retrieved document context is included in the prompt, allowing the model to produce accurate, context-aware answers while reducing hallucinations.

---

## Docker Deployment

The entire application is containerized using **Docker Compose**, enabling the frontend, backend, and database services to run together with a single command. This ensures a consistent development environment and simplifies project setup.

---

# Technology Stack

| Layer | Technologies |
|--------|--------------|
| Frontend | React, TypeScript, Vite |
| Backend | FastAPI, Python |
| Database | PostgreSQL, pgvector |
| AI | Google Gemini Embeddings, Groq LLM |
| ORM | SQLAlchemy |
| DevOps | Docker, Docker Compose |
| Version Control | Git & GitHub |

---

# System Workflow

1. User uploads a PDF or TXT document.
2. The backend extracts and chunks the document text.
3. Gemini generates embeddings for each chunk.
4. Chunks and embeddings are stored in PostgreSQL.
5. The user submits a question through the chat interface.
6. The backend converts the question into an embedding.
7. The retriever finds the most relevant document chunks.
8. The retrieved context is passed to the Groq LLM.
9. The LLM generates a grounded response.
10. The response is displayed in the frontend chat interface.

---

# Future Improvements

- Multi-document retrieval
- User authentication and authorization
- Streaming AI responses
- Support for additional document formats
- Cloud deployment
- Improved retrieval ranking