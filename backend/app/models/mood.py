from sqlalchemy import Column, String, DateTime, Float, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from ..core.database import Base


class MoodProfile(Base):
    __tablename__ = "mood_profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Valence: -1 (negative) to 1 (positive)
    valence = Column(Float, nullable=False)
    # Arousal: 0 (calm) to 1 (excited)
    arousal = Column(Float, nullable=False)
    
    # Source of mood prediction
    source = Column(String)  # 'text', 'behavioral', 'fused'
    confidence = Column(Float)  # 0 to 1
    
    # Additional metadata
    metadata = Column(JSON)  # Store emotion labels, features, etc.
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", backref="mood_profiles")

