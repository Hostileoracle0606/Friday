from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from ..core.database import Base


class OAuthProvider(str, enum.Enum):
    BRIGHTSPACE = "brightspace"
    GOOGLE_CALENDAR = "google_calendar"


class OAuthToken(Base):
    __tablename__ = "oauth_tokens"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    provider = Column(String, nullable=False)  # OAuthProvider enum value
    access_token = Column(Text, nullable=False)  # Encrypted
    refresh_token = Column(Text)  # Encrypted, optional
    token_expires_at = Column(DateTime(timezone=True))
    scope = Column(String)  # OAuth scopes granted
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    user = relationship("User", backref="oauth_tokens")

