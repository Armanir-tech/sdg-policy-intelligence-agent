# AI Provider Setup

The app supports four modes:

```text
Auto -> try configured providers in order
Groq -> use GROQ_API_KEY
Gemini -> use GEMINI_API_KEY
OpenRouter -> use OPENROUTER_API_KEY
Local -> automatic fallback when no API key is available
```

## Environment Variables

Edit the backend `.env` file on the server:

```bash
cd /root/sdg-policy-intelligence-agent/backend
nano .env
```

Add whichever provider keys you have:

```env
GROQ_API_KEY=
GROQ_MODEL=llama-3.1-8b-instant

GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash

OPENROUTER_API_KEY=
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct:free
```

Restart:

```bash
systemctl restart sdg-policy-backend
```

## Provider Links

- Groq keys: `https://console.groq.com/keys`
- Gemini keys: `https://aistudio.google.com/app/apikey`
- OpenRouter keys: `https://openrouter.ai/keys`

Do not commit API keys to GitHub.

## UI Behavior

The website includes an AI provider selector:

- Auto
- Groq
- Gemini
- OpenRouter

If the selected provider is not configured or fails, the backend falls back to
local template generation so the demo keeps working.
