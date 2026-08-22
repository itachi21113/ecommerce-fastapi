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