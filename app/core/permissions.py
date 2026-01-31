"""
Permissions Module
Role-based access control (RBAC) for GlobalTrustHub.
"""

from enum import Enum
from typing import List, Optional
from functools import wraps
from fastapi import HTTPException, status


class UserRole(str, Enum):
    """User roles in the system."""
    STUDENT = "student"
    JOB_SEEKER = "job_seeker"
    AGENT = "agent"
    INSTITUTION = "institution"
    SERVICE_PROVIDER = "service_provider"
    ADMIN = "admin"
    MODERATOR = "moderator"


class Permission(str, Enum):
    """System permissions."""
    # User permissions
    VIEW_PROFILE = "view_profile"
    EDIT_PROFILE = "edit_profile"
    DELETE_ACCOUNT = "delete_account"
    
    # Verification permissions
    SUBMIT_VERIFICATION = "submit_verification"
    VIEW_VERIFICATION_STATUS = "view_verification_status"
    
    # Chat permissions
    SEND_MESSAGE = "send_message"
    VIEW_CHAT_HISTORY = "view_chat_history"
    
    # Review permissions
    SUBMIT_REVIEW = "submit_review"
    VIEW_REVIEWS = "view_reviews"
    
    # Service permissions
    LIST_SERVICES = "list_services"
    CREATE_SERVICE = "create_service"
    MANAGE_SERVICES = "manage_services"
    
    # Admin permissions
    MANAGE_USERS = "manage_users"
    MANAGE_VERIFICATIONS = "manage_verifications"
    VIEW_ANALYTICS = "view_analytics"
    MANAGE_SYSTEM = "manage_system"
    BAN_USER = "ban_user"
    
    # Payment permissions
    PROCESS_PAYMENT = "process_payment"
    VIEW_TRANSACTIONS = "view_transactions"


# Role-Permission mapping
ROLE_PERMISSIONS: dict[UserRole, List[Permission]] = {
    UserRole.STUDENT: [
        Permission.VIEW_PROFILE,
        Permission.EDIT_PROFILE,
        Permission.SUBMIT_VERIFICATION,
        Permission.VIEW_VERIFICATION_STATUS,
        Permission.SEND_MESSAGE,
        Permission.VIEW_CHAT_HISTORY,
        Permission.SUBMIT_REVIEW,
        Permission.VIEW_REVIEWS,
        Permission.LIST_SERVICES,
    ],
    UserRole.JOB_SEEKER: [
        Permission.VIEW_PROFILE,
        Permission.EDIT_PROFILE,
        Permission.SUBMIT_VERIFICATION,
        Permission.VIEW_VERIFICATION_STATUS,
        Permission.SEND_MESSAGE,
        Permission.VIEW_CHAT_HISTORY,
        Permission.SUBMIT_REVIEW,
        Permission.VIEW_REVIEWS,
        Permission.LIST_SERVICES,
    ],
    UserRole.AGENT: [
        Permission.VIEW_PROFILE,
        Permission.EDIT_PROFILE,
        Permission.SUBMIT_VERIFICATION,
        Permission.VIEW_VERIFICATION_STATUS,
        Permission.SEND_MESSAGE,
        Permission.VIEW_CHAT_HISTORY,
        Permission.VIEW_REVIEWS,
        Permission.LIST_SERVICES,
        Permission.CREATE_SERVICE,
        Permission.MANAGE_SERVICES,
        Permission.PROCESS_PAYMENT,
        Permission.VIEW_TRANSACTIONS,
    ],
    UserRole.INSTITUTION: [
        Permission.VIEW_PROFILE,
        Permission.EDIT_PROFILE,
        Permission.SUBMIT_VERIFICATION,
        Permission.VIEW_VERIFICATION_STATUS,
        Permission.SEND_MESSAGE,
        Permission.VIEW_CHAT_HISTORY,
        Permission.VIEW_REVIEWS,
        Permission.LIST_SERVICES,
        Permission.CREATE_SERVICE,
        Permission.MANAGE_SERVICES,
        Permission.PROCESS_PAYMENT,
        Permission.VIEW_TRANSACTIONS,
    ],
    UserRole.SERVICE_PROVIDER: [
        Permission.VIEW_PROFILE,
        Permission.EDIT_PROFILE,
        Permission.SUBMIT_VERIFICATION,
        Permission.VIEW_VERIFICATION_STATUS,
        Permission.SEND_MESSAGE,
        Permission.VIEW_CHAT_HISTORY,
        Permission.VIEW_REVIEWS,
        Permission.LIST_SERVICES,
        Permission.CREATE_SERVICE,
        Permission.MANAGE_SERVICES,
        Permission.PROCESS_PAYMENT,
        Permission.VIEW_TRANSACTIONS,
    ],
    UserRole.MODERATOR: [
        Permission.VIEW_PROFILE,
        Permission.MANAGE_USERS,
        Permission.MANAGE_VERIFICATIONS,
        Permission.VIEW_REVIEWS,
        Permission.BAN_USER,
    ],
    UserRole.ADMIN: [
        # Admins have all permissions
        *list(Permission),
    ],
}


def has_permission(role: UserRole, permission: Permission) -> bool:
    """
    Check if a role has a specific permission.
    
    Args:
        role: User role to check
        permission: Permission to verify
    
    Returns:
        bool: True if role has permission
    """
    return permission in ROLE_PERMISSIONS.get(role, [])


def get_role_permissions(role: UserRole) -> List[Permission]:
    """
    Get all permissions for a role.
    
    Args:
        role: User role
    
    Returns:
        List[Permission]: List of permissions for the role
    """
    return ROLE_PERMISSIONS.get(role, [])


def require_permission(permission: Permission):
    """
    Decorator to require a specific permission for a route.
    
    Args:
        permission: Required permission
    
    Usage:
        @require_permission(Permission.MANAGE_USERS)
        async def admin_route():
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get current user from kwargs (injected by dependency)
            current_user = kwargs.get("current_user")
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required",
                )
            
            if not has_permission(current_user.role, permission):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission denied: {permission.value}",
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def require_roles(allowed_roles: List[UserRole]):
    """
    Decorator to require specific roles for a route.
    
    Args:
        allowed_roles: List of allowed roles
    
    Usage:
        @require_roles([UserRole.ADMIN, UserRole.MODERATOR])
        async def admin_route():
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get("current_user")
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required",
                )
            
            if current_user.role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied for your role",
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator
