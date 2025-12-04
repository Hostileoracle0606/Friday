from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate
import uuid


def get_user_tasks(
    db: Session,
    user_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None
) -> List[Task]:
    """Get all tasks for a user with optional filtering"""
    query = db.query(Task).filter(Task.user_id == user_id)
    
    if status:
        query = query.filter(Task.status == status)
    
    return query.offset(skip).limit(limit).all()


def get_task_by_id(db: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Task]:
    """Get a specific task by ID, ensuring it belongs to the user"""
    return db.query(Task).filter(
        and_(Task.id == task_id, Task.user_id == user_id)
    ).first()


def create_task(db: Session, task_data: TaskCreate, user_id: uuid.UUID) -> Task:
    """Create a new task"""
    new_task = Task(**task_data.model_dump(), user_id=user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def update_task(
    db: Session,
    task_id: uuid.UUID,
    user_id: uuid.UUID,
    task_data: TaskUpdate
) -> Optional[Task]:
    """Update an existing task"""
    task = get_task_by_id(db, task_id, user_id)
    if not task:
        return None
    
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    """Delete a task"""
    task = get_task_by_id(db, task_id, user_id)
    if not task:
        return False
    
    db.delete(task)
    db.commit()
    return True


