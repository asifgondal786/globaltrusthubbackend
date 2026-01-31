"""
Trust Score Schema
Pydantic schemas for trust score.
"""

from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class TrustScoreResponse(BaseModel):
    """Schema for trust score response."""
    user_id: str
    score: float = Field(..., ge=0, le=1000)
    level: str = Field(..., description="unverified, bronze, silver, gold, platinum")
    percentile: float = Field(..., ge=0, le=100)
    last_updated: datetime
    
    # Score breakdown
    verification_score: float
    activity_score: float
    review_score: float
    behavior_score: float
    
    class Config:
        from_attributes = True


class TrustScoreBreakdown(BaseModel):
    """Detailed trust score breakdown."""
    user_id: str
    total_score: float
    
    # Component scores
    components: Dict[str, float] = Field(
        default_factory=dict,
        description={
            "verification_depth": "Score from document verification (0-200)",
            "transaction_history": "Score from successful transactions (0-200)",
            "review_quality": "Score from reviews received (0-200)",
            "platform_activity": "Score from platform engagement (0-200)",
            "behavior_analysis": "Score from behavior patterns (0-200)",
        }
    )
    
    # Factors affecting score
    positive_factors: List[str] = []
    negative_factors: List[str] = []
    
    # Recommendations
    improvement_tips: List[str] = []


class TrustScoreHistory(BaseModel):
    """Trust score history entry."""
    timestamp: datetime
    score: float
    change: float
    reason: str


class TrustScoreHistoryResponse(BaseModel):
    """Schema for trust score history."""
    user_id: str
    current_score: float
    history: List[TrustScoreHistory]
    trend: str = Field(..., description="increasing, stable, decreasing")


class TrustScoreUpdate(BaseModel):
    """Schema for manual trust score adjustment (admin only)."""
    user_id: str
    adjustment: float = Field(..., ge=-100, le=100)
    reason: str = Field(..., min_length=10, max_length=500)


class TrustLevelThresholds(BaseModel):
    """Trust level thresholds configuration."""
    unverified: int = 0
    bronze: int = 200
    silver: int = 400
    gold: int = 600
    platinum: int = 800


class ProviderTrustScore(BaseModel):
    """Trust score for service providers."""
    provider_id: str
    business_name: str
    score: float
    level: str
    
    # Additional metrics
    total_reviews: int
    average_rating: float
    successful_transactions: int
    dispute_rate: float
    response_time_hours: float
    
    # Badges/achievements
    badges: List[str] = []
    
    # Ranking
    category_rank: Optional[int] = None
    featured: bool = False


class TrustScoreComparison(BaseModel):
    """Compare trust scores between providers."""
    providers: List[ProviderTrustScore]
    comparison_date: datetime
