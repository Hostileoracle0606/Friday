from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
import uuid


class MoodAnalysisRequest(BaseModel):
    text: str


class MoodProfileResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    valence: float
    arousal: float
    source: str
    confidence: float
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

