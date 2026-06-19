import time
import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from backend.config import validate_env, settings
from backend.logger import get_logger
from backend.models.database import Base, engine, SessionLocal
from backend.models.user import User, UserRole
from backend.models.task import Task, ToolLog
from backend.middleware.auth import pwd_context
from backend.routers import health, tasks, auth

# ── Validate env on startup ──────────────────────────────────────────
validate_env()

logger = get_logger("main")

# ── Create DB tables ─────────────────────────────────────────────────
Base.metadata.create_all(bind=engine)

# ── Rate limiter ─────────────────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address)

# ── Seed admin user ──────────────────────────────────────────────────
def seed_admin():
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.username == "admin").first()
        if not existing:
            admin = User(
                username        = "admin",
                email           = "admin@agent.local",
                hashed_password = pwd_context.hash("admin123"),
                role            = UserRole.admin,
                is_active       = True
            )
            db.add(admin)
            db.commit()
            logger.info("✅ Admin user seeded successfully")
        else:
            logger.info("✅ Admin user already exists")
    except Exception as e:
        logger.error(f"❌ Seeding failed: {e}")
        db.rollback()
    finally:
        db.close()

# ── Start agents as background threads ───────────────────────────────
def start_agents():
    try:
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from agents.research_agent import ResearchAgent
        from agents.rag_agent      import RAGAgent
        from agents.critic_agent   import CriticAgent
        from agents.coding_agent   import CodingAgent
        from agents.browser_agent  import BrowserAgent

        agents = [
            ResearchAgent(),
            RAGAgent(),
            CriticAgent(),
            CodingAgent(),
            BrowserAgent(),
        ]

        def run_agent(agent):
            while True:
                try:
                    agent.run()
                except Exception as e:
                    logger.error(f"Agent {agent.agent_name} crashed: {e} — restarting in 5s")
                    time.sleep(5)

        for agent in agents:
            t = threading.Thread(
                target  = run_agent,
                args    = (agent,),
                daemon  = True,
                name    = f"agent-{agent.agent_name}"
            )
            t.start()
            logger.info(f"✅ {agent.agent_name} agent started as background thread")

        logger.info("✅ All agents running in background threads")

    except Exception as e:
        logger.error(f"❌ Failed to start agents: {e}")

# ── Lifespan ─────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Autonomous Agent Gateway starting up")
    logger.info(f"📦 Database : {settings.POSTGRES_DB}@{settings.POSTGRES_HOST}")
    logger.info(f"📦 Redis    : {settings.REDIS_HOST}:{settings.REDIS_PORT}")
    logger.info(f"📦 Qdrant   : {settings.QDRANT_HOST}:{settings.QDRANT_PORT}")

    # Seed admin
    seed_admin()

    # Start agents in background
    agent_thread = threading.Thread(target=start_agents, daemon=True, name="agent-starter")
    agent_thread.start()
    logger.info("✅ Agent starter thread launched")

    yield

    # Shutdown
    logger.info("🛑 Autonomous Agent Gateway shutting down")

# ── App ───────────────────────────────────────────────────────────────
app = FastAPI(
    title      = "Autonomous Agent Gateway",
    version    = "1.0.0",
    description= "Multi-agent orchestration system",
    lifespan   = lifespan
)

# ── Rate limit error handler ──────────────────────────────────────────
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ── CORS ──────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins    = settings.CORS_ORIGINS,
    allow_credentials= True,
    allow_methods    = ["*"],
    allow_headers    = ["*"],
)

# ── Request logging middleware ────────────────────────────────────────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start    = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000)
    logger.info(f"{request.method} {request.url.path} → {response.status_code} ({duration}ms)")
    return response

# ── Global error handler ──────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error on {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# ── Routers ───────────────────────────────────────────────────────────
app.include_router(health.router,        tags=["Health"])
app.include_router(auth.router,  prefix="/auth", tags=["Auth"])
app.include_router(tasks.router, prefix="/api",  tags=["Tasks"])