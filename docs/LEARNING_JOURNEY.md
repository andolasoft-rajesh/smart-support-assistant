# 📚 AI Internship Learning Journey

This document contains my complete day-by-day progress during my AI Developer Internship.

It covers my journey from software development fundamentals to building the Smart Support Assistant capstone project using FastAPI, React, LLMs, embeddings, and Retrieval-Augmented Generation (RAG).

--- 
## Day 1 — Tooling Setup & First AI-Generated Code

- Set up the development environment with Python, Node.js, Git, Docker, and VS Code.
- Configured essential VS Code extensions for development.
- Created the internship workspace structure.
- Used an AI assistant to generate a Python script that prints the current date and a motivational quote.
- Successfully executed the script using the VS Code terminal.

**Key Learnings:**
- Learned development environment setup, terminal usage, and AI-assisted code generation.
---

## Day 2 Update

- Created GitHub repository
- Learned Git branching
- Practiced commits and push workflow

---

## Day 3 Update

- Created CLI To-Do App using Python
- Learned file handling and basic command-line operations
- Practiced Git commit and push workflow

---

## Day 4 Update

- Built Notes App using React (Vite)
- Learned useState for managing notes
- Implemented add and delete functionality
- Practiced frontend state management

---

## Day 5 Update

- Built a FastAPI backend API and Dockerized it
- Created `/about` endpoint returning JSON response
- Learned FastAPI routing and basic API development
- Containerized application using Docker and understood port mapping

---

## Day 6 Update – AI Use Cases

- Researched 10 AI use cases in engineering domains
- Mapped each use case to AI capability (Text, Code, Vision, Extraction, Agent)
- Defined input and output for all use cases
- Selected **Resume Screening** as the first project to build
- Wrote justification for choosing Resume Screening

### Selected Project

- Resume Screening AI System
- Input: Resume + Job Description
- Output: Match score, matched skills, missing skills, recommendation

### Learning

- Learned how real-world problems map to AI solutions

---

## Day 7 – Prompt Library

Built a library of production-ready AI prompts for:

- Resume bullet generation
- Document summarization (JSON)
- Meeting action item extraction
- Error message rewriting
- Professional email generation

Each prompt includes:

- System Message
- User Template
- Example Output

The resume and document summary prompts also include **v1 vs v2** improvements.

---

## Day 8 Update

- Loaded Gemini API key from `.env`
- Added `.env.example` for configuration
- Read input document from a file path argument
- Used a summarization prompt from the prompt library
- Called the Gemini API to generate a summary
- Parsed and printed structured JSON fields
- Added error handling for:
  - Missing API key
  - Failed API requests

---

## Day 9 Update

- Read a document from `document.txt`
- Chunked the document into configurable chunks
- Generated embeddings using Gemini Embedding API
- Saved chunks and embeddings to `chunks_embeddings.json`
- Retrieved the top 3 most similar chunks using cosine similarity
- Generated concise answers using Gemini based on retrieved context

---

## Day 10 – Project Scaffold

- FastAPI setup completed
- `/health` endpoint implemented
- `/chat` endpoint (echo version)
- Basic API structure tested

---

## Day 11 – Backend + Database

- Integrated FastAPI with PostgreSQL
- Created SQLAlchemy models
- Implemented Conversation and Message tables
- Added UUID-based conversation tracking
- Stored chat history in database
- Implemented table relationships

### Testing

- Tested APIs using Swagger UI
- Verified database records using PostgreSQL
- Checked tables using pgAdmin

### Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic

---

# Smart Support Assistant Project

## Day 12 – Chat UI Connected to Backend

Completed the frontend chat interface and connected it with the FastAPI backend.

### Features

- User and assistant messages displayed with separate styling
- Enter key support for sending messages
- Loading indicator while waiting for responses
- Backend error handling with visible error messages
- TypeScript interfaces matching backend API
- Successful frontend-backend chat communication

### Technologies

- React
- TypeScript
- FastAPI

---

## Day 13 – End-to-End LLM Integration

Integrated the application with a Large Language Model.

### Features

- Connected frontend to Groq LLM
- Implemented conversation memory
- Loaded system prompt from configuration
- Limited conversation history to recent messages
- Added graceful error handling for failed LLM requests
- Displayed friendly error messages in UI

---

## Day 14 – Document Upload & Embeddings

Implemented the complete document processing pipeline.

### Features

- Upload support for PDF and TXT files
- Automatic text extraction
- Document chunking
- Gemini embedding generation
- Stored chunks and embeddings in PostgreSQL
- Listed uploaded documents
- Prevented duplicate chunks by replacing existing document data

---

## Day 15 – Retrieval Augmented Generation (RAG)

Completed the full RAG workflow.

### Features

- Semantic document retrieval
- Context-aware question answering
- Honest refusal for out-of-document questions
- Configurable retrieval chunk count using environment variables
- Grounded responses generated from uploaded documents

---

## Day 16 – Document Summarization Feature

Implemented document summarization as the individual feature.

### Features

- Document summarization endpoint
- Structured JSON response
- Prompt stored separately
- JSON parsing and validation
- Frontend Summarize button
- Displays summary and key points
- Successfully tested on multiple uploaded documents

---

## Day 17 – Evaluation

### Features

- Created 10 evaluation test cases
- Implemented automated evaluation harness (`eval/run_eval.py`)
- Added `eval/testcases.csv`
- Recorded evaluation results in `eval/EVAL.md`
- Improved prompt behavior against prompt injection
- Final evaluation score: **10/10**


## Day 18 – Dockerized Full Stack

Containerized the complete application.

### Features

- Docker Compose setup
- One-command startup

```bash
docker compose up --build
```

- Backend container
- Frontend container
- PostgreSQL with pgvector
- Environment variables managed using `.env.example`
- Successfully verified complete stack execution

---

## Day 19 – Final Project Preparation

Prepared the project for final submission.

### Completed

- Fixed major project bugs
- Updated README
- Added architecture documentation
- Prepared demo presentation
- Recorded demo video
- Created release version **v1.0**

---

## Day 20 – Final Submission

Completed internship submission.

### Deliverables

- Final GitHub repository
- README
- ARCHITECTURE.md
- EVAL.md
- Demo video
- Version tag **v1.0**
- Individual reflection document

---

# Technologies Used

### Backend

- FastAPI
- Python
- SQLAlchemy
- PostgreSQL
- pgvector

### Frontend

- React
- TypeScript
- Vite

### AI

- Groq LLM
- Google Gemini Embeddings
- Retrieval-Augmented Generation (RAG)

### DevOps

- Docker
- Docker Compose
- Git
- GitHub

---

# Project Features

- AI-powered document question answering
- PDF and TXT document upload
- Semantic search using embeddings
- RAG-based responses
- Conversation history
- Document history
- Document summarization
- Automated evaluation
- Dockerized deployment

---

# Project Structure

```
smart-support-assistant/
│
├── backend/
├── frontend/
├── eval/
├── docker-compose.yml
├── README.md
├── ARCHITECTURE.md
```

---

# How to Run

## Clone Repository

```bash
git clone <repository-url>
cd smart-support-assistant
```

## Configure Environment

Create a `.env` file using `.env.example`.

## Start Project

```bash
docker compose up --build
```

Frontend:

```
http://localhost:5173
```

Backend:

```
http://localhost:8000/docs
```

---

# Future Improvements

- Multi-document search
- User authentication
- Streaming responses
- Better document ranking
- Support for additional document formats

---

# Author

**Barsarani Sahoo**

Python Developer Intern
