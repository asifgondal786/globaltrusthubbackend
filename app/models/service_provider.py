"""
Service Provider Model
Model for agents, institutions, and service providers.
"""

from datetime import datetime
from typing import Optional, List
from enum import Enum as PyEnum


class ProviderType(str, PyEnum):
    """Types of service providers."""
    AGENT = "agent"
    UNIVERSITY = "university"
    COLLEGE = "college"
    BANK = "bank"
    MONEY_TRANSFER = "money_transfer"
    EMPLOYER = "employer"
    LANDLORD = "landlord"
    HOSTEL = "hostel"
    HOTEL = "hotel"
    TRANSPORT = "transport"
    LEGAL = "legal"
    OTHER = "other"


class SubscriptionStatus(str, PyEnum):
    """Subscription status for paid providers."""
    TRIAL = "trial"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class ServiceProvider:
    """
    Service Provider model for businesses on GlobalTrustHub.
    
    Attributes:
        id: Unique provider identifier
        user_id: Associated user account ID
        provider_type: Type of service provider
        
        # Business Info
        business_name: Official business name
        business_license: License/registration number
        registration_country: Country of registration
        website: Official website URL
        
        # Contact
        contact_email: Business email
        contact_phone: Business phone
        address: Business address
        
        # Trust & Reputation
        trust_score: Public trust score (0-1000)
        total_reviews: Number of reviews received
        average_rating: Average rating (1-5)
        successful_cases: Number of successful completions
        
        # Services
        services_offered: List of services provided
        
        # Subscription
        subscription_status: Current subscription status
        subscription_expires: Subscription expiry date
        monthly_fee: Monthly subscription fee
        
        # Status
        is_featured: Whether provider is featured
        is_verified: Whether fully verified
        is_active: Whether currently active
        
        # Timestamps
        created_at: Registration timestamp
        updated_at: Last update timestamp
    """
    
    __tablename__ = "service_providers"
    
    id: str = ""
    user_id: str = ""
    provider_type: ProviderType = ProviderType.OTHER
    
    # Business Info
    business_name: str = ""
    business_license: Optional[str] = None
    registration_country: str = ""
    website: Optional[str] = None
    
    # Contact
    contact_email: str = ""
    contact_phone: str = ""
    address: str = ""
    
    # Trust & Reputation
    trust_score: float = 0.0
    total_reviews: int = 0
    average_rating: float = 0.0
    successful_cases: int = 0
    
    # Services
    services_offered: List[str] = []
    
    # Subscription
    subscription_status: SubscriptionStatus = SubscriptionStatus.TRIAL
    subscription_expires: Optional[datetime] = None
    monthly_fee: float = 10.0
    
    # Status
    is_featured: bool = False
    is_verified: bool = False
    is_active: bool = True
    
    # Timestamps
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    
    def __init__(self, **kwargs):
        self.services_offered = []
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self) -> str:
        return f"<ServiceProvider(id={self.id}, name={self.business_name}, type={self.provider_type})>"
    
    @property
    def is_subscription_active(self) -> bool:
        """Check if subscription is currently active."""
        if self.subscription_status not in [SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIAL]:
            return False
        if self.subscription_expires and datetime.utcnow() > self.subscription_expires:
            return False
        return True
    
    @property
    def can_be_featured(self) -> bool:
        """Check if provider qualifies for featured status."""
        return (
            self.is_verified and
            self.is_subscription_active and
            self.trust_score >= 700 and
            self.total_reviews >= 10 and
            self.average_rating >= 4.0
        )
