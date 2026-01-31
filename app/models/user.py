"""
User Model
SQLAlchemy ORM model for users.
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, Boolean, DateTime, Enum, Float, Text, JSON
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

# Base would come from database setup
# from app.database.base import Base


class UserRole(str, PyEnum):
    """User roles in the system."""
    STUDENT = "student"
    JOB_SEEKER = "job_seeker"
    AGENT = "agent"
    INSTITUTION = "institution"
    SERVICE_PROVIDER = "service_provider"
    ADMIN = "admin"
    MODERATOR = "moderator"


class UserType(str, PyEnum):
    """User types for registration."""
    STUDENT = "student"
    JOB_SEEKER = "job_seeker"
    SERVICE_PROVIDER = "service_provider"


class VerificationStatus(str, PyEnum):
    """Verification status levels."""
    UNVERIFIED = "unverified"
    PENDING = "pending"
    LEVEL_1 = "level_1"
    LEVEL_2 = "level_2"
    LEVEL_3 = "level_3"
    REJECTED = "rejected"


class User:
    """
    User model representing all user types in GlobalTrustHub.
    
    Attributes:
        id: Unique identifier
        email: User's email address
        phone: Phone number
        password_hash: Hashed password
        role: User role (student, agent, institution, etc.)
        
        # Profile
        full_name: User's full legal name
        display_name: Optional display name
        avatar_url: Profile picture URL
        bio: Short biography
        
        # Verification
        is_verified: Whether user is verified
        verification_status: Current verification level
        cnic_number: National ID (Pakistan)
        passport_number: Passport number
        address: Physical address
        
        # Trust
        trust_score: Dynamic trust score (0-1000)
        
        # Status
        is_active: Account active status
        is_banned: Whether user is banned
        ban_reason: Reason for ban if applicable
        
        # Timestamps
        created_at: Account creation timestamp
        updated_at: Last update timestamp
        last_login: Last login timestamp
    """
    
    __tablename__ = "users"
    
    # Primary Key
    id: str = ""  # UUID
    
    # Authentication
    email: str = ""
    phone: Optional[str] = None
    password_hash: str = ""
    
    # Role
    role: UserRole = UserRole.STUDENT
    
    # Profile
    full_name: str = ""
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    
    # Verification
    is_verified: bool = False
    verification_status: VerificationStatus = VerificationStatus.UNVERIFIED
    cnic_number: Optional[str] = None
    passport_number: Optional[str] = None
    address: Optional[str] = None
    domicile: Optional[str] = None
    
    # Trust Score
    trust_score: float = 0.0
    
    # Status
    is_active: bool = True
    is_banned: bool = False
    ban_reason: Optional[str] = None
    
    # Metadata
    metadata: dict = {}
    
    # Timestamps
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    last_login: Optional[datetime] = None
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
    
    @property
    def is_paid_user(self) -> bool:
        """Check if user is on a paid plan."""
        return self.role in [
            UserRole.AGENT,
            UserRole.INSTITUTION,
            UserRole.SERVICE_PROVIDER,
        ]
    
    @property
    def verification_level(self) -> int:
        """Get numeric verification level."""
        level_map = {
            VerificationStatus.UNVERIFIED: 0,
            VerificationStatus.PENDING: 0,
            VerificationStatus.LEVEL_1: 1,
            VerificationStatus.LEVEL_2: 2,
            VerificationStatus.LEVEL_3: 3,
            VerificationStatus.REJECTED: 0,
        }
        return level_map.get(self.verification_status, 0)
    
    def can_access_feature(self, feature: str) -> bool:
        """Check if user can access a specific feature based on verification."""
        feature_requirements = {
            "chat": 1,
            "apply_jobs": 1,
            "submit_review": 2,
            "create_service": 2,
        }
        required_level = feature_requirements.get(feature, 0)
        return self.verification_level >= required_level
