from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid


class JournalEntryBase(BaseModel):
    content: str
    mood_label: Optional[str] = None


class JournalEntryCreate(JournalEntryBase):
    pass


class JournalEntryResponse(JournalEntryBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

