from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    admin  = "admin"
    user   = "user"
    viewer = "viewer"

class UserCreate(BaseModel):
    username : str
    email    : EmailStr
    password : str
    role    : UserRole = UserRole.user

class UserLogin(BaseModel):
    username : str
    password : str

class UserResponse(BaseModel):
    id        : UUID
    username  : str
    email     : str
    is_active : bool
    role      : UserRole
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)