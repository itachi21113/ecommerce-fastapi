from pydantic import BaseModel, Field , ConfigDict, EmailStr
from enum import Enum
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int  # or uuid.UUID if using UUIDs
    name: str
    email: EmailStr
    created_at: datetime

    # Allows Pydantic to read directly from SQLAlchemy ORM instances
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)

class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8, max_length=64)

class MessageResponse(BaseModel):
    message: str