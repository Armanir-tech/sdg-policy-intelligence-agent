# Learning Recap

This file summarizes the project build process in the order it happened.

## 1. Server Upgrade

The original server had Ubuntu 16.04 and Python 3.5, which were too old for modern FastAPI, React, ChromaDB, and LangGraph development.

We reinstalled the server with Ubuntu 22.04.

Why:

- newer Python support,
- easier Node.js installation,
- cleaner deployment,
- better long-term compatibility.

## 2. Basic Server Tools

Installed:

```bash
apt update
apt install -y python3 python3-pip python3-venv git curl unzip build-essential
```

Why:

- Python runs the backend.
- pip installs Python packages.
- venv isolates project dependencies.
- git is needed for GitHub and source control.
- curl helps install tools and test endpoints.

## 3. Node.js

Installed Node.js 20.

Why:

- React/Vite frontend needs Node.js and npm.

## 4. Backend

Created a FastAPI backend.

Why:

- it exposes API endpoints,
- the frontend sends questions to it,
- RAG and agent workflow run there.

## 5. Frontend

Created a React/Vite frontend.

Why:

- it gives the project a real product interface,
- it makes the portfolio demo easier to understand.

## 6. Permanent Deployment

Backend:

- systemd service
- runs even after SSH terminal closes

Frontend:

- production build
- served through nginx

Why:

- development servers stop when terminal closes,
- production deployment should be persistent.

## 7. RAG

Added ChromaDB vector retrieval.

Why:

- RAG means the answer is grounded in documents,
- vector retrieval finds relevant document chunks for a question.

## 8. Agent Workflow

Added LangGraph workflow:

```text
research -> analysis -> validation -> brief
```

Why:

- each step has a clear responsibility,
- the workflow is easier to explain in interviews,
- it matches agentic AI internship expectations.

## 9. Upload

Added PDF/TXT upload.

Why:

- users can add their own policy reports,
- uploaded documents become searchable evidence.

