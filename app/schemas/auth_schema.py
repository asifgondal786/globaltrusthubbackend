"""
Auth Schema
Pydantic schemas for authentication.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Schema for login request."""
    email: EmailStr
    password: str
    remember_me: bool = False


class LoginResponse(BaseModel):
    """Schema for login response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict


class TokenRefreshRequest(BaseModel):
    """Schema for token refresh request."""
    refresh_token: str


class TokenRefreshResponse(BaseModel):
    """Schema for token refresh response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class RegisterRequest(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    full_name: str = Field(..., min_length=2, max_length=100)
    phone: Optional[str] = None
    role: str = "student"
    user_type: str = Field(default="student", description="User type: student, job_seeker, service_provider")


class RegisterResponse(BaseModel):
    """Schema for registration response."""
    message: str
    user_id: str
    email: str
    requires_verification: bool = True


class ForgotPasswordRequest(BaseModel):
    """Schema for forgot password request."""
    email: EmailStr


class ForgotPasswordResponse(BaseModel):
    """Schema for forgot password response."""
    message: str
    email: str


class ResetPasswordRequest(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)


class ResetPasswordResponse(BaseModel):
    """Schema for password reset response."""
    message: str


class VerifyEmailRequest(BaseModel):
    """Schema for email verification."""
    token: str


class VerifyEmailResponse(BaseModel):
    """Schema for email verification response."""
    message: str
    is_verified: bool


class OTPRequest(BaseModel):
    """Schema for OTP request (phone verification)."""
    phone: str


class OTPVerifyRequest(BaseModel):
    """Schema for OTP verification."""
    phone: str
    otp: str = Field(..., min_length=6, max_length=6)


class OTPResponse(BaseModel):
    """Schema for OTP response."""
    message: str
    expires_in: int


class LogoutRequest(BaseModel):
    """Schema for logout request."""
    refresh_token: Optional[str] = None


class SessionInfo(BaseModel):
    """Schema for session information."""
    session_id: str
    device: str
    ip_address: str
    location: Optional[str] = None
    created_at: datetime
    last_active: datetime
    is_current: bool = False
