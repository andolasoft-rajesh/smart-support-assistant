# 🚀 Intern Learning Journey

Hi, I'm **Ankur Bandopadhyay**.

This repository documents my progress throughout a **4-week AI Internship Program**, where I'm building practical skills in Python, Git/GitHub, React, FastAPI, Docker, Prompt Engineering, and AI application development. It contains all assignments, projects, and key learnings from the internship.

---

# 📚 Internship Focus

### Week 1
- Development Environment Setup
- Git & GitHub
- Python Fundamentals
- React
- FastAPI
- Docker

### Week 2
- Prompt Engineering
- LLM API Integration
- Embeddings & RAG
- Project Setup & Team Collaboration

### Week 3 & 4
- Capstone Project Development
- Production-Grade RAG Implementations
- Automated Evaluation Harnesses
- Multi-Container Orchestration (Docker Compose)

---

# 🎯 Objectives

- Strengthen software development fundamentals
- Learn AI development workflows
- Build full-stack applications
- Work with LLM APIs and RAG
- Practice collaborative development using Git

---

# 📅 Learning Log

## Day 1 — Tooling Setup & First AI-Generated Code
- **Task:** Set up the development environment and generate a Python script using AI.
- **Deliverables:** Configured the required tools and ran the AI-generated script.
- **Key Learnings:** Environment setup, terminal usage, and Python basics.

---

## Day 2 — GitHub Repository
- **Task:** Create and organize the internship repository.
- **Deliverables:** Repository with README, `.gitignore`, commits, and a merged pull request.
- **Key Learnings:** Git, branching, pull requests, and repository management.

---

## Day 3 — CLI To-Do Application
- **Task:** Build a command-line To-Do application.
- **Deliverables:** CLI app with persistent task storage using JSON.
- **Key Learnings:** Functions, file handling, and error handling.

---

## Day 4 — React Notes Application
- **Task:** Build a Notes application using React.
- **Deliverables:** Notes app with add and delete functionality.
- **Key Learnings:** React components, state, and event handling.

---

## Day 5 — Dockerized FastAPI API
- **Task:** Build and containerize a FastAPI application.
- **Deliverables:** FastAPI app with Docker support and API documentation.
- **Key Learnings:** REST APIs, FastAPI, and Docker.

---

## Day 6 — AI Use Cases in Engineering
- **Task:** Research practical AI applications in engineering.
- **Deliverables:** Documented ten AI use cases with their applications.
- **Key Learnings:** AI capabilities and real-world use cases.

---

## Day 7 — Prompt Library
- **Task:** Create a library of reusable AI prompts.
- **Deliverables:** Collection of prompts with examples and iterations.
- **Key Learnings:** Prompt engineering and structured prompting.

---

## Day 8 — First LLM API Integration
- **Task:** Integrate an LLM API into a Python application.
- **Deliverables:** API script with environment variable support and JSON output.
- **Key Learnings:** API integration and response handling.

---

## Day 9 — Document Chunking & Embeddings
- **Task:** Build the ingestion stage of a RAG pipeline.
- **Deliverables:** Document chunking, embeddings, and similarity search.
- **Key Learnings:** Embeddings, semantic search, and RAG basics.

---

## Day 10 — Project Scaffold
- **Task:** Set up the capstone project environment.
- **Deliverables:** Configured backend/frontend and contributed via a pull request.
- **Key Learnings:** Project setup, collaboration, and development workflow.

<br>

---

> # 🌐 [ENTERPRISE STAGE] PRODUCTION CAPSTONE PROJECT
> **From Day 11 onward, the repository transitions from foundational learning to the architectural scaffold, building, testing, and deployment of a full-stack, enterprise-ready AI Assistant. The following logs document the core project development phase.**

---

<br>

## Day 11 — Chat & Health Endpoints
- **Topic:** FastAPI Routing, SQLAlchemy ORM & PostgreSQL Integration
- **Deliverables:** Implemented `GET /health` and `POST /chat` endpoints; integrated PostgreSQL with SQLAlchemy for database connectivity.
- **Key Learnings:** Understood FastAPI dependency injection using `Depends(get_db)` and mastered SQLAlchemy CRUD operations (`query()`, `add()`, `commit()`, and `refresh()`).

---

## Day 12 — Chat Screen Wired to Backend
- **Topic:** React Chat UI, TypeScript & FastAPI Integration
- **Deliverables:** Built a reactive chat interface with user/assistant message bubbles connected to the FastAPI backend with explicit error handling.
- **Key Learnings:** Integrated a React frontend with a FastAPI backend using Axios and handled multi-state management for smooth chat conversation flows.

---

## Day 13 — End-to-End Prompt → Response
- **Topic:** LLM API Integration, Memory Management & Robust Exception Infrastructure
- **Deliverables:** Completed core LLM UI integration with a 20-message rolling chat history capability and an isolated config system prompt. Implemented safe fallback structures returning user-friendly `HTTP 502` errors if downstream LLM providers drop connections.
- **Key Learnings:** Learned context windows management using rolling history arrays and established defensive coding practices separating system prompts from raw route logic.

---

## Day 14 — Persist Chunks & Embeddings
- **Topic:** Document Parsing Engine, Vector Storage & Database Transaction Workflows
- **Deliverables:** Engineered an upload pipeline (`POST /documents/upload_multiple`) accepting `.txt` and `.pdf` binaries to chunk, embed, and store context. Built document inventory views (`GET /documents`) displaying processing status and active chunk counts. Integrated an implicit delete-then-insert mechanism to prevent vector duplication upon file re-upload.
- **Key Learnings:** Gained experience in multi-format structural text extraction (PyPDF/Plaintext), relational schemas mapping vector chunks to parent objects, and relational data cleaning principles.

