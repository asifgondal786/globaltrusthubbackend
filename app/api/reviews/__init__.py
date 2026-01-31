"""
Reviews API Router
Review and rating endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.dependencies import get_current_active_user, get_current_verified_user, get_admin_user
from app.models.user import User
from app.schemas.review_schema import (
    ReviewCreate,
    ReviewUpdate,
    ReviewResponse,
    ReviewListResponse,
    ReviewReport,
    ReviewHelpful,
    ReviewModerationAction,
)

router = APIRouter()


@router.post("/", response_model=ReviewResponse)
async def create_review(
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_verified_user),
):
    """
    Submit a new review.
    
    Requires verification level 2+.
    """
    # In production: validate target exists, check for duplicate, AI analysis
    
    return ReviewResponse(
        id="review_123",
        reviewer_id=current_user.id,
        target_id=review_data.target_id,
        target_type=review_data.target_type,
        rating=review_data.rating,
        title=review_data.title,
        content=review_data.content,
        is_verified_transaction=review_data.transaction_id is not None,
        status="pending",
        helpful_count=0,
        created_at="2024-01-01T00:00:00Z",
    )


@router.get("/", response_model=ReviewListResponse)
async def list_reviews(
    target_id: str = Query(...),
    target_type: str = Query(...),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=50),
    sort_by: str = Query("recent", description="recent, rating_high, rating_low, helpful"),
):
    """
    List reviews for a target entity.
    """
    return ReviewListResponse(
        reviews=[],
        total=0,
        page=page,
        per_page=per_page,
        average_rating=0.0,
        rating_distribution={"5": 0, "4": 0, "3": 0, "2": 0, "1": 0},
    )


@router.get("/my-reviews")
async def list_my_reviews(
    page: int = Query(1, ge=1),
    current_user: User = Depends(get_current_active_user),
):
    """
    List current user's submitted reviews.
    """
    return {"reviews": [], "total": 0, "page": page}


@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review(review_id: str):
    """
    Get a specific review.
    """
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Review not found",
    )


@router.patch("/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: str,
    update_data: ReviewUpdate,
    current_user: User = Depends(get_current_active_user),
):
    """
    Update a review (by author only).
    """
    # In production: verify ownership
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Review not found",
    )


@router.delete("/{review_id}")
async def delete_review(
    review_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """
    Delete a review (by author only).
    """
    return {"message": f"Review {review_id} deleted"}


@router.post("/{review_id}/helpful")
async def mark_review_helpful(
    review_id: str,
    helpful: bool = True,
    current_user: User = Depends(get_current_active_user),
):
    """
    Mark a review as helpful or not.
    """
    return {
        "review_id": review_id,
        "helpful": helpful,
        "new_count": 1 if helpful else 0,
    }


@router.post("/{review_id}/report")
async def report_review(
    review_id: str,
    report_data: ReviewReport,
    current_user: User = Depends(get_current_active_user),
):
    """
    Report a review for moderation.
    """
    return {
        "message": "Review reported for moderation",
        "report_id": "report_123",
    }


# Admin endpoints

@router.get("/admin/pending")
async def list_pending_reviews(
    page: int = Query(1, ge=1),
    admin_user: User = Depends(get_admin_user),
):
    """
    List reviews pending moderation (admin only).
    """
    return {"reviews": [], "total": 0, "page": page}


@router.post("/admin/{review_id}/moderate")
async def moderate_review(
    review_id: str,
    action: ReviewModerationAction,
    admin_user: User = Depends(get_admin_user),
):
    """
    Moderate a review (admin only).
    """
    return {
        "message": f"Review {review_id} has been {action.action}",
        "moderated_by": admin_user.id,
    }
