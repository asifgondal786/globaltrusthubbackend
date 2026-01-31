"""
Trust Score Engine - Decay Logic
Time-based trust score decay and maintenance.
"""

from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import math


class DecayReason(str, Enum):
    """Reasons for trust score decay."""
    INACTIVITY = "inactivity"
    DOCUMENT_EXPIRY = "document_expiry"
    NEGATIVE_REVIEW = "negative_review"
    REPORT_RECEIVED = "report_received"
    SUBSCRIPTION_LAPSE = "subscription_lapse"
    FAILED_VERIFICATION = "failed_verification"


class DecayConfig:
    """Configuration for trust score decay."""
    
    # Inactivity decay
    INACTIVITY_THRESHOLD_DAYS = 30  # Days before decay starts
    INACTIVITY_DECAY_RATE = 0.02  # 2% per week after threshold
    MAX_INACTIVITY_DECAY = 0.30  # Maximum 30% decay from inactivity
    
    # Document expiry decay
    DOC_EXPIRY_WARNING_DAYS = 30  # Warning before expiry
    DOC_EXPIRY_DECAY = 0.10  # 10% decay on expiry
    
    # Event-based decay
    NEGATIVE_REVIEW_DECAY = 0.02  # 2% per negative review
    REPORT_DECAY = 0.05  # 5% per validated report
    SUBSCRIPTION_LAPSE_DECAY = 0.15  # 15% for subscription lapse
    
    # Recovery rates
    POSITIVE_REVIEW_RECOVERY = 0.01  # 1% per positive review
    ACTIVITY_RECOVERY_RATE = 0.05  # 5% recovery per week of activity
    MAX_RECOVERY_PER_WEEK = 0.10  # Maximum 10% recovery per week


class TrustScoreDecay:
    """
    Manage trust score decay over time.
    
    Trust scores decay due to:
    - Prolonged inactivity
    - Document expiry
    - Negative events (reviews, reports)
    - Subscription lapses (for paid users)
    """
    
    def __init__(self, config: DecayConfig = None):
        self.config = config or DecayConfig()
    
    def calculate_inactivity_decay(
        self,
        last_activity: datetime,
        current_score: float,
    ) -> Tuple[float, Optional[str]]:
        """
        Calculate decay from inactivity.
        
        Returns:
            Tuple[float, Optional[str]]: (decay_amount, decay_reason)
        """
        now = datetime.utcnow()
        days_inactive = (now - last_activity).days
        
        if days_inactive <= self.config.INACTIVITY_THRESHOLD_DAYS:
            return 0.0, None
        
        # Calculate weeks of inactivity beyond threshold
        weeks_over = (days_inactive - self.config.INACTIVITY_THRESHOLD_DAYS) / 7
        
        # Apply exponential decay (slowing over time)
        decay_rate = self.config.INACTIVITY_DECAY_RATE
        decay_factor = 1 - math.exp(-decay_rate * weeks_over)
        
        # Cap at maximum decay
        decay_factor = min(decay_factor, self.config.MAX_INACTIVITY_DECAY)
        
        decay_amount = current_score * decay_factor
        
        reason = f"Inactive for {days_inactive} days (decay: {decay_factor:.1%})"
        
        return decay_amount, reason
    
    def calculate_document_expiry_decay(
        self,
        documents: list,
        current_score: float,
    ) -> Tuple[float, list]:
        """
        Calculate decay from expired documents.
        
        Returns:
            Tuple[float, list]: (total_decay, expired_documents)
        """
        now = datetime.utcnow()
        total_decay = 0.0
        expired_docs = []
        
        for doc in documents:
            expiry_date = doc.get("expiry_date")
            if not expiry_date:
                continue
            
            if isinstance(expiry_date, str):
                expiry_date = datetime.fromisoformat(expiry_date)
            
            if expiry_date < now:
                decay = current_score * self.config.DOC_EXPIRY_DECAY
                total_decay += decay
                expired_docs.append({
                    "document_type": doc.get("type"),
                    "expired_at": expiry_date.isoformat(),
                    "decay_applied": decay,
                })
        
        return total_decay, expired_docs
    
    def apply_event_decay(
        self,
        reason: DecayReason,
        current_score: float,
        severity: float = 1.0,
    ) -> Tuple[float, float]:
        """
        Apply decay from a specific event.
        
        Args:
            reason: Decay reason type
            current_score: Current trust score
            severity: Multiplier for decay (0.5-2.0)
        
        Returns:
            Tuple[float, float]: (new_score, decay_amount)
        """
        decay_rates = {
            DecayReason.NEGATIVE_REVIEW: self.config.NEGATIVE_REVIEW_DECAY,
            DecayReason.REPORT_RECEIVED: self.config.REPORT_DECAY,
            DecayReason.SUBSCRIPTION_LAPSE: self.config.SUBSCRIPTION_LAPSE_DECAY,
            DecayReason.FAILED_VERIFICATION: 0.10,
        }
        
        base_decay = decay_rates.get(reason, 0.05)
        actual_decay = base_decay * severity
        
        decay_amount = current_score * actual_decay
        new_score = max(0, current_score - decay_amount)
        
        return new_score, decay_amount
    
    def calculate_recovery(
        self,
        current_score: float,
        base_score: float,
        positive_events: int,
        active_weeks: int,
    ) -> Tuple[float, str]:
        """
        Calculate score recovery from positive behavior.
        
        Args:
            current_score: Current (decayed) score
            base_score: Original score before decay
            positive_events: Number of positive events (reviews, etc.)
            active_weeks: Weeks of consistent activity
        
        Returns:
            Tuple[float, str]: (recovery_amount, reason)
        """
        if current_score >= base_score:
            return 0.0, "No recovery needed"
        
        # Calculate potential recovery
        from_reviews = positive_events * self.config.POSITIVE_REVIEW_RECOVERY * base_score
        from_activity = active_weeks * self.config.ACTIVITY_RECOVERY_RATE * base_score
        
        total_recovery = from_reviews + from_activity
        
        # Cap recovery
        max_recovery = self.config.MAX_RECOVERY_PER_WEEK * base_score
        total_recovery = min(total_recovery, max_recovery)
        
        # Don't recover beyond base score
        max_possible = base_score - current_score
        total_recovery = min(total_recovery, max_possible)
        
        reason = f"Recovery: {positive_events} positive events, {active_weeks} active weeks"
        
        return total_recovery, reason
    
    def get_decay_forecast(
        self,
        current_score: float,
        last_activity: datetime,
        documents: list,
        weeks_ahead: int = 4,
    ) -> list:
        """
        Forecast trust score decay over coming weeks.
        
        Returns:
            list: Weekly projections with scores and reasons
        """
        forecast = []
        score = current_score
        
        for week in range(1, weeks_ahead + 1):
            projected_date = datetime.utcnow() + timedelta(weeks=week)
            
            # Calculate inactivity decay
            future_last_activity = last_activity  # Assume continued inactivity
            decay, reason = self.calculate_inactivity_decay(
                future_last_activity,
                score,
            )
            
            projected_score = score - decay if decay else score
            
            forecast.append({
                "week": week,
                "date": projected_date.isoformat(),
                "projected_score": max(0, projected_score),
                "decay": decay,
                "reason": reason or "No decay",
            })
            
            score = projected_score
        
        return forecast


# Global decay manager instance
trust_decay = TrustScoreDecay()
