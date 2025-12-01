"""
Sync routes for Brightspace and Calendar integration
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..core.database import get_db
from ..core.security import get_current_user
from ..models.user import User
from ..models.oauth_token import OAuthToken, OAuthProvider
from ..models.task import Task, TaskSource
from ..schemas.task import TaskCreate, TaskResponse
from ..services import task_service
from ...services.ingestion.brightspace_client import BrightspaceClient
from ...services.ingestion.calendar_client import GoogleCalendarClient
from ..services.encryption_service import encrypt_token, decrypt_token

router = APIRouter(prefix="/sync", tags=["sync"])


@router.post("/brightspace/authorize")
def authorize_brightspace(
    app_id: str,
    app_key: str,
    user_id: str,
    user_key: str,
    host: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Authorize and store Brightspace credentials
    Note: In production, this should use proper OAuth flow
    """
    # Store credentials (encrypted)
    # For now, we'll store them as OAuth tokens
    existing_token = db.query(OAuthToken).filter(
        OAuthToken.user_id == current_user.id,
        OAuthToken.provider == OAuthProvider.BRIGHTSPACE.value
    ).first()
    
    if existing_token:
        # Update existing token
        existing_token.access_token = encrypt_token(f"{app_id}:{app_key}:{user_id}:{user_key}:{host}")
        existing_token.updated_at = datetime.utcnow()
    else:
        # Create new token
        new_token = OAuthToken(
            user_id=current_user.id,
            provider=OAuthProvider.BRIGHTSPACE.value,
            access_token=encrypt_token(f"{app_id}:{app_key}:{user_id}:{user_key}:{host}"),
            scope="read"
        )
        db.add(new_token)
    
    db.commit()
    return {"message": "Brightspace credentials stored successfully"}


@router.post("/brightspace/sync", response_model=List[TaskResponse])
def sync_brightspace_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Sync tasks from Brightspace"""
    # Get stored credentials
    oauth_token = db.query(OAuthToken).filter(
        OAuthToken.user_id == current_user.id,
        OAuthToken.provider == OAuthProvider.BRIGHTSPACE.value
    ).first()
    
    if not oauth_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Brightspace not authorized. Please authorize first."
        )
    
    # Decrypt and parse credentials
    credentials = decrypt_token(oauth_token.access_token).split(':')
    if len(credentials) != 5:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid stored credentials"
        )
    
    app_id, app_key, user_id, user_key, host = credentials
    
    # Initialize client
    client = BrightspaceClient(app_id, app_key, user_id, user_key, host)
    
    # Fetch courses and assignments
    try:
        courses = client.get_courses()
        created_tasks = []
        
        for course in courses:
            org_unit_id = course.get('OrgUnit', {}).get('Id')
            course_name = course.get('OrgUnit', {}).get('Name', 'Unknown Course')
            
            if not org_unit_id:
                continue
            
            try:
                assignments = client.get_assignments(str(org_unit_id))
                
                for assignment in assignments:
                    # Convert to task
                    task_data = client.assignment_to_task(assignment, course_name)
                    
                    # Check if task already exists (by title and source)
                    existing = db.query(Task).filter(
                        Task.user_id == current_user.id,
                        Task.title == task_data['title'],
                        Task.source == TaskSource.BRIGHTSPACE
                    ).first()
                    
                    if not existing:
                        # Create new task
                        task_create = TaskCreate(**task_data)
                        task = task_service.create_task(db, task_create, current_user.id)
                        created_tasks.append(task)
            except Exception as e:
                # Log error but continue with other courses
                print(f"Error syncing course {course_name}: {str(e)}")
                continue
        
        return created_tasks
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to sync Brightspace tasks: {str(e)}"
        )


@router.post("/calendar/authorize")
def authorize_google_calendar(
    code: str,
    redirect_uri: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Complete Google Calendar OAuth flow
    Note: This is a simplified version - in production, handle the full OAuth flow
    """
    # In production, exchange code for tokens using the OAuth flow
    # For now, this is a placeholder
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Google Calendar OAuth not fully implemented. Use OAuth flow in production."
    )


@router.post("/calendar/sync", response_model=List[TaskResponse])
def sync_calendar_events(
    calendar_id: str = "primary",
    days_ahead: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Sync events from Google Calendar"""
    # Get stored credentials
    oauth_token = db.query(OAuthToken).filter(
        OAuthToken.user_id == current_user.id,
        OAuthToken.provider == OAuthProvider.GOOGLE_CALENDAR.value
    ).first()
    
    if not oauth_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google Calendar not authorized. Please authorize first."
        )
    
    # In production, reconstruct Credentials object from stored token
    # For now, this is a placeholder
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Google Calendar sync not fully implemented. Requires OAuth token handling."
    )

