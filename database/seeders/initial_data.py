"""
Database Seeders - Initial Data
Seed initial data for development and testing.
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
import json


def get_admin_users() -> List[Dict[str, Any]]:
    """Get initial admin users."""
    return [
        {
            "email": "admin@globaltrusthub.com",
            "full_name": "System Administrator",
            "role": "admin",
            "is_verified": True,
            "verification_status": "level_3",
            "trust_score": 1000,
        },
        {
            "email": "moderator@globaltrusthub.com",
            "full_name": "Content Moderator",
            "role": "moderator",
            "is_verified": True,
            "verification_status": "level_2",
            "trust_score": 900,
        },
    ]


def get_sample_service_categories() -> List[Dict[str, Any]]:
    """Get service categories."""
    return [
        {"id": "university", "name": "Universities", "description": "Higher education institutions"},
        {"id": "agent", "name": "Education Agents", "description": "Study abroad consultants"},
        {"id": "employer", "name": "Employers", "description": "Job providers"},
        {"id": "housing", "name": "Housing", "description": "Accommodation services"},
        {"id": "financial", "name": "Financial Services", "description": "Banks and money transfer"},
        {"id": "travel", "name": "Travel", "description": "Travel and transport services"},
        {"id": "legal", "name": "Legal Services", "description": "Immigration lawyers and consultants"},
    ]


def get_sample_countries() -> List[Dict[str, Any]]:
    """Get supported countries."""
    return [
        {"code": "PK", "name": "Pakistan", "is_source": True},
        {"code": "GB", "name": "United Kingdom", "is_destination": True},
        {"code": "US", "name": "United States", "is_destination": True},
        {"code": "CA", "name": "Canada", "is_destination": True},
        {"code": "AU", "name": "Australia", "is_destination": True},
        {"code": "DE", "name": "Germany", "is_destination": True},
        {"code": "AE", "name": "United Arab Emirates", "is_destination": True},
    ]


def get_verification_levels() -> List[Dict[str, Any]]:
    """Get verification level definitions."""
    return [
        {
            "level": 0,
            "name": "Unverified",
            "requirements": [],
            "permissions": ["browse", "view_public_profiles"],
        },
        {
            "level": 1,
            "name": "Basic",
            "requirements": ["email_verified", "phone_verified"],
            "permissions": ["send_messages", "submit_applications"],
        },
        {
            "level": 2,
            "name": "Standard",
            "requirements": ["cnic_verified", "address_verified"],
            "permissions": ["submit_reviews", "access_all_features"],
        },
        {
            "level": 3,
            "name": "Premium",
            "requirements": ["passport_verified", "criminal_check"],
            "permissions": ["priority_support", "verified_badge"],
        },
    ]


def get_subscription_plans() -> List[Dict[str, Any]]:
    """Get subscription plan definitions."""
    return [
        {
            "id": "agent_monthly",
            "name": "Agent Monthly",
            "price": 10.00,
            "currency": "USD",
            "billing_period": "monthly",
            "target_role": "agent",
            "features": [
                "Verified agent badge",
                "Public trust score",
                "Unlimited client messaging",
                "Service listings",
            ],
        },
        {
            "id": "institution_monthly",
            "name": "Institution Monthly",
            "price": 10.00,
            "currency": "USD",
            "billing_period": "monthly",
            "target_role": "institution",
            "features": [
                "Verified institution badge",
                "Student recruitment tools",
                "Application management",
            ],
        },
        {
            "id": "provider_monthly",
            "name": "Service Provider Monthly",
            "price": 10.00,
            "currency": "USD",
            "billing_period": "monthly",
            "target_role": "service_provider",
            "features": [
                "Verified provider badge",
                "Service listings",
                "Client reviews",
            ],
        },
        {
            "id": "promotion_monthly",
            "name": "Service Promotion",
            "price": 20.00,
            "currency": "USD",
            "billing_period": "monthly",
            "target_role": "any_paid",
            "features": [
                "Featured placement",
                "Priority in search",
                "Analytics dashboard",
            ],
        },
    ]


async def seed_database(db_session) -> Dict[str, int]:
    """
    Run all seeders.
    
    Returns counts of seeded records.
    """
    counts = {}
    
    # In production: insert into database
    # For now, just return what would be seeded
    
    counts["admin_users"] = len(get_admin_users())
    counts["categories"] = len(get_sample_service_categories())
    counts["countries"] = len(get_sample_countries())
    counts["verification_levels"] = len(get_verification_levels())
    counts["subscription_plans"] = len(get_subscription_plans())
    
    return counts


if __name__ == "__main__":
    # Print sample data for verification
    print("Admin Users:", json.dumps(get_admin_users(), indent=2))
    print("\nCategories:", json.dumps(get_sample_service_categories(), indent=2))
