"""
Scam Language Analysis - Model
Machine learning model for scam detection.
"""

from typing import List, Dict, Tuple, Optional
import json
from pathlib import Path

from app.ai_ml.scam_language_analysis.nlp_preprocessing import (
    preprocess_for_model,
    calculate_scam_score,
    get_risk_assessment,
)


class ScamDetectionModel:
    """
    Scam detection model combining rule-based and ML approaches.
    
    In production, this would use:
    - Fine-tuned transformer model (BERT/RoBERTa)
    - Trained on scam message datasets
    - Continuous learning from flagged messages
    """
    
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path
        self.model_loaded = False
        self.threshold = 0.5
        
        # Load model if path provided
        if model_path and Path(model_path).exists():
            self._load_model()
    
    def _load_model(self):
        """Load trained model weights."""
        # In production: load PyTorch/TensorFlow model
        self.model_loaded = True
    
    def predict(
        self,
        text: str,
    ) -> Dict:
        """
        Predict scam probability for text.
        
        Returns:
            Dict with prediction results
        """
        # Preprocess
        features = preprocess_for_model(text)
        
        # Rule-based scoring
        rule_score, rule_reasons = calculate_scam_score(text)
        
        # ML model scoring (placeholder - uses rules for now)
        if self.model_loaded:
            # In production: ml_score = self.model.predict(features)
            ml_score = rule_score  # Placeholder
        else:
            ml_score = rule_score
        
        # Combine scores
        final_score = (rule_score * 0.6 + ml_score * 0.4)
        
        # Generate assessment
        assessment = get_risk_assessment(final_score, rule_reasons)
        
        return {
            "text": text[:200] + "..." if len(text) > 200 else text,
            "scam_probability": final_score,
            "is_scam": final_score >= self.threshold,
            "rule_score": rule_score,
            "ml_score": ml_score,
            "assessment": assessment,
            "features": {
                "token_count": features["token_count"],
                "has_url": features["has_url"],
                "caps_ratio": features["caps_ratio"],
            },
        }
    
    def predict_batch(
        self,
        texts: List[str],
    ) -> List[Dict]:
        """Predict scam probability for multiple texts."""
        return [self.predict(text) for text in texts]
    
    def analyze_conversation(
        self,
        messages: List[Dict],
    ) -> Dict:
        """
        Analyze entire conversation for scam patterns.
        
        Args:
            messages: List of message dicts with 'content' and 'sender_id'
        
        Returns:
            Conversation-level analysis
        """
        if not messages:
            return {
                "risk_level": "minimal",
                "max_score": 0.0,
                "flagged_messages": [],
                "recommendation": "No messages to analyze",
            }
        
        flagged = []
        max_score = 0.0
        
        for i, msg in enumerate(messages):
            content = msg.get("content", "")
            if not content:
                continue
            
            result = self.predict(content)
            
            if result["scam_probability"] > 0.3:
                flagged.append({
                    "message_index": i,
                    "sender_id": msg.get("sender_id"),
                    "score": result["scam_probability"],
                    "preview": content[:100],
                    "reasons": result["assessment"]["details"],
                })
            
            max_score = max(max_score, result["scam_probability"])
        
        # Determine conversation risk
        if max_score >= 0.7 or len(flagged) >= 3:
            risk_level = "high"
        elif max_score >= 0.4 or len(flagged) >= 2:
            risk_level = "medium"
        elif max_score >= 0.2:
            risk_level = "low"
        else:
            risk_level = "minimal"
        
        return {
            "risk_level": risk_level,
            "max_score": max_score,
            "flagged_messages": flagged,
            "flagged_count": len(flagged),
            "total_messages": len(messages),
            "recommendation": self._get_conversation_recommendation(risk_level, flagged),
        }
    
    def _get_conversation_recommendation(
        self,
        risk_level: str,
        flagged: List,
    ) -> str:
        """Generate recommendation for conversation."""
        if risk_level == "high":
            return (
                "⚠️ HIGH RISK: This conversation shows significant scam indicators. "
                "Do not send money or share personal documents. Report if needed."
            )
        elif risk_level == "medium":
            return (
                "⚡ CAUTION: Some suspicious patterns detected. "
                "Verify claims independently before proceeding."
            )
        elif risk_level == "low":
            return (
                "ℹ️ Some minor concerns. Exercise normal caution "
                "and verify credentials."
            )
        else:
            return "✅ No significant concerns detected."
    
    def update_threshold(self, new_threshold: float):
        """Update classification threshold."""
        self.threshold = max(0.1, min(0.9, new_threshold))
    
    def get_model_info(self) -> Dict:
        """Get model metadata."""
        return {
            "model_loaded": self.model_loaded,
            "threshold": self.threshold,
            "version": "1.0.0",
            "type": "hybrid_rule_ml",
        }


# Global model instance
scam_detector = ScamDetectionModel()
