from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from ..core.database import Base


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskSource(str, enum.Enum):
    MANUAL = "manual"
    BRIGHTSPACE = "brightspace"
    CALENDAR = "calendar"


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    due_date = Column(DateTime(timezone=True))
    estimated_time = Column(Integer)  # in minutes
    source = Column(SQLEnum(TaskSource), default=TaskSource.MANUAL)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    user = relationship("User", backref="tasks")

