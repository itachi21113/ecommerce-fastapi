from pydantic import BaseModel, Field , ConfigDict, EmailStr , field_validator
from enum import Enum
from datetime import datetime
from app.core.security import validate_password as validate_password_policy

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=64)

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        return validate_password_policy(password)

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

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel):
    refresh_token: str