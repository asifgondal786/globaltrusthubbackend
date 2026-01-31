"""
Fraud Detection - Feature Engineering
Feature extraction for fraud detection models.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import math


class FraudFeatureExtractor:
    """
    Extract features from user behavior for fraud detection.
    
    Features include:
    - Account age and activity patterns
    - Transaction velocity and amounts
    - Network/relationship features
    - Behavioral anomalies
    """
    
    def extract_account_features(
        self,
        user_data: Dict[str, Any],
    ) -> Dict[str, float]:
        """
        Extract account-level features.
        """
        created_at = user_data.get("created_at", datetime.utcnow())
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        
        account_age_days = (datetime.utcnow() - created_at).days
        
        return {
            "account_age_days": account_age_days,
            "account_age_weeks": account_age_days / 7,
            "is_new_account": 1.0 if account_age_days < 7 else 0.0,
            "profile_completeness": user_data.get("profile_completeness", 0.0),
            "verification_level": user_data.get("verification_level", 0),
            "has_verified_email": 1.0 if user_data.get("email_verified") else 0.0,
            "has_verified_phone": 1.0 if user_data.get("phone_verified") else 0.0,
        }
    
    def extract_activity_features(
        self,
        activity_logs: List[Dict[str, Any]],
        timeframe_hours: int = 24,
    ) -> Dict[str, float]:
        """
        Extract activity pattern features.
        """
        if not activity_logs:
            return {
                "activity_count_24h": 0,
                "unique_actions": 0,
                "messages_sent": 0,
                "login_count": 0,
                "avg_session_duration": 0,
            }
        
        cutoff = datetime.utcnow() - timedelta(hours=timeframe_hours)
        recent = [a for a in activity_logs if a.get("timestamp", datetime.min) > cutoff]
        
        action_types = set(a.get("action_type") for a in recent)
        messages = [a for a in recent if a.get("action_type") == "message_sent"]
        logins = [a for a in recent if a.get("action_type") == "login"]
        
        return {
            "activity_count_24h": len(recent),
            "unique_actions": len(action_types),
            "messages_sent": len(messages),
            "login_count": len(logins),
            "avg_session_duration": 15.0,  # Placeholder
            "activity_velocity": len(recent) / max(timeframe_hours, 1),
        }
    
    def extract_transaction_features(
        self,
        transactions: List[Dict[str, Any]],
    ) -> Dict[str, float]:
        """
        Extract transaction-based features.
        """
        if not transactions:
            return {
                "total_transactions": 0,
                "successful_rate": 0.0,
                "avg_amount": 0.0,
                "max_amount": 0.0,
                "transaction_velocity": 0.0,
            }
        
        successful = [t for t in transactions if t.get("status") == "completed"]
        amounts = [t.get("amount", 0) for t in transactions]
        
        return {
            "total_transactions": len(transactions),
            "successful_count": len(successful),
            "successful_rate": len(successful) / len(transactions),
            "avg_amount": sum(amounts) / len(amounts),
            "max_amount": max(amounts),
            "min_amount": min(amounts),
            "total_amount": sum(amounts),
            "transaction_velocity": len(transactions) / 30,  # Per month
        }
    
    def extract_network_features(
        self,
        user_id: str,
        connections: List[Dict[str, Any]],
    ) -> Dict[str, float]:
        """
        Extract social/network-based features.
        """
        if not connections:
            return {
                "connection_count": 0,
                "verified_connections": 0,
                "avg_connection_trust": 0.0,
            }
        
        verified = [c for c in connections if c.get("is_verified")]
        trust_scores = [c.get("trust_score", 0) for c in connections]
        
        return {
            "connection_count": len(connections),
            "verified_connections": len(verified),
            "verified_ratio": len(verified) / len(connections),
            "avg_connection_trust": sum(trust_scores) / len(trust_scores),
            "min_connection_trust": min(trust_scores) if trust_scores else 0,
        }
    
    def extract_behavioral_features(
        self,
        behavior_data: Dict[str, Any],
    ) -> Dict[str, float]:
        """
        Extract behavioral anomaly features.
        """
        return {
            "response_rate": behavior_data.get("response_rate", 0.0),
            "avg_response_time_min": behavior_data.get("avg_response_time", 0) / 60,
            "profile_changes": behavior_data.get("profile_changes", 0),
            "report_count": behavior_data.get("report_count", 0),
            "scam_flags": behavior_data.get("scam_flags", 0),
            "dispute_count": behavior_data.get("dispute_count", 0),
        }
    
    def extract_all_features(
        self,
        user_data: Dict[str, Any],
        activity_logs: List[Dict[str, Any]],
        transactions: List[Dict[str, Any]],
        connections: List[Dict[str, Any]],
        behavior_data: Dict[str, Any],
    ) -> Dict[str, float]:
        """
        Extract all features for fraud detection.
        """
        features = {}
        
        features.update(self.extract_account_features(user_data))
        features.update(self.extract_activity_features(activity_logs))
        features.update(self.extract_transaction_features(transactions))
        features.update(self.extract_network_features(
            user_data.get("id", ""),
            connections,
        ))
        features.update(self.extract_behavioral_features(behavior_data))
        
        # Derived features
        features["risk_score_base"] = self._calculate_risk_base(features)
        
        return features
    
    def _calculate_risk_base(self, features: Dict[str, float]) -> float:
        """Calculate base risk score from features."""
        risk = 0.0
        
        # New account risk
        if features.get("is_new_account"):
            risk += 0.2
        
        # Low verification risk
        if features.get("verification_level", 0) == 0:
            risk += 0.2
        
        # High activity velocity
        if features.get("activity_velocity", 0) > 10:
            risk += 0.15
        
        # Reports/flags
        risk += features.get("scam_flags", 0) * 0.1
        risk += features.get("report_count", 0) * 0.05
        
        return min(risk, 1.0)


# Global feature extractor instance
fraud_feature_extractor = FraudFeatureExtractor()
