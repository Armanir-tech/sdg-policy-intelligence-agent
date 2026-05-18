# Project Plan

## Goal

Create a polished portfolio project that shows practical agentic AI ability in a development policy context.

## Phase 1 - Skeleton

- Create repository structure.
- Add backend and frontend foundations.
- Write README and learning notes.

## Phase 2 - Backend MVP

- Add FastAPI app.
- Add health endpoint.
- Add question endpoint with mock response.

## Phase 3 - RAG

- Add PDF loading.
- Add text chunking.
- Add embeddings.
- Store document chunks in ChromaDB.
- Retrieve relevant chunks for a question.

## Phase 4 - Agent Workflow

- Add LangGraph workflow:
  - research node
  - analysis node
  - validation node
  - brief node

Status: initial workflow implemented.

## Phase 5 - Frontend

- Build a clean research-dashboard UI.
- Add question input.
- Show answer, policy brief, sources, and validation notes.
- Add PDF/TXT upload.

Status: dashboard and upload flow implemented.

## Phase 6 - Deployment

- Deploy backend and frontend on Ubuntu server.
- Add environment variables.
- Add production run instructions.
