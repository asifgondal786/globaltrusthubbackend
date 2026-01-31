"""
Review Schema
Pydantic schemas for reviews.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    """Schema for creating a review."""
    target_id: str
    target_type: str
    rating: int = Field(..., ge=1, le=5)
    title: str = Field(..., min_length=5, max_length=100)
    content: str = Field(..., min_length=20, max_length=2000)
    transaction_id: Optional[str] = None


class ReviewUpdate(BaseModel):
    """Schema for updating a review."""
    rating: Optional[int] = Field(None, ge=1, le=5)
    title: Optional[str] = Field(None, min_length=5, max_length=100)
    content: Optional[str] = Field(None, min_length=20, max_length=2000)


class ReviewResponse(BaseModel):
    """Schema for review response."""
    id: str
    reviewer_id: str
    reviewer_name: Optional[str] = None
    reviewer_avatar: Optional[str] = None
    target_id: str
    target_type: str
    rating: int
    title: str
    content: str
    is_verified_transaction: bool
    status: str
    helpful_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ReviewListResponse(BaseModel):
    """Schema for paginated review list."""
    reviews: List[ReviewResponse]
    total: int
    page: int
    per_page: int
    average_rating: float
    rating_distribution: dict


class ReviewReport(BaseModel):
    """Schema for reporting a review."""
    review_id: str
    reason: str = Field(..., min_length=10, max_length=500)
    category: str = Field(..., description="spam, inappropriate, fake, other")


class ReviewHelpful(BaseModel):
    """Schema for marking review as helpful."""
    review_id: str
    helpful: bool = True


class ReviewModerationAction(BaseModel):
    """Schema for admin moderation action."""
    review_id: str
    action: str = Field(..., description="approve, reject, flag")
    reason: Optional[str] = None
