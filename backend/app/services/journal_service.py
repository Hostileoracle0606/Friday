from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from datetime import datetime
from ..models.journal import JournalEntry
from ..schemas.journal import JournalEntryCreate
import uuid


def create_journal_entry(
    db: Session,
    entry_data: JournalEntryCreate,
    user_id: uuid.UUID
) -> JournalEntry:
    """Create a new journal entry"""
    new_entry = JournalEntry(**entry_data.model_dump(), user_id=user_id)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


def get_user_journal_entries(
    db: Session,
    user_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
    since: Optional[datetime] = None
) -> List[JournalEntry]:
    """Get journal entries for a user with optional date filtering"""
    query = db.query(JournalEntry).filter(JournalEntry.user_id == user_id)
    
    if since:
        query = query.filter(JournalEntry.created_at >= since)
    
    return query.order_by(desc(JournalEntry.created_at)).offset(skip).limit(limit).all()


def get_journal_entry_by_id(
    db: Session,
    entry_id: uuid.UUID,
    user_id: uuid.UUID
) -> Optional[JournalEntry]:
    """Get a specific journal entry by ID, ensuring it belongs to the user"""
    return db.query(JournalEntry).filter(
        and_(JournalEntry.id == entry_id, JournalEntry.user_id == user_id)
    ).first()

