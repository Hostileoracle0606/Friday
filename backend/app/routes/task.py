from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.security import get_current_user
from ..models.user import User
from ..models.task import TaskStatus
from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse
from ..services import task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=List[TaskResponse])
def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    task_status: Optional[TaskStatus] = Query(None, alias="status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all tasks for the current user"""
    tasks = task_service.get_user_tasks(
        db, current_user.id, skip=skip, limit=limit, status=task_status
    )
    return tasks


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new task"""
    task = task_service.create_task(db, task_data, current_user.id)
    return task


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific task by ID"""
    import uuid
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )
    
    task = task_service.get_task_by_id(db, task_uuid, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: str,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing task"""
    import uuid
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )
    
    task = task_service.update_task(db, task_uuid, current_user.id, task_data)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a task"""
    import uuid
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )
    
    success = task_service.delete_task(db, task_uuid, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

