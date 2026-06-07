## Progress
- [x] Phase 1 — Local infrastructure (PostgreSQL + Redis + Qdrant)
- [x] Phase 2 — FastAPI Gateway (JWT auth + Task endpoints + WebSocket)
- [x] Phase 3 — Orchestrator Core (Planner + Dispatcher + Memory)
- [x] Phase 4 — Agents (Research + RAG + Critic + Coding + Browser)
- [x] Phase 5 — Tool Router (Central registry + real embeddings + PostgreSQL logging)
- [x] Phase 6 — React Frontend (Login + Register + Dashboard + WebSocket feed)
- [ ] Phase 7 — Integration & Hardening

## Running locally
# Backend
uvicorn backend.main:app --reload --port 8000

# Frontend
cd frontend && npm run dev