# Groq API Setup

Groq provides an OpenAI-compatible API with a free developer tier and rate limits.
This project can use Groq for the `analysis` and `brief` LangGraph steps.

## 1. Create API Key

Create a Groq API key from:

```text
https://console.groq.com/keys
```

Do not commit the key to GitHub.

## 2. Add Key On Server

On the server:

```bash
cd /root/sdg-policy-intelligence-agent/backend
nano .env
```

Add:

```env
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

Then restart:

```bash
systemctl restart sdg-policy-backend
```

Check:

```bash
curl http://localhost:8000/health
```

## 3. How To Know It Works

Ask a question in the web UI. The answer should read less like a fixed template
and more like a natural policy analysis.

If the key is missing or rate-limited, the app falls back to the local
template-based response.
