# Smart Support Assistant

Welcome! I'm Om Priya Dash, an aspiring Software Developer and AI Engineer. This repository showcases my learning journey and project implementation completed during my AI Engineering Internship.

This repository documents my learning journey and implementation of the **Smart Support Assistant** as part of my AI Engineering Internship. Throughout this project, I built an AI-powered document assistant using modern technologies such as FastAPI, Next.js, PostgreSQL, Docker, and Google Gemini.

Over the course of 20 days, I learned backend development, frontend integration, Retrieval-Augmented Generation (RAG), vector databases, Docker, prompt engineering, and full-stack AI application development.

This README serves as a record of my daily progress, the features I implemented, and the technical skills I gained throughout the internship.

---

## Project Overview

The Smart Support Assistant is an AI-powered document question-answering application that allows users to:

- Upload PDF and TXT documents
- Extract and process document text
- Generate embeddings using Google Gemini
- Store embeddings in PostgreSQL with pgvector
- Retrieve relevant document chunks using semantic search
- Generate context-aware answers using Retrieval-Augmented Generation (RAG)
- Summarize uploaded documents
- Display AI-generated responses through an interactive chat interface

---

## Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- pgvector
- Uvicorn

### Frontend
- Next.js
- React
- TypeScript

### AI & Machine Learning
- Google Gemini API
- Gemini Embedding API
- Retrieval-Augmented Generation (RAG)

### DevOps
- Docker
- Docker Compose

### Version Control
- Git
- GitHub

---

## Key Features

- AI-powered chatbot
- Conversation memory
- PDF and TXT document upload
- Automatic text extraction
- Text chunking
- Vector embedding generation
- Semantic search
- Retrieval-Augmented Generation (RAG)
- AI-powered document summarization
- PostgreSQL with pgvector
- Dockerized full-stack application

---

# Daily Progress

# Day 1 – Tooling Setup & First AI-Generated Code
- Installed Python, Node.js, Git, Docker Desktop, and VS Code.
- Configured the development environment.
- Generated and executed a Python script that displays the current date and a motivational quote.
- Verified all required tool versions.

*Skills Learned*
- Development environment setup
- Python basics
- Running programs from the terminal

# Day 2 – GitHub Repository Setup
- Created the public `intern-learning` repository.
- Added a professional README and `.gitignore`.
- Organized project structure.
- Practiced Git workflow using commits, branches, and pull requests.

*Skills Learned*
- Git & GitHub
- Version control
- Branching and collaboration

# Day 3 – CLI To-Do Application
- Developed a command-line To-Do application in Python.
- Stored tasks in a JSON file.
- Implemented add, remove, and list functionality.
- Added error handling and virtual environment support.

*Skills Learned*
- File handling
- JSON storage
- Python functions
- Error handling

# Day 4 – React Notes Application
- Built a Notes application using React.
- Implemented adding and deleting notes.
- Managed application state with React `useState`.
- Added input validation.

*Skills Learned*
- React fundamentals
- State management
- Component-based development

# Day 5 – Dockerized FastAPI Application
- Created a FastAPI application.
- Implemented a custom `/about` endpoint.
- Dockerized the application.
- Documented build and run instructions.

*Skills Learned*
- FastAPI
- REST APIs
- Docker
- API documentation

# Day 6 – AI Use Cases Research
- Researched ten practical AI use cases.
- Categorized each by model capability.
- Identified engineering-focused AI applications.
- Selected and justified the most impactful use case.

*Skills Learned*
- AI applications
- Problem analysis
- Documentation

# Day 7 – Prompt Engineering Library
- Created five reusable production-quality prompts.
- Included system prompts, templates, examples, and prompt iterations.
- Focused on structured and reliable AI outputs.

*Skills Learned*
- Prompt engineering
- JSON output design
- Prompt optimization

# Day 8 – LLM API Integration
- Connected an LLM API using Python.
- Loaded API keys securely from `.env`.
- Processed structured JSON responses.
- Implemented exception handling.

*Skills Learned*
- API integration
- Environment variables
- JSON parsing
- Error handling

# Day 9 – Document Chunking & Embeddings
- Implemented the ingestion phase of a RAG pipeline.
- Split documents into configurable chunks.
- Generated embeddings.
- Built semantic similarity search for document retrieval.

*Skills Learned*
- RAG fundamentals
- Embeddings
- Semantic search
- Vector-based retrieval

# Day 10 – Capstone Project Setup
- Cloned the capstone project.
- Created a feature branch.
- Configured backend and frontend environments.
- Contributed to the project through a pull request.

*Skills Learned*
- Team collaboration
- Project setup
- Git workflow
- FastAPI & React environment configuration.

# Day 11 – Backend API Development
- Implemented `/health` and `/chat` endpoints.
- Created SQLAlchemy database models.
- Stored chat conversations and messages.
- Used Pydantic models for request and response validation.

*Skills Learned*
- Backend development
- SQLAlchemy
- Database integration
- REST API design

