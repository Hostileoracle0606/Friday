"""
Mood analysis routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from ..core.database import get_db
from ..core.security import get_current_user
from ..models.user import User
from ..models.mood import MoodProfile
from ..models.journal import JournalEntry
from ..schemas.mood import MoodProfileResponse, MoodAnalysisRequest
from ..models.mood import MoodProfile

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from services.mood.text_analyzer import TextMoodAnalyzer
from services.mood.behavioral_predictor import BehavioralMoodPredictor
from services.mood.mood_fusion import MoodFusion

router = APIRouter(prefix="/mood", tags=["mood"])

text_analyzer = TextMoodAnalyzer()
behavioral_predictor = BehavioralMoodPredictor()
mood_fusion = MoodFusion()


@router.post("/analyze-text", response_model=MoodProfileResponse)
def analyze_text_mood(
    request: MoodAnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Analyze mood from text"""
    result = text_analyzer.analyze(request.text)
    
    # Store mood profile
    mood_profile = MoodProfile(
        user_id=current_user.id,
        valence=result['valence'],
        arousal=result['arousal'],
        source='text',
        confidence=result['confidence'],
        metadata={
            'emotions': result.get('emotions', []),
            'text_length': len(request.text)
        }
    )
    db.add(mood_profile)
    db.commit()
    db.refresh(mood_profile)
    
    return mood_profile


@router.post("/predict-behavioral", response_model=MoodProfileResponse)
def predict_behavioral_mood(
    days_back: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Predict mood from behavioral patterns"""
    result = behavioral_predictor.predict(db, current_user.id, days_back)
    
    # Store mood profile
    mood_profile = MoodProfile(
        user_id=current_user.id,
        valence=result['valence'],
        arousal=result['arousal'],
        source='behavioral',
        confidence=result['confidence'],
        metadata=result.get('features', {})
    )
    db.add(mood_profile)
    db.commit()
    db.refresh(mood_profile)
    
    return mood_profile


@router.get("/current", response_model=MoodProfileResponse)
def get_current_mood(
    use_text: bool = True,
    use_behavioral: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current fused mood profile"""
    text_mood = None
    behavioral_mood = None
    
    # Get latest journal entry for text analysis
    if use_text:
        latest_journal = db.query(JournalEntry).filter(
            JournalEntry.user_id == current_user.id
        ).order_by(JournalEntry.created_at.desc()).first()
        
        if latest_journal:
            text_mood = text_analyzer.analyze(latest_journal.content)
            # Update journal entry with mood label
            if not latest_journal.mood_label:
                # Determine emotion label from valence/arousal
                if text_mood['valence'] > 0.5:
                    latest_journal.mood_label = 'positive'
                elif text_mood['valence'] < -0.5:
                    latest_journal.mood_label = 'negative'
                else:
                    latest_journal.mood_label = 'neutral'
                db.commit()
    
    # Get behavioral prediction
    if use_behavioral:
        behavioral_mood = behavioral_predictor.predict(db, current_user.id)
    
    # Fuse moods
    fused = mood_fusion.fuse(text_mood, behavioral_mood)
    
    # Store fused mood profile
    mood_profile = MoodProfile(
        user_id=current_user.id,
        valence=fused['valence'],
        arousal=fused['arousal'],
        source='fused',
        confidence=fused['confidence'],
        metadata={
            'source_breakdown': fused.get('source'),
            'components': fused.get('components', {})
        }
    )
    db.add(mood_profile)
    db.commit()
    db.refresh(mood_profile)
    
    return mood_profile


@router.get("/history")
def get_mood_history(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get mood history"""
    cutoff = datetime.utcnow() - timedelta(days=days)
    
    profiles = db.query(MoodProfile).filter(
        MoodProfile.user_id == current_user.id,
        MoodProfile.created_at >= cutoff
    ).order_by(MoodProfile.created_at.desc()).all()
    
    return profiles

