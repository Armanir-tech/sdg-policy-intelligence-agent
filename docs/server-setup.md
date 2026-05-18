# Server Setup

These commands are for a small Ubuntu 22.04 server with about 3 GB RAM.

## Server Status

The server has been reinstalled with Ubuntu 22.04 LTS. This is a good base for
the project because it supports modern Python, Node.js, Docker, FastAPI, and
frontend tooling.

## 1. System Packages

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git curl
```

## 2. Node.js

Use Node.js 20 LTS:

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

## 3. Backend

```bash
cd ~/sdg-policy-intelligence-agent/backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 4. Frontend

```bash
cd ~/sdg-policy-intelligence-agent/frontend
npm install
npm run dev
```

## 5. Browser

Open:

```text
http://SERVER_IP:5173
```

The frontend calls:

```text
http://SERVER_IP:8000/research
```

If needed, create `frontend/.env`:

```bash
cp .env.example .env
nano .env
```

Then set:

```text
VITE_API_BASE_URL=http://SERVER_IP:8000
```

For the first version, the backend returns a mock response. Then we connect the real RAG and agent workflow.
