"""
Text-based mood analyzer using emotion classification
Uses a simplified approach inspired by GoEmotions dataset
"""
from typing import Dict, List, Optional
import re
from collections import Counter


class TextMoodAnalyzer:
    """
    Analyzes text to infer mood (valence and arousal)
    Uses keyword-based approach as a baseline (can be replaced with ML model)
    """
    
    # Emotion keywords mapped to (valence, arousal)
    EMOTION_KEYWORDS = {
        # Positive emotions (high valence, varying arousal)
        'happy': (0.8, 0.7), 'joy': (0.9, 0.8), 'excited': (0.8, 0.9),
        'grateful': (0.7, 0.5), 'content': (0.6, 0.3), 'peaceful': (0.7, 0.2),
        'proud': (0.8, 0.6), 'hopeful': (0.7, 0.5), 'optimistic': (0.7, 0.6),
        'energetic': (0.7, 0.9), 'motivated': (0.7, 0.7), 'confident': (0.8, 0.6),
        
        # Negative emotions (low valence, varying arousal)
        'sad': (-0.6, 0.3), 'depressed': (-0.8, 0.2), 'down': (-0.5, 0.3),
        'anxious': (-0.4, 0.8), 'worried': (-0.5, 0.7), 'stressed': (-0.6, 0.8),
        'angry': (-0.7, 0.9), 'frustrated': (-0.6, 0.8), 'annoyed': (-0.5, 0.7),
        'tired': (-0.4, 0.2), 'exhausted': (-0.6, 0.1), 'burned': (-0.7, 0.2),
        'overwhelmed': (-0.7, 0.8), 'helpless': (-0.8, 0.4), 'lonely': (-0.7, 0.3),
        
        # Neutral/low arousal
        'calm': (0.2, 0.2), 'neutral': (0.0, 0.3), 'fine': (0.2, 0.3),
        'okay': (0.1, 0.3), 'meh': (-0.1, 0.2),
    }
    
    # Intensifiers that modify arousal
    INTENSIFIERS = {
        'very': 1.2, 'extremely': 1.4, 'really': 1.1, 'super': 1.3,
        'slightly': 0.8, 'a bit': 0.8, 'somewhat': 0.9, 'quite': 1.1,
    }
    
    # Negation words
    NEGATIONS = {'not', "n't", 'no', 'never', 'none', 'nothing', 'nobody'}
    
    def analyze(self, text: str) -> Dict[str, float]:
        """
        Analyze text and return mood profile
        
        Returns:
            Dictionary with 'valence', 'arousal', 'confidence', and 'emotions'
        """
        if not text or len(text.strip()) == 0:
            return {
                'valence': 0.0,
                'arousal': 0.3,
                'confidence': 0.0,
                'emotions': []
            }
        
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        # Find emotion keywords
        found_emotions = []
        emotion_scores = []
        
        for i, word in enumerate(words):
            # Check for emotion keyword
            if word in self.EMOTION_KEYWORDS:
                valence, arousal = self.EMOTION_KEYWORDS[word]
                
                # Check for negation
                is_negated = False
                if i > 0:
                    prev_words = words[max(0, i-3):i]
                    if any(neg in prev_words for neg in self.NEGATIONS):
                        is_negated = True
                        valence = -valence * 0.5  # Flip and reduce intensity
                
                # Check for intensifiers
                intensity = 1.0
                if i > 0 and words[i-1] in self.INTENSIFIERS:
                    intensity = self.INTENSIFIERS[words[i-1]]
                elif i < len(words) - 1 and words[i+1] in self.INTENSIFIERS:
                    intensity = self.INTENSIFIERS[words[i+1]]
                
                arousal *= intensity
                arousal = min(1.0, max(0.0, arousal))
                
                found_emotions.append({
                    'emotion': word,
                    'valence': valence,
                    'arousal': arousal,
                    'negated': is_negated
                })
                emotion_scores.append((valence, arousal))
        
        # Calculate average valence and arousal
        if emotion_scores:
            avg_valence = sum(v for v, _ in emotion_scores) / len(emotion_scores)
            avg_arousal = sum(a for _, a in emotion_scores) / len(emotion_scores)
            confidence = min(1.0, len(emotion_scores) * 0.3)  # More emotions = higher confidence
        else:
            # Fallback: analyze sentiment from text patterns
            avg_valence, avg_arousal, confidence = self._fallback_analysis(text_lower)
            found_emotions = []
        
        return {
            'valence': round(avg_valence, 3),
            'arousal': round(avg_arousal, 3),
            'confidence': round(confidence, 3),
            'emotions': found_emotions
        }
    
    def _fallback_analysis(self, text: str) -> tuple:
        """Fallback analysis when no emotion keywords found"""
        # Simple heuristics
        positive_words = ['good', 'great', 'nice', 'well', 'better', 'best', 'love', 'like']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'worst', 'difficult', 'hard', 'problem']
        
        pos_count = sum(1 for word in positive_words if word in text)
        neg_count = sum(1 for word in negative_words if word in text)
        
        if pos_count > neg_count:
            valence = 0.3
        elif neg_count > pos_count:
            valence = -0.3
        else:
            valence = 0.0
        
        # Estimate arousal from text length and punctuation
        exclamation_count = text.count('!')
        question_count = text.count('?')
        arousal = min(0.7, 0.3 + (exclamation_count + question_count) * 0.1)
        
        confidence = 0.2  # Low confidence for fallback
        
        return valence, arousal, confidence

