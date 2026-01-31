"""
Users API Router
User management endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.dependencies import get_current_user, get_current_active_user, get_admin_user
from app.schemas.user_schema import (
    UserResponse,
    UserUpdate,
    UserPublicProfile,
    UserListResponse,
    PasswordChange,
    UserVerificationUpdate,
)
from app.models.user import User

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    """
    Get current authenticated user's profile.
    """
    return current_user


@router.patch("/me", response_model=UserResponse)
async def update_current_user_profile(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
):
    """
    Update current user's profile.
    """
    # In production: update user in database
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)
    
    return current_user


@router.post("/me/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_active_user),
):
    """
    Change current user's password.
    """
    # In production: verify current password and update
    return {"message": "Password changed successfully"}


@router.patch("/me/verification", response_model=UserResponse)
async def update_verification_info(
    verification_data: UserVerificationUpdate,
    current_user: User = Depends(get_current_active_user),
):
    """
    Update user's verification information.
    """
    # In production: update verification fields and trigger re-verification
    return current_user


@router.get("/{user_id}", response_model=UserPublicProfile)
async def get_user_public_profile(
    user_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """
    Get a user's public profile.
    """
    # In production: fetch user from database
    return UserPublicProfile(
        id=user_id,
        full_name="Sample User",
        role="student",
        is_verified=True,
        trust_score=750.0,
    )


@router.get("/", response_model=UserListResponse)
async def list_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    role: str = Query(None),
    admin_user: User = Depends(get_admin_user),
):
    """
    List all users (admin only).
    """
    # In production: paginated query from database
    return UserListResponse(
        users=[],
        total=0,
        page=page,
        per_page=per_page,
        pages=0,
    )


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    admin_user: User = Depends(get_admin_user),
):
    """
    Delete a user account (admin only).
    """
    # In production: soft delete user
    return {"message": f"User {user_id} has been deleted"}


@router.post("/{user_id}/ban")
async def ban_user(
    user_id: str,
    reason: str,
    admin_user: User = Depends(get_admin_user),
):
    """
    Ban a user (admin only).
    """
    # In production: set is_banned = True with reason
    return {"message": f"User {user_id} has been banned", "reason": reason}


@router.post("/{user_id}/unban")
async def unban_user(
    user_id: str,
    admin_user: User = Depends(get_admin_user),
):
    """
    Unban a user (admin only).
    """
    return {"message": f"User {user_id} has been unbanned"}
