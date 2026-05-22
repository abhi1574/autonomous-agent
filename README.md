# Autonomous Agent System

A multi-agent orchestration system built with FastAPI, React, and Claude API.

## Architecture
- **Orchestrator** — task planning and agent dispatch
- **Agents** — Research, RAG, Critic, Coding, Browser
- **Memory** — PostgreSQL (task history) + Redis (state) + Qdrant (vector/RAG)
- **Frontend** — React + TypeScript dashboard with real-time WebSocket feed

## Tech Stack
`FastAPI` `React` `TypeScript` `PostgreSQL` `Redis` `Qdrant` `Claude API` `Python`

## Progress
- [x] Phase 1 — Local infrastructure (PostgreSQL + Redis + Qdrant)
- [x] Phase 2 — FastAPI Gateway
- [x] Phase 3 — Orchestrator Core
- [ ] Phase 4 — Agents
- [ ] Phase 5 — Tool Router
- [ ] Phase 6 — React Frontend
- [ ] Phase 7 — Integration & Hardening

## Setup
```bash
uv venv && .venv\Scripts\activate
uv add fastapi uvicorn sqlalchemy psycopg2-binary redis qdrant-client python-dotenv
python check_infra.py
```