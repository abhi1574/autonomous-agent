from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    username : str
    email    : EmailStr
    password : str

class UserLogin(BaseModel):
    username : str
    password : str

class UserResponse(BaseModel):
    id        : UUID
    username  : str
    email     : str
    is_active : bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)