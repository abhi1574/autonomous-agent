from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    pending   = "pending"
    running   = "running"
    completed = "completed"
    failed    = "failed"

class TaskCreate(BaseModel):
    title: str
    description: str | None = None

class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: str | None
    status: TaskStatus
    result: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True