from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from ..core.database import Base


class JournalEntry(Base):
    __tablename__ = "journal_entries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    mood_label = Column(String)  # To be filled by mood analyzer in Phase 3
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", backref="journal_entries")

