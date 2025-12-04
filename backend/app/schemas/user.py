from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Dict
import uuid


class UserBase(BaseModel):
    email: EmailStr
    timezone: str = "UTC"
    preferences: Dict = {}
    consents: Dict = {}


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    timezone: Optional[str] = None
    preferences: Optional[Dict] = None
    consents: Optional[Dict] = None


class UserResponse(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


