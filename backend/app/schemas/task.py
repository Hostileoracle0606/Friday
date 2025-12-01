from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid
from ..models.task import TaskStatus, TaskSource


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    estimated_time: Optional[int] = None
    source: TaskSource = TaskSource.MANUAL
    status: TaskStatus = TaskStatus.PENDING


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    estimated_time: Optional[int] = None
    status: Optional[TaskStatus] = None


class TaskResponse(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

