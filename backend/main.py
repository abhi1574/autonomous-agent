from fastapi import FastAPI
from .models.database import Base, engine
from .routers import health, tasks, auth

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Autonomous Agent Gateway",
    version="0.1.0",
    description="FastAPI gateway for the autonomous agent system"
)

app.include_router(health.router,        tags=["Health"])
app.include_router(auth.router,   prefix="/auth",  tags=["Auth"])
app.include_router(tasks.router,  prefix="/api",   tags=["Tasks"])