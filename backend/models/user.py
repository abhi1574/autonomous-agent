from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from .database import Base
import uuid
import enum
from datetime import datetime, UTC

class UserRole(str, enum.Enum):
    admin  = "admin"
    user   = "user"
    viewer = "viewer"

class User(Base):
    __tablename__ = "users"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username        = Column(String(100), unique=True, nullable=False, index=True)
    email           = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active       = Column(Boolean, default=True)
    role            = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    created_at      = Column(DateTime, default=lambda: datetime.now(UTC))