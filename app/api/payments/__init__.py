"""
Payments API Router
Payment and subscription endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.dependencies import get_current_active_user, get_admin_user
from app.models.user import User

router = APIRouter()


@router.get("/subscriptions/plans")
async def list_subscription_plans():
    """
    List available subscription plans.
    """
    return {
        "plans": [
            {
                "id": "agent",
                "name": "Agent Subscription",
                "price": 10.00,
                "currency": "USD",
                "billing_period": "monthly",
                "features": [
                    "Verified agent badge",
                    "Public trust score",
                    "Client messaging",
                    "Service listings",
                ],
            },
            {
                "id": "institution",
                "name": "Institution Subscription",
                "price": 10.00,
                "currency": "USD",
                "billing_period": "monthly",
                "features": [
                    "Verified institution badge",
                    "Student recruitment tools",
                    "Application management",
                ],
            },
            {
                "id": "provider",
                "name": "Service Provider Subscription",
                "price": 10.00,
                "currency": "USD",
                "billing_period": "monthly",
                "features": [
                    "Verified provider badge",
                    "Service listings",
                    "Client reviews",
                ],
            },
            {
                "id": "promotion",
                "name": "Service Promotion",
                "price": 20.00,
                "currency": "USD",
                "billing_period": "monthly",
                "features": [
                    "Featured placement",
                    "Priority in search",
                    "Analytics dashboard",
                ],
            },
        ]
    }


@router.get("/subscriptions/current")
async def get_current_subscription(
    current_user: User = Depends(get_current_active_user),
):
    """
    Get current user's subscription status.
    """
    return {
        "has_subscription": False,
        "plan": None,
        "status": None,
        "expires_at": None,
        "auto_renew": False,
    }


@router.post("/subscriptions/subscribe")
async def subscribe(
    plan_id: str,
    payment_method: str,
    current_user: User = Depends(get_current_active_user),
):
    """
    Subscribe to a plan.
    """
    return {
        "subscription_id": "sub_123",
        "plan_id": plan_id,
        "status": "active",
        "next_billing_date": "2024-02-01",
        "payment_url": "https://payment.gateway/checkout/abc",
    }


@router.post("/subscriptions/cancel")
async def cancel_subscription(
    current_user: User = Depends(get_current_active_user),
):
    """
    Cancel current subscription.
    """
    return {
        "message": "Subscription cancelled",
        "effective_until": "2024-01-31",
    }


@router.get("/transactions")
async def list_transactions(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_active_user),
):
    """
    List user's transaction history.
    """
    return {
        "transactions": [],
        "total": 0,
        "page": page,
    }


@router.get("/transactions/{transaction_id}")
async def get_transaction(
    transaction_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """
    Get transaction details.
    """
    return {
        "id": transaction_id,
        "amount": 10.00,
        "currency": "USD",
        "status": "completed",
    }


@router.get("/transactions/{transaction_id}/receipt")
async def get_receipt(
    transaction_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """
    Get transaction receipt/invoice.
    """
    return {
        "receipt_url": f"https://api.globaltrusthub.com/receipts/{transaction_id}.pdf",
    }


@router.post("/transactions/{transaction_id}/refund")
async def request_refund(
    transaction_id: str,
    reason: str,
    current_user: User = Depends(get_current_active_user),
):
    """
    Request a refund for a transaction.
    """
    return {
        "refund_request_id": "refund_123",
        "status": "pending",
        "message": "Refund request submitted for review",
    }


# Webhook for payment gateway
@router.post("/webhooks/stripe")
async def stripe_webhook():
    """
    Stripe payment webhook handler.
    """
    return {"received": True}


@router.post("/webhooks/jazzcash")
async def jazzcash_webhook():
    """
    JazzCash payment webhook handler.
    """
    return {"received": True}


# Admin endpoints

@router.get("/admin/revenue")
async def get_revenue_stats(
    period: str = Query("month"),
    admin_user: User = Depends(get_admin_user),
):
    """
    Get revenue statistics (admin only).
    """
    return {
        "period": period,
        "total_revenue": 0.0,
        "subscription_revenue": 0.0,
        "promotion_revenue": 0.0,
        "active_subscriptions": 0,
    }
