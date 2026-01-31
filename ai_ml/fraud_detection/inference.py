"""
Fraud Detection - Inference
Real-time fraud prediction.
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

from app.ai_ml.fraud_detection.feature_engineering import fraud_feature_extractor


class FraudPredictor:
    """
    Real-time fraud prediction service.
    """
    
    def __init__(self):
        self.model_loaded = False
        self.threshold = 0.5
        self.high_risk_threshold = 0.8
    
    def predict(
        self,
        features: Dict[str, float],
    ) -> Dict[str, Any]:
        """
        Predict fraud probability for given features.
        
        Returns:
            Dict with probability, risk_level, and factors
        """
        # In production: use trained model
        # probability = self.model.predict_proba(features)[0][1]
        
        # Rule-based prediction (placeholder)
        probability = self._calculate_probability(features)
        
        risk_level = self._get_risk_level(probability)
        factors = self._get_risk_factors(features)
        
        return {
            "probability": probability,
            "is_fraud": probability >= self.threshold,
            "risk_level": risk_level,
            "factors": factors,
            "timestamp": datetime.utcnow().isoformat(),
        }
    
    def _calculate_probability(self, features: Dict[str, float]) -> float:
        """Calculate fraud probability from features."""
        prob = 0.0
        
        # New account risk
        if features.get("is_new_account", 0):
            prob += 0.15
        
        # Low verification
        if features.get("verification_level", 0) == 0:
            prob += 0.15
        
        # Scam flags
        prob += min(features.get("scam_flags", 0) * 0.15, 0.3)
        
        # Reports
        prob += min(features.get("report_count", 0) * 0.1, 0.2)
        
        # High activity
        if features.get("activity_velocity", 0) > 10:
            prob += 0.1
        
        # Low response rate (for providers)
        if features.get("response_rate", 1) < 0.3:
            prob += 0.1
        
        # Base risk from feature extractor
        prob += features.get("risk_score_base", 0) * 0.2
        
        return min(prob, 1.0)
    
    def _get_risk_level(self, probability: float) -> str:
        """Get risk level label from probability."""
        if probability >= 0.8:
            return "critical"
        elif probability >= 0.6:
            return "high"
        elif probability >= 0.4:
            return "medium"
        elif probability >= 0.2:
            return "low"
        else:
            return "minimal"
    
    def _get_risk_factors(self, features: Dict[str, float]) -> List[Dict[str, Any]]:
        """Identify contributing risk factors."""
        factors = []
        
        if features.get("is_new_account"):
            factors.append({
                "factor": "new_account",
                "description": "Account created recently",
                "weight": "medium",
            })
        
        if features.get("verification_level", 0) == 0:
            factors.append({
                "factor": "unverified",
                "description": "No identity verification completed",
                "weight": "high",
            })
        
        if features.get("scam_flags", 0) > 0:
            factors.append({
                "factor": "scam_flags",
                "description": f"{features['scam_flags']} scam language detections",
                "weight": "high",
            })
        
        if features.get("report_count", 0) > 0:
            factors.append({
                "factor": "reports",
                "description": f"Reported by {features['report_count']} users",
                "weight": "high",
            })
        
        if features.get("activity_velocity", 0) > 10:
            factors.append({
                "factor": "high_activity",
                "description": "Unusually high activity volume",
                "weight": "medium",
            })
        
        return factors
    
    def predict_for_user(
        self,
        user_data: Dict[str, Any],
        activity_logs: List[Dict[str, Any]],
        transactions: List[Dict[str, Any]],
        connections: List[Dict[str, Any]],
        behavior_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Full fraud prediction for a user.
        """
        features = fraud_feature_extractor.extract_all_features(
            user_data,
            activity_logs,
            transactions,
            connections,
            behavior_data,
        )
        
        prediction = self.predict(features)
        prediction["user_id"] = user_data.get("id")
        prediction["features"] = features
        
        return prediction
    
    def batch_predict(
        self,
        users_data: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Batch fraud prediction for multiple users.
        """
        results = []
        for user_data in users_data:
            prediction = self.predict_for_user(
                user_data=user_data,
                activity_logs=user_data.get("activity_logs", []),
                transactions=user_data.get("transactions", []),
                connections=user_data.get("connections", []),
                behavior_data=user_data.get("behavior", {}),
            )
            results.append(prediction)
        return results
    
    def get_recommended_action(
        self,
        prediction: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Get recommended action based on prediction.
        """
        risk_level = prediction.get("risk_level", "minimal")
        probability = prediction.get("probability", 0)
        
        actions = {
            "critical": {
                "action": "block",
                "description": "Immediately suspend account for review",
                "auto_execute": True,
            },
            "high": {
                "action": "restrict",
                "description": "Restrict messaging and transactions",
                "auto_execute": True,
            },
            "medium": {
                "action": "monitor",
                "description": "Flag for enhanced monitoring",
                "auto_execute": False,
            },
            "low": {
                "action": "watch",
                "description": "Add to watchlist",
                "auto_execute": False,
            },
            "minimal": {
                "action": "none",
                "description": "No action required",
                "auto_execute": False,
            },
        }
        
        return actions.get(risk_level, actions["minimal"])


# Global predictor instance
fraud_predictor = FraudPredictor()
