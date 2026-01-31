"""
Trust Score Engine - Score Calculator
Core trust score calculation logic.
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum


class TrustLevel(str, Enum):
    """Trust score levels."""
    UNVERIFIED = "unverified"
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"


# Trust level thresholds
LEVEL_THRESHOLDS = {
    TrustLevel.UNVERIFIED: 0,
    TrustLevel.BRONZE: 200,
    TrustLevel.SILVER: 400,
    TrustLevel.GOLD: 600,
    TrustLevel.PLATINUM: 800,
}

# Component weights (total = 1.0)
COMPONENT_WEIGHTS = {
    "verification": 0.25,      # Document verification depth
    "transactions": 0.25,      # Successful transactions
    "reviews": 0.20,           # Reviews received
    "activity": 0.15,          # Platform engagement
    "behavior": 0.15,          # Behavior patterns
}

# Maximum score per component (before weighting)
MAX_COMPONENT_SCORE = 200


class TrustScoreCalculator:
    """
    Calculator for user trust scores.
    
    Trust score is a composite metric (0-1000) based on:
    - Verification depth (documents verified)
    - Transaction history (successful outcomes)
    - Review quality (ratings received)
    - Platform activity (engagement level)
    - Behavior analysis (response patterns, disputes)
    """
    
    def calculate_verification_score(
        self,
        verification_level: int,
        documents_verified: int,
        identity_confirmed: bool,
    ) -> float:
        """
        Calculate verification component score.
        
        Args:
            verification_level: Current verification level (0-3)
            documents_verified: Number of verified documents
            identity_confirmed: Whether identity is confirmed
        
        Returns:
            float: Score (0-200)
        """
        score = 0.0
        
        # Base score from verification level
        level_scores = {0: 0, 1: 50, 2: 100, 3: 150}
        score += level_scores.get(verification_level, 0)
        
        # Bonus for additional documents
        score += min(documents_verified * 10, 30)
        
        # Bonus for confirmed identity
        if identity_confirmed:
            score += 20
        
        return min(score, MAX_COMPONENT_SCORE)
    
    def calculate_transaction_score(
        self,
        successful_transactions: int,
        failed_transactions: int,
        total_value: float,
        dispute_rate: float,
    ) -> float:
        """
        Calculate transaction history component score.
        
        Args:
            successful_transactions: Number of successful transactions
            failed_transactions: Number of failed transactions
            total_value: Total transaction value
            dispute_rate: Rate of disputes (0-1)
        
        Returns:
            float: Score (0-200)
        """
        score = 0.0
        
        # Base score from successful transactions
        score += min(successful_transactions * 5, 100)
        
        # Bonus for high value
        if total_value > 10000:
            score += 30
        elif total_value > 5000:
            score += 20
        elif total_value > 1000:
            score += 10
        
        # Penalty for failed transactions
        score -= failed_transactions * 10
        
        # Penalty for disputes
        if dispute_rate > 0.1:
            score -= 50
        elif dispute_rate > 0.05:
            score -= 25
        
        return max(0, min(score, MAX_COMPONENT_SCORE))
    
    def calculate_review_score(
        self,
        total_reviews: int,
        average_rating: float,
        verified_reviews: int,
    ) -> float:
        """
        Calculate reviews component score.
        
        Args:
            total_reviews: Total number of reviews received
            average_rating: Average rating (1-5)
            verified_reviews: Number of reviews from verified transactions
        
        Returns:
            float: Score (0-200)
        """
        score = 0.0
        
        # Base score from review count
        score += min(total_reviews * 3, 60)
        
        # Score from average rating
        if average_rating >= 4.5:
            score += 80
        elif average_rating >= 4.0:
            score += 60
        elif average_rating >= 3.5:
            score += 40
        elif average_rating >= 3.0:
            score += 20
        
        # Bonus for verified reviews
        verified_ratio = verified_reviews / max(total_reviews, 1)
        score += verified_ratio * 40
        
        return min(score, MAX_COMPONENT_SCORE)
    
    def calculate_activity_score(
        self,
        days_active: int,
        login_frequency: float,  # Logins per week
        profile_completeness: float,  # 0-1
        response_rate: float,  # 0-1
    ) -> float:
        """
        Calculate activity component score.
        
        Args:
            days_active: Days since account creation
            login_frequency: Average logins per week
            profile_completeness: Profile completion ratio
            response_rate: Message response rate
        
        Returns:
            float: Score (0-200)
        """
        score = 0.0
        
        # Account age bonus
        if days_active > 365:
            score += 40
        elif days_active > 180:
            score += 30
        elif days_active > 90:
            score += 20
        elif days_active > 30:
            score += 10
        
        # Login frequency
        score += min(login_frequency * 5, 30)
        
        # Profile completeness
        score += profile_completeness * 50
        
        # Response rate
        score += response_rate * 50
        
        return min(score, MAX_COMPONENT_SCORE)
    
    def calculate_behavior_score(
        self,
        reported_count: int,
        scam_flags: int,
        positive_interactions: int,
        community_contributions: int,
    ) -> float:
        """
        Calculate behavior component score.
        
        Args:
            reported_count: Times user was reported
            scam_flags: AI-detected scam behavior flags
            positive_interactions: Positive interaction count
            community_contributions: Helpful actions (reviews, verified advice)
        
        Returns:
            float: Score (0-200)
        """
        # Start with base score
        score = 100.0
        
        # Penalties for negative behavior
        score -= reported_count * 15
        score -= scam_flags * 30
        
        # Bonuses for positive behavior
        score += min(positive_interactions * 2, 50)
        score += min(community_contributions * 5, 50)
        
        return max(0, min(score, MAX_COMPONENT_SCORE))
    
    def calculate_total_score(
        self,
        verification_score: float,
        transaction_score: float,
        review_score: float,
        activity_score: float,
        behavior_score: float,
    ) -> Tuple[float, Dict[str, float]]:
        """
        Calculate total trust score from components.
        
        Returns:
            Tuple[float, Dict]: (total_score, breakdown)
        """
        breakdown = {
            "verification": verification_score * COMPONENT_WEIGHTS["verification"],
            "transactions": transaction_score * COMPONENT_WEIGHTS["transactions"],
            "reviews": review_score * COMPONENT_WEIGHTS["reviews"],
            "activity": activity_score * COMPONENT_WEIGHTS["activity"],
            "behavior": behavior_score * COMPONENT_WEIGHTS["behavior"],
        }
        
        # Scale to 0-1000
        total = sum(breakdown.values()) * 5
        
        return min(total, 1000), breakdown
    
    def get_trust_level(self, score: float) -> TrustLevel:
        """Get trust level for a given score."""
        for level in reversed(list(TrustLevel)):
            if score >= LEVEL_THRESHOLDS[level]:
                return level
        return TrustLevel.UNVERIFIED
    
    def get_improvement_tips(
        self,
        breakdown: Dict[str, float],
        current_level: TrustLevel,
    ) -> List[str]:
        """Generate tips for improving trust score."""
        tips = []
        
        # Find weakest components
        weakest = min(breakdown.items(), key=lambda x: x[1])
        
        if weakest[0] == "verification":
            tips.append("Complete document verification to boost your score")
        elif weakest[0] == "transactions":
            tips.append("Complete more successful transactions")
        elif weakest[0] == "reviews":
            tips.append("Collect reviews from satisfied clients")
        elif weakest[0] == "activity":
            tips.append("Stay active on the platform and complete your profile")
        elif weakest[0] == "behavior":
            tips.append("Maintain positive interactions with the community")
        
        # Level-specific tips
        if current_level == TrustLevel.UNVERIFIED:
            tips.append("Start by verifying your identity with CNIC or passport")
        elif current_level == TrustLevel.BRONZE:
            tips.append("Reach Silver level by completing address verification")
        
        return tips


# Global calculator instance
trust_calculator = TrustScoreCalculator()