---

## Day 15 — RAG Chat (Week 3 Milestone)
- **Topic:** Knowledge Base Grounding, Retrieval-Augmented Generation & Hallucination Guardrails
- **Deliverables:** Connected the real-time retrieval database engine directly into the generation prompt loop. Programmed strict containment guardrails causing the assistant to answer with an honest refusal if requested parameters fall outside provided data text scope. Made top-K retrieval count dynamically configurable through environment variables.
- **Key Learnings:** Mastered the mechanics of Vector Search-driven contextual generation, configured similarity query constraints, and mitigated LLM hallucinations by establishing tight, document-bound answering rules.

---

## Day 16 — Your Feature: Structured Document Actions
- **Topic:** Structural Document Intelligence, Strict Schema Enforcement & UI Render Components
- **Deliverables:** Developed an end-to-end extraction feature that transforms massive unstructured enterprise documents into rigid JSON datasets. Created safe parsing utility methods handling malformed API text with `HTTP 502` traps. Tied the backend directly into an action panel display component inside the React client.
- **Key Learnings:** Enforced programmatic constraints on LLM outputs using schema matching, guarded structural data transformations against parsing exceptions, and mapped nested structures directly into interface views.

---

## Day 17 — Test Set & One Fix
- **Topic:** Continuous Integration Testing, Metrics Evaluation & System Prompt Optimization
- **Deliverables:** Designed a robust 10-case evaluation harness (`testcases.csv`) featuring answerable, unanswerable, and adversarial prompt injection challenges. Automated execution via an independent evaluation script, established baseline accuracy trends inside `EVAL.md`, and optimized token constraints to successfully push scores from baseline to enhanced target heights.
- **Key Learnings:** Discovered how to mathematically track and evaluate AI application accuracy, separate instruction-following failures from data retrieval drops, and fortify safety prompts against systemic prompt injection.

---

## Day 18 — One-Command Full Stack
- **Topic:** Multi-Container Systems Orchestration & Deterministic Environment Portability
- **Deliverables:** Engineered a unified `docker-compose.yml` infrastructure that stands up the vector database, Python API container, and Vite React frontend with a single terminal command. Documented an immutable environment configuration system (`.env.example`) ensuring error-free cloning.
- **Key Learnings:** Gained deep operational knowledge of multi-container networking variables, volume mount persistence, container startup dependency order, and production environment standardization.

---

## Day 19 — Final Repo & Demo Video
- **Topic:** Production Release Lifecycle, Technical Architecture Mapping & Product Demonstrations
- **Deliverables:** Patched remaining runtime bugs, built a structural overview document (`ARCHITECTURE.md`) breaking down container models, and recorded an end-to-end user-journey product run. Generated the stable `v1.0` release tag in the repository.
- **Key Learnings:** Translated technical module dependencies into high-level systems diagrams and learned how to succinctly articulate complex full-stack architecture paradigms to business stakeholders.

---

## Day 20 — Final Submission
- **Topic:** Technical Portfolio Management & Engineering Retrospectives
- **Deliverables:** Finalized the deployment package consisting of code architecture indexes, evaluation ledgers, video components, and an explicit personal engineering retrospective document detailing project decisions.
- **Key Learnings:** Synthesized the technical deliverables into a complete asset delivery pipeline, evaluated individual engineering choices made during code architecture, and structured future learning objectives.

---

# 🛠️ Technologies

- **Languages:** Python, TypeScript, SQL
- **Frameworks:** FastAPI, React, Vite
- **Data & AI:** PostgreSQL, pgvector, Google GenAI SDK (Gemini)
- **DevOps:** Docker, Docker Compose, Git & GitHub
- **Methodologies:** Prompt Engineering, RAG Pipelines, Automated LLM Evaluation

Click the link below to watch the live walk-through and explanation of the project:

> ### 🎬 [**Watch the Smart Support Assistant Demo Video**](https://drive.google.com/file/d/17K3BGVZdKgxFqcoIf4iCn1zn-xKFG33z/view?usp=sharing)

## 📋 What is Covered in the Presentation

The video walks through the complete lifecycle of the application and demonstrates the key deliverables:

### 1. Architectural Walk-through
*   A brief overview of the full-stack flow (React frontend, FastAPI backend, PostgreSQL database with `pgvector`, and Google Gemini API integration).
*   Explanation of the document ingestion and chunking strategy.

### 2. Live Feature Demonstration ("The Golden Path")
*   **Multi-Document Upload:** Uploading multiple PDF/TXT files and monitoring successful ingestion/embedding generation.
*   **RAG-Grounding Chat:** Asking questions directly related to the uploaded document content and showing how the assistant retrieves relevant chunks to form answers.
*   **Summarize Feature:** Demonstrating the document summarization tool, which returns parsed, structured JSON outputs of key points.

### 3. System Robustness & Error Handling
*   Demonstration of how the backend gracefully recovers from database connection losses (using transactional rollbacks and automatic reconnection pool pings).
*   Handling of Gemini API rate limits (exponential backoff retry logic).

---

This repository serves as my internship portfolio, showcasing the projects, assignments, and concepts I've learned throughout the AI Internship Program.