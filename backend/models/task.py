import uuid
import enum
from datetime import datetime, UTC
from sqlalchemy import Column, String, Text, DateTime, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from .database import Base

class TaskStatus(str, enum.Enum):
    pending   = "pending"
    running   = "running"
    completed = "completed"
    failed    = "failed"

class Task(Base):
    __tablename__ = "tasks"

    id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title       = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status      = Column(Enum(TaskStatus), default=TaskStatus.pending, nullable=False)
    result      = Column(Text, nullable=True)
    created_at  = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at  = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))


class ToolLog(Base):
    __tablename__ = "tool_logs"

    id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id     = Column(String, nullable=True)
    agent_name  = Column(String(100), nullable=False)
    tool_name   = Column(String(100), nullable=False)
    input       = Column(Text, nullable=True)
    output      = Column(Text, nullable=True)
    status      = Column(String(50), default="success")
    duration_ms = Column(Integer, nullable=True)
    created_at  = Column(DateTime, default=lambda: datetime.now(UTC))