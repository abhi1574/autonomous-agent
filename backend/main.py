from fastapi import FastAPI
from .models.database import Base, engine
from .routers import health, tasks, auth
from backend.models.user import User
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Autonomous Agent Gateway",
    version="0.1.0",
    description="FastAPI gateway for the autonomous agent system"
)

# CORS — allow React frontend to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router,        tags=["Health"])
app.include_router(auth.router,   prefix="/auth",  tags=["Auth"])
app.include_router(tasks.router,  prefix="/api",   tags=["Tasks"])