from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime
from ..core.database import get_db
from ..core.security import get_current_user
from ..models.user import User
from ..schemas.journal import JournalEntryCreate, JournalEntryResponse
from ..services import journal_service

router = APIRouter(prefix="/journal", tags=["journal"])


@router.post("", response_model=JournalEntryResponse, status_code=status.HTTP_201_CREATED)
def create_journal_entry(
    entry_data: JournalEntryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit a new journal entry"""
    entry = journal_service.create_journal_entry(db, entry_data, current_user.id)
    return entry


@router.get("", response_model=List[JournalEntryResponse])
def get_journal_entries(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    since: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get journal entry history for the current user"""
    entries = journal_service.get_user_journal_entries(
        db, current_user.id, skip=skip, limit=limit, since=since
    )
    return entries


@router.get("/{entry_id}", response_model=JournalEntryResponse)
def get_journal_entry(
    entry_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific journal entry by ID"""
    import uuid
    try:
        entry_uuid = uuid.UUID(entry_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid entry ID format"
        )
    
    entry = journal_service.get_journal_entry_by_id(db, entry_uuid, current_user.id)
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Journal entry not found"
        )
    return entry

