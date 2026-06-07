import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from backend.config import validate_env, settings
from backend.logger import get_logger
from backend.models.database import Base, engine
from backend.models.user import User
from backend.models.task import Task, ToolLog
from backend.routers import health, tasks, auth
from contextlib import asynccontextmanager

# Validate env on startup
validate_env()

logger = get_logger("main")

# Create tables
Base.metadata.create_all(bind=engine)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title      ="Autonomous Agent Gateway",
    version    ="1.0.0",
    description="Multi-agent orchestration system"
)

# Rate limit error handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins    =settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods    =["*"],
    allow_headers    =["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000)
    logger.info(f"{request.method} {request.url.path} → {response.status_code} ({duration}ms)")
    return response

# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error on {request.url.path}: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

# Startup event
@asynccontextmanager
async def lifespan(app):
    # Startup
    logger.info("🚀 Autonomous Agent Gateway starting up")
    logger.info(f"📦 Database: {settings.POSTGRES_DB}@{settings.POSTGRES_HOST}")
    logger.info(f"📦 Redis: {settings.REDIS_HOST}:{settings.REDIS_PORT}")
    logger.info(f"📦 Qdrant: {settings.QDRANT_HOST}:{settings.QDRANT_PORT}")
    yield
    # Shutdown
    logger.info("🛑 Autonomous Agent Gateway shutting down")

# Routers
app.include_router(health.router,        tags=["Health"])
app.include_router(auth.router,  prefix="/auth",  tags=["Auth"])
app.include_router(tasks.router, prefix="/api",   tags=["Tasks"])