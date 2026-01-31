"""
Audit Service
Audit logging for security and compliance.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class AuditAction(str, Enum):
    """Types of auditable actions."""
    # Authentication
    LOGIN = "login"
    LOGOUT = "logout"
    LOGIN_FAILED = "login_failed"
    PASSWORD_CHANGE = "password_change"
    PASSWORD_RESET = "password_reset"
    
    # User Management
    USER_CREATE = "user_create"
    USER_UPDATE = "user_update"
    USER_DELETE = "user_delete"
    USER_BAN = "user_ban"
    USER_UNBAN = "user_unban"
    
    # Verification
    DOCUMENT_UPLOAD = "document_upload"
    DOCUMENT_VERIFY = "document_verify"
    DOCUMENT_REJECT = "document_reject"
    VERIFICATION_LEVEL_CHANGE = "verification_level_change"
    
    # Trust Score
    TRUST_SCORE_UPDATE = "trust_score_update"
    TRUST_SCORE_MANUAL_ADJUST = "trust_score_manual_adjust"
    
    # Financial
    SUBSCRIPTION_START = "subscription_start"
    SUBSCRIPTION_CANCEL = "subscription_cancel"
    PAYMENT_SUCCESS = "payment_success"
    PAYMENT_FAILED = "payment_failed"
    REFUND_REQUEST = "refund_request"
    REFUND_PROCESSED = "refund_processed"
    
    # Content
    REVIEW_CREATE = "review_create"
    REVIEW_DELETE = "review_delete"
    REVIEW_MODERATE = "review_moderate"
    SERVICE_CREATE = "service_create"
    SERVICE_UPDATE = "service_update"
    
    # Safety
    REPORT_SUBMIT = "report_submit"
    REPORT_RESOLVE = "report_resolve"
    FRAUD_ALERT = "fraud_alert"
    CONVERSATION_FREEZE = "conversation_freeze"
    
    # Admin
    ADMIN_ACTION = "admin_action"
    SYSTEM_CONFIG_CHANGE = "system_config_change"


class AuditService:
    """
    Service for recording audit logs.
    Critical for security, compliance, and dispute resolution.
    """
    
    def __init__(self):
        self.logger = logging.getLogger("audit")
    
    async def log(
        self,
        action: AuditAction,
        user_id: Optional[str] = None,
        target_id: Optional[str] = None,
        target_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        request_id: Optional[str] = None,
    ) -> str:
        """
        Record an audit log entry.
        
        Returns:
            str: Audit log entry ID
        """
        entry_id = f"audit_{datetime.utcnow().timestamp()}"
        
        log_entry = {
            "id": entry_id,
            "timestamp": datetime.utcnow().isoformat(),
            "action": action.value,
            "user_id": user_id,
            "target_id": target_id,
            "target_type": target_type,
            "details": details or {},
            "ip_address": ip_address,
            "user_agent": user_agent,
            "request_id": request_id,
        }
        
        # Log to structured logger
        self.logger.info(f"AUDIT: {log_entry}")
        
        # In production: store in database
        
        return entry_id
    
    async def log_login(
        self,
        user_id: str,
        success: bool,
        ip_address: str,
        user_agent: str,
        failure_reason: Optional[str] = None,
    ) -> str:
        """Log login attempt."""
        action = AuditAction.LOGIN if success else AuditAction.LOGIN_FAILED
        
        return await self.log(
            action=action,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details={"failure_reason": failure_reason} if failure_reason else None,
        )
    
    async def log_verification_action(
        self,
        action: AuditAction,
        user_id: str,
        document_id: str,
        admin_id: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> str:
        """Log verification-related action."""
        return await self.log(
            action=action,
            user_id=admin_id or user_id,
            target_id=document_id,
            target_type="document",
            details={
                "affected_user": user_id,
                "notes": notes,
            },
        )
    
    async def log_trust_score_change(
        self,
        user_id: str,
        old_score: float,
        new_score: float,
        reason: str,
        admin_id: Optional[str] = None,
    ) -> str:
        """Log trust score change."""
        action = (
            AuditAction.TRUST_SCORE_MANUAL_ADJUST
            if admin_id
            else AuditAction.TRUST_SCORE_UPDATE
        )
        
        return await self.log(
            action=action,
            user_id=admin_id or user_id,
            target_id=user_id,
            target_type="user",
            details={
                "old_score": old_score,
                "new_score": new_score,
                "change": new_score - old_score,
                "reason": reason,
            },
        )
    
    async def log_payment(
        self,
        user_id: str,
        transaction_id: str,
        amount: float,
        currency: str,
        success: bool,
        error: Optional[str] = None,
    ) -> str:
        """Log payment transaction."""
        action = AuditAction.PAYMENT_SUCCESS if success else AuditAction.PAYMENT_FAILED
        
        return await self.log(
            action=action,
            user_id=user_id,
            target_id=transaction_id,
            target_type="transaction",
            details={
                "amount": amount,
                "currency": currency,
                "error": error,
            },
        )
    
    async def log_fraud_alert(
        self,
        user_id: str,
        alert_type: str,
        severity: str,
        details: Dict[str, Any],
    ) -> str:
        """Log fraud detection alert."""
        return await self.log(
            action=AuditAction.FRAUD_ALERT,
            user_id=user_id,
            details={
                "alert_type": alert_type,
                "severity": severity,
                **details,
            },
        )
    
    async def get_user_audit_trail(
        self,
        user_id: str,
        actions: Optional[List[AuditAction]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get audit trail for a user."""
        # In production: query from database
        return []
    
    async def get_system_audit_logs(
        self,
        actions: Optional[List[AuditAction]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get system-wide audit logs (admin only)."""
        # In production: query from database
        return []


# Global audit service instance
audit_service = AuditService()
