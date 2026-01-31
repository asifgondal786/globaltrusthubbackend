"""
Admin API Router
Administrative endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, Query

from app.dependencies import get_admin_user
from app.models.user import User

router = APIRouter()


@router.get("/dashboard")
async def admin_dashboard(admin_user: User = Depends(get_admin_user)):
    """
    Get admin dashboard statistics.
    """
    return {
        "users": {
            "total": 0,
            "active": 0,
            "verified": 0,
            "banned": 0,
            "new_today": 0,
        },
        "verifications": {
            "pending": 0,
            "completed_today": 0,
        },
        "reviews": {
            "pending_moderation": 0,
            "reported": 0,
        },
        "revenue": {
            "today": 0.0,
            "this_month": 0.0,
        },
        "system": {
            "status": "healthy",
            "uptime": "99.9%",
        },
    }


@router.get("/users")
async def list_all_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    role: str = Query(None),
    verification_status: str = Query(None),
    search: str = Query(None),
    admin_user: User = Depends(get_admin_user),
):
    """
    List all users with filters.
    """
    return {
        "users": [],
        "total": 0,
        "page": page,
    }


@router.get("/users/{user_id}")
async def get_user_details(
    user_id: str,
    admin_user: User = Depends(get_admin_user),
):
    """
    Get detailed user information.
    """
    return {
        "id": user_id,
        "email": "user@example.com",
        "full_details": True,
    }


@router.get("/fraud-alerts")
async def list_fraud_alerts(
    page: int = Query(1, ge=1),
    severity: str = Query(None, description="low, medium, high, critical"),
    admin_user: User = Depends(get_admin_user),
):
    """
    List AI-detected fraud alerts.
    """
    return {
        "alerts": [],
        "total": 0,
        "page": page,
    }


@router.post("/fraud-alerts/{alert_id}/resolve")
async def resolve_fraud_alert(
    alert_id: str,
    action: str,
    notes: str = None,
    admin_user: User = Depends(get_admin_user),
):
    """
    Resolve a fraud alert.
    """
    return {
        "message": f"Alert {alert_id} resolved with action: {action}",
        "resolved_by": admin_user.id,
    }


@router.get("/disputes")
async def list_disputes(
    page: int = Query(1, ge=1),
    status: str = Query(None),
    admin_user: User = Depends(get_admin_user),
):
    """
    List active disputes.
    """
    return {
        "disputes": [],
        "total": 0,
        "page": page,
    }


@router.post("/disputes/{dispute_id}/resolve")
async def resolve_dispute(
    dispute_id: str,
    resolution: str,
    notes: str,
    admin_user: User = Depends(get_admin_user),
):
    """
    Resolve a dispute.
    """
    return {
        "message": f"Dispute {dispute_id} resolved",
        "resolution": resolution,
        "resolved_by": admin_user.id,
    }


@router.get("/audit-logs")
async def get_audit_logs(
    page: int = Query(1, ge=1),
    action_type: str = Query(None),
    user_id: str = Query(None),
    admin_user: User = Depends(get_admin_user),
):
    """
    Get system audit logs.
    """
    return {
        "logs": [],
        "total": 0,
        "page": page,
    }


@router.get("/banned-providers")
async def list_banned_providers(admin_user: User = Depends(get_admin_user)):
    """
    List banned service providers (for public transparency).
    """
    return {
        "banned_providers": [],
        "total": 0,
    }


@router.get("/statistics/fraud")
async def fraud_statistics(admin_user: User = Depends(get_admin_user)):
    """
    Get fraud statistics (for public transparency).
    """
    return {
        "total_fraud_cases": 0,
        "cases_this_month": 0,
        "amount_prevented": 0.0,
        "detection_rate": "99%",
    }


@router.post("/system/maintenance")
async def toggle_maintenance_mode(
    enabled: bool,
    message: str = None,
    admin_user: User = Depends(get_admin_user),
):
    """
    Toggle system maintenance mode.
    """
    return {
        "maintenance_mode": enabled,
        "message": message,
    }