# Day 12 – Frontend Chat Integration
- Connected the React frontend with the backend chat API.
- Implemented message rendering and loading states.
- Added backend error handling.
- Used TypeScript interfaces for API communication.

*Skills Learned*
- Frontend-backend integration
- TypeScript
- API communication
- Error handling
- User interface development

# Day 13 – End-to-End Prompt → Response
- Integrated Google Gemini to generate real-time AI responses.
- Connected the frontend chat interface with the FastAPI backend.
- Implemented conversation memory using conversation IDs.
- Loaded the system prompt from a configuration file instead of hardcoding it.
- Added friendly error handling for LLM failures with HTTP 502 responses.
- Limited conversation history to the latest 20 messages.

*Skills Learned*
- Large Language Model (LLM) Integration
- Google Gemini API
- Prompt Management
- Conversation Memory
- REST API Development
- Exception Handling
- FastAPI Backend Development

# Day 14 – Persist Chunks & Embeddings
- Implemented document upload for PDF and TXT files.
- Extracted text from uploaded documents.
- Split documents into overlapping chunks.
- Generated vector embeddings using Gemini Embedding API.
- Stored documents, chunks, and embeddings in PostgreSQL using pgvector.
- Implemented duplicate document replacement by deleting existing chunks before inserting new ones.
- Created an endpoint to list uploaded documents and their chunk counts.

*Skills Learned*
- PDF Processing
- Text Chunking
- SQLAlchemy ORM
- PostgreSQL
- pgvector
- Vector Embeddings
- Database Transactions
- CRUD Operations

# Day 15 – RAG Chat (Week 3 Milestone)
- Retrieved relevant document chunks using vector similarity search.
- Embedded user queries with the same embedding model.
- Generated AI responses grounded in uploaded documents.
- Returned honest responses for questions outside the uploaded documents.
- Made the retrieval chunk count (k) configurable using environment variables.

*Skills Learned*
- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Vector Similarity Search
- Cosine Distance
- Environment Variables
- Context Retrieval
- AI-Powered Question Answering

# Day 16 – Individual Feature
- Developed a complete feature endpoint using FastAPI.
- Stored prompts in a dedicated prompts module.
- Implemented structured JSON response parsing.
- Added clean JSON parsing error handling.
- Integrated the feature into the frontend with a dedicated UI control.
- Tested the feature using multiple uploaded documents.

*Skills Learned*
- Feature Development
- Prompt Engineering
- JSON Parsing
- FastAPI Endpoints
- Frontend Integration
- Error Handling
- API Design

# Day 17 – Test Set & Evaluation
- Created a test dataset containing answerable, refusal, and challenging questions.
- Evaluated the assistant using the testing harness.
- Recorded baseline evaluation results.
- Identified retrieval and prompt-related issues.
- Improved system performance through retrieval tuning and prompt refinement.
- Documented before-and-after evaluation results.

*Skills Learned*
- AI Model Evaluation
- Test Case Design
- Prompt Optimization
- Retrieval Tuning
- Performance Analysis
- Debugging AI Systems

# Day 18 – One-Command Full Stack
- Dockerized the FastAPI backend.
- Dockerized the Next.js frontend.
- Configured PostgreSQL with pgvector using Docker Compose.
- Enabled one-command startup using Docker Compose.
- Created a complete `.env.example` configuration.
- Verified full-stack functionality in a containerized environment.

*Skills Learned*
- Docker
- Docker Compose
- Container Networking
- Multi-Container Applications
- Environment Configuration
- Deployment Workflow

# Day 19 – Final Repository & Demo
- Fixed remaining high-priority issues.
- Completed project documentation.
- Prepared the project architecture documentation.
- Recorded the end-to-end demo video.
- Finalized presentation materials and project walkthrough.
- Tagged the project as Version 1.0.

*Skills Learned*
- Technical Documentation
- Software Architecture
- Project Presentation
- Bug Fixing
- Release Management
- Git Versioning

# Day 20 – Final Submission
- Finalized the repository with all required documentation.
- Included README, Architecture, and Evaluation documents.
- Added the project demo video.
- Prepared an individual reflection summarizing project contributions, challenges, and learning outcomes.
- Verified the complete project before submission.

*Skills Learned*
- Project Documentation
- Software Delivery
- Reflection and Self-Evaluation
- Version Control
- Project Management
- Professional Software Development Practices

## Skills Gained

- Python
- FastAPI
- React & Next.js
- TypeScript
- PostgreSQL & pgvector
- Docker & Docker Compose
- Google Gemini API
- Retrieval-Augmented Generation (RAG)
- REST API Development
- Git & GitHub
- Prompt Engineering
- Debugging & Problem Solving

## Google Drive

Project files, presentation, and demo video:
https://drive.google.com/file/d/19gVrok_Q2CdOckMa3F7am1jV37LzqHOy/view?usp=sharing

*Thank you for visiting this repository! I hope this project demonstrates my learning journey and growth in AI and full-stack software development.*