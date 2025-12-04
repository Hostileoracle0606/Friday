"""
Behavioral mood predictor
Predicts mood based on user behavior patterns (task completion, journaling frequency, etc.)
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
import uuid
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.models.task import Task, TaskStatus
from app.models.journal import JournalEntry


class BehavioralMoodPredictor:
    """
    Predicts mood from behavioral patterns:
    - Task completion rates
    - Upcoming deadlines
    - Journaling frequency
    - Time of day patterns
    - Activity streaks
    """
    
    def predict(
        self,
        db: Session,
        user_id: uuid.UUID,
        days_back: int = 7
    ) -> Dict[str, float]:
        """
        Predict mood from behavioral features
        
        Args:
            db: Database session
            user_id: User ID
            days_back: Number of days to analyze
            
        Returns:
            Dictionary with 'valence', 'arousal', 'confidence', and 'features'
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days_back)
        
        # Feature 1: Task completion rate
        total_tasks = db.query(Task).filter(
            and_(
                Task.user_id == user_id,
                Task.created_at >= cutoff_date
            )
        ).count()
        
        completed_tasks = db.query(Task).filter(
            and_(
                Task.user_id == user_id,
                Task.status == TaskStatus.COMPLETED,
                Task.created_at >= cutoff_date
            )
        ).count()
        
        completion_rate = completed_tasks / total_tasks if total_tasks > 0 else 0.5
        
        # Feature 2: Upcoming deadlines (urgency)
        upcoming_tasks = db.query(Task).filter(
            and_(
                Task.user_id == user_id,
                Task.due_date.isnot(None),
                Task.due_date >= datetime.utcnow(),
                Task.due_date <= datetime.utcnow() + timedelta(days=3),
                Task.status != TaskStatus.COMPLETED
            )
        ).count()
        
        # Feature 3: Overdue tasks
        overdue_tasks = db.query(Task).filter(
            and_(
                Task.user_id == user_id,
                Task.due_date.isnot(None),
                Task.due_date < datetime.utcnow(),
                Task.status != TaskStatus.COMPLETED
            )
        ).count()
        
        # Feature 4: Journaling frequency
        journal_entries = db.query(JournalEntry).filter(
            and_(
                JournalEntry.user_id == user_id,
                JournalEntry.created_at >= cutoff_date
            )
        ).count()
        
        journaling_frequency = journal_entries / days_back  # entries per day
        
        # Feature 5: Task load (total estimated time)
        total_time = db.query(func.sum(Task.estimated_time)).filter(
            and_(
                Task.user_id == user_id,
                Task.status != TaskStatus.COMPLETED,
                Task.estimated_time.isnot(None)
            )
        ).scalar() or 0
        
        # Calculate mood from features
        # High completion rate -> positive valence
        valence = (completion_rate - 0.5) * 0.6  # Scale to -0.3 to +0.3
        
        # Overdue tasks reduce valence
        if overdue_tasks > 0:
            valence -= min(0.4, overdue_tasks * 0.1)
        
        # Journaling frequency slightly increases valence (self-reflection is positive)
        valence += min(0.2, journaling_frequency * 0.1)
        
        # Clamp valence
        valence = max(-1.0, min(1.0, valence))
        
        # Arousal: based on upcoming deadlines and task load
        arousal = 0.3  # Base arousal
        
        # More upcoming deadlines -> higher arousal
        arousal += min(0.4, upcoming_tasks * 0.1)
        
        # High task load -> higher arousal (stress)
        if total_time > 0:
            arousal += min(0.3, (total_time / 600) * 0.1)  # Normalize by 600 minutes (10 hours)
        
        # Clamp arousal
        arousal = max(0.0, min(1.0, arousal))
        
        # Confidence based on data availability
        confidence = min(1.0, (total_tasks + journal_entries) / 20)
        
        features = {
            'completion_rate': round(completion_rate, 3),
            'upcoming_tasks': upcoming_tasks,
            'overdue_tasks': overdue_tasks,
            'journaling_frequency': round(journaling_frequency, 2),
            'total_task_time': int(total_time)
        }
        
        return {
            'valence': round(valence, 3),
            'arousal': round(arousal, 3),
            'confidence': round(confidence, 3),
            'features': features
        }

