"""
Mood fusion service
Combines text-based and behavioral mood predictions into a single mood profile
"""
from typing import Dict, Optional


class MoodFusion:
    """
    Fuses multiple mood signals with weighted averaging
    """
    
    def fuse(
        self,
        text_mood: Optional[Dict[str, float]] = None,
        behavioral_mood: Optional[Dict[str, float]] = None,
        weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, float]:
        """
        Fuse multiple mood predictions
        
        Args:
            text_mood: Text analysis result
            behavioral_mood: Behavioral prediction result
            weights: Custom weights for each source (default: confidence-based)
            
        Returns:
            Fused mood profile with valence, arousal, confidence
        """
        if weights is None:
            weights = {}
        
        moods = []
        total_weight = 0.0
        
        # Add text mood if available
        if text_mood and text_mood.get('confidence', 0) > 0:
            weight = weights.get('text', text_mood.get('confidence', 0.5))
            moods.append({
                'valence': text_mood['valence'],
                'arousal': text_mood['arousal'],
                'weight': weight
            })
            total_weight += weight
        
        # Add behavioral mood if available
        if behavioral_mood and behavioral_mood.get('confidence', 0) > 0:
            weight = weights.get('behavioral', behavioral_mood.get('confidence', 0.5))
            moods.append({
                'valence': behavioral_mood['valence'],
                'arousal': behavioral_mood['arousal'],
                'weight': weight
            })
            total_weight += weight
        
        # If no moods available, return neutral
        if not moods or total_weight == 0:
            return {
                'valence': 0.0,
                'arousal': 0.3,
                'confidence': 0.0,
                'source': 'none'
            }
        
        # Weighted average
        fused_valence = sum(m['valence'] * m['weight'] for m in moods) / total_weight
        fused_arousal = sum(m['arousal'] * m['weight'] for m in moods) / total_weight
        
        # Overall confidence (average of individual confidences, weighted)
        if text_mood and behavioral_mood:
            text_conf = text_mood.get('confidence', 0)
            behav_conf = behavioral_mood.get('confidence', 0)
            fused_confidence = (text_conf + behav_conf) / 2
        elif text_mood:
            fused_confidence = text_mood.get('confidence', 0)
        elif behavioral_mood:
            fused_confidence = behavioral_mood.get('confidence', 0)
        else:
            fused_confidence = 0.0
        
        # Determine primary source
        if text_mood and behavioral_mood:
            if text_mood.get('confidence', 0) > behavioral_mood.get('confidence', 0):
                source = 'text_primary'
            else:
                source = 'behavioral_primary'
        elif text_mood:
            source = 'text_only'
        else:
            source = 'behavioral_only'
        
        return {
            'valence': round(fused_valence, 3),
            'arousal': round(fused_arousal, 3),
            'confidence': round(fused_confidence, 3),
            'source': source,
            'components': {
                'text': text_mood,
                'behavioral': behavioral_mood
            }
        }

