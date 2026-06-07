from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from .database import Base
import uuid
from datetime import datetime, UTC

class User(Base):
    __tablename__ = "users"

    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username   = Column(String(100), unique=True, nullable=False, index=True)
    email      = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active  = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))