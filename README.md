# Cloud Deployed Multi‑Agent Support System

## Overview
This repository demonstrates a **FastAPI** backend powered by **LangGraph** agents that can handle multiple specialized tasks (billing, technical, generic). The backend is container‑ready via Docker Compose and can be exposed publicly using **ngrok**.

## Architecture
- **backend/** – FastAPI application (`backend/main.py`) and LangGraph workflow (`backend/agent.py`).
- **frontend/** – (optional) UI for interacting with the API.
- **docker‑compose.yml** – Services for backend, frontend, and optional database.
- **terraform/** – (placeholder) infrastructure as code for future cloud deployments.

## Local Development
```bash
# Start the FastAPI server
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

# (Optional) Run with Docker Compose
docker compose up --build
```

## Public Exposure with ngrok
1. Install ngrok (v3) and authenticate with your token.
2. Start a tunnel:
```bash
ngrok http 8000
```
You will receive a public URL (e.g., `https://abcd1234.ngrok.io`).
Use it to call:
```bash
curl -X POST https://<public-url>/api/chat -H "Content-Type: application/json" -d '{"message":"Hello"}'
```

## Contributing
Feel free to open issues or submit pull requests. Ensure code is formatted with `black` and passes `pytest`.

## License
MIT © 2026
