"""
Auth API Router
Authentication endpoints.
"""

import logging
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel, EmailStr

from app.schemas.auth_schema import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    TokenRefreshRequest,
    TokenRefreshResponse,
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    ResetPasswordRequest,
    ResetPasswordResponse,
    VerifyEmailRequest,
    VerifyEmailResponse,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_token,
    get_password_hash,
    verify_password,
)
from app.core.rate_limiter import rate_limit, auth_limiter
from app.services.email_service import email_service
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()
security = HTTPBearer()


# Admin Login Schema
class AdminLoginRequest(BaseModel):
    """Schema for admin login request."""
    email: EmailStr
    password: str


class AdminLoginResponse(BaseModel):
    """Schema for admin login response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    is_admin: bool = True
    user: dict


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, _=Depends(rate_limit(auth_limiter))):
    """
    Authenticate user and return tokens.
    
    - **email**: User's email address
    - **password**: User's password
    - **remember_me**: Extended session duration
    """
    # In production: validate against database
    # For now, placeholder logic
    
    # Check if this is an admin email
    is_admin = request.email.lower() in [e.lower() for e in settings.ADMIN_EMAILS]
    
    access_token = create_access_token(data={"sub": "user_id", "is_admin": is_admin})
    refresh_token = create_refresh_token(data={"sub": "user_id"})
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=1800,
        user={"id": "user_id", "email": request.email, "is_admin": is_admin},
    )


@router.post("/admin/login", response_model=AdminLoginResponse)
async def admin_login(request: AdminLoginRequest, _=Depends(rate_limit(auth_limiter))):
    """
    Admin-specific login endpoint.
    Only allows login from registered admin emails.
    
    - **email**: Admin's email address
    - **password**: Admin's password
    """
    # Validate admin email
    if request.email.lower() not in [e.lower() for e in settings.ADMIN_EMAILS]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. This email is not authorized for admin access.",
        )
    
    # In production: validate password against database
    # For now, accept any password for demo purposes
    
    access_token = create_access_token(data={"sub": "admin_id", "is_admin": True, "role": "admin"})
    refresh_token = create_refresh_token(data={"sub": "admin_id"})
    
    logger.info(f"Admin login successful: {request.email}")
    
    return AdminLoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=1800,
        is_admin=True,
        user={"id": "admin_id", "email": request.email, "role": "admin"},
    )


@router.post("/register", response_model=RegisterResponse)
async def register(request: RegisterRequest, _=Depends(rate_limit(auth_limiter))):
    """
    Register a new user account.
    
    - **email**: User's email address
    - **password**: Minimum 8 characters with uppercase, lowercase, and digit
    - **full_name**: User's full legal name
    - **role**: User role (student, agent, institution, service_provider)
    - **user_type**: User type (student, job_seeker, service_provider)
    """
    # Validate user_type
    valid_user_types = settings.USER_TYPES
    if request.user_type not in valid_user_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid user_type. Must be one of: {', '.join(valid_user_types)}",
        )
    
    # In production: check if email exists, create user in database
    new_user_id = "new_user_id"
    
    # Generate verification token
    verification_token = create_access_token(
        data={"sub": new_user_id, "purpose": "email_verification"},
        expires_delta=timedelta(hours=24)
    )
    
    # Send verification email
    try:
        email_sent = await email_service.send_verification_email(
            email=request.email,
            token=verification_token,
        )
        if email_sent:
            logger.info(f"Verification email sent to: {request.email}")
        else:
            logger.warning(f"Failed to send verification email to: {request.email}")
    except Exception as e:
        logger.error(f"Error sending verification email: {e}")
        # Don't fail registration if email sending fails
    
    return RegisterResponse(
        message="Registration successful. Please check your email for verification.",
        user_id=new_user_id,
        email=request.email,
        requires_verification=True,
    )


@router.post("/refresh", response_model=TokenRefreshResponse)
async def refresh_token(request: TokenRefreshRequest):
    """
    Refresh access token using refresh token.
    """
    payload = verify_token(request.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    access_token = create_access_token(data={"sub": payload.get("sub")})
    
    return TokenRefreshResponse(
        access_token=access_token,
        expires_in=1800,
    )


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
async def forgot_password(request: ForgotPasswordRequest, _=Depends(rate_limit(auth_limiter))):
    """
    Request password reset email.
    """
    # Generate reset token
    reset_token = create_access_token(
        data={"sub": request.email, "purpose": "password_reset"},
        expires_delta=timedelta(hours=1)
    )
    
    # Send reset email
    try:
        await email_service.send_password_reset_email(
            email=request.email,
            token=reset_token,
        )
        logger.info(f"Password reset email sent to: {request.email}")
    except Exception as e:
        logger.error(f"Error sending password reset email: {e}")
    
    return ForgotPasswordResponse(
        message="If an account exists with this email, a reset link has been sent.",
        email=request.email,
    )


@router.post("/reset-password", response_model=ResetPasswordResponse)
async def reset_password(request: ResetPasswordRequest, _=Depends(rate_limit(auth_limiter))):
    """
    Reset password using reset token.
    """
    payload = verify_token(request.token)
    if not payload or payload.get("purpose") != "password_reset":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )
    
    # In production: update password in database
    
    return ResetPasswordResponse(message="Password has been reset successfully.")


@router.post("/verify-email", response_model=VerifyEmailResponse)
async def verify_email(request: VerifyEmailRequest):
    """
    Verify email address using verification token.
    """
    payload = verify_token(request.token)
    if not payload or payload.get("purpose") != "email_verification":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token",
        )
    
    # In production: mark email as verified in database
    logger.info(f"Email verified for user: {payload.get('sub')}")
    
    return VerifyEmailResponse(
        message="Email verified successfully.",
        is_verified=True,
    )


@router.post("/logout")
async def logout():
    """
    Logout current session.
    """
    # In production: invalidate refresh token
    return {"message": "Logged out successfully"}


@router.post("/resend-verification")
async def resend_verification(email: str):
    """
    Resend verification email.
    """
    # Generate new verification token
    verification_token = create_access_token(
        data={"sub": email, "purpose": "email_verification"},
        expires_delta=timedelta(hours=24)
    )
    
    # Send verification email
    try:
        await email_service.send_verification_email(
            email=email,
            token=verification_token,
        )
        logger.info(f"Verification email resent to: {email}")
        return {"message": "Verification email sent successfully.", "email": email}
    except Exception as e:
        logger.error(f"Error resending verification email: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send verification email. Please try again later.",
        )

