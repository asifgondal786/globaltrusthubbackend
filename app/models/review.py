"""
Review Model
Model for user reviews and ratings.
"""

from datetime import datetime
from typing import Optional
from enum import Enum as PyEnum


class ReviewType(str, PyEnum):
    """Types of reviews."""
    SERVICE = "service"
    AGENT = "agent"
    INSTITUTION = "institution"
    EMPLOYER = "employer"
    LANDLORD = "landlord"
    EXPERIENCE = "experience"


class ReviewStatus(str, PyEnum):
    """Review moderation status."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    FLAGGED = "flagged"


class Review:
    """
    Review model for user feedback and ratings.
    
    Attributes:
        id: Unique review identifier
        reviewer_id: User ID of reviewer
        target_id: ID of entity being reviewed
        target_type: Type of entity being reviewed
        
        # Review Content
        rating: Numeric rating (1-5)
        title: Review title
        content: Review text content
        
        # Verification
        is_verified_transaction: Whether review is from verified transaction
        transaction_id: Associated transaction if applicable
        
        # Moderation
        status: Moderation status
        moderated_by: Moderator who reviewed
        moderated_at: Moderation timestamp
        rejection_reason: Reason if rejected
        
        # Engagement
        helpful_count: Number of "helpful" votes
        report_count: Number of reports
        
        # Timestamps
        created_at: Review creation timestamp
        updated_at: Last update timestamp
    """
    
    __tablename__ = "reviews"
    
    id: str = ""
    reviewer_id: str = ""
    target_id: str = ""
    target_type: ReviewType = ReviewType.SERVICE
    
    # Review Content
    rating: int = 5
    title: str = ""
    content: str = ""
    
    # Verification
    is_verified_transaction: bool = False
    transaction_id: Optional[str] = None
    
    # Moderation
    status: ReviewStatus = ReviewStatus.PENDING
    moderated_by: Optional[str] = None
    moderated_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    
    # AI Analysis
    sentiment_score: float = 0.0
    scam_language_detected: bool = False
    
    # Engagement
    helpful_count: int = 0
    report_count: int = 0
    
    # Timestamps
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self) -> str:
        return f"<Review(id={self.id}, rating={self.rating}, target={self.target_type})>"
    
    @property
    def is_published(self) -> bool:
        """Check if review is publicly visible."""
        return self.status == ReviewStatus.APPROVED
    
    @property
    def needs_moderation(self) -> bool:
        """Check if review needs manual moderation."""
        return (
            self.status == ReviewStatus.PENDING or
            self.report_count >= 3 or
            self.scam_language_detected
        )
    
    @property
    def trust_weight(self) -> float:
        """Calculate weight of review for trust score calculation."""
        weight = 1.0
        
        # Verified transactions have more weight
        if self.is_verified_transaction:
            weight *= 1.5
        
        # Helpful reviews have more weight
        if self.helpful_count > 10:
            weight *= 1.2
        
        return weight
