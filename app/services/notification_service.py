"""
Notification Service
Push notifications and in-app notifications.
"""

from typing import List, Optional, Dict, Any
import logging
from enum import Enum

from app.config import settings

logger = logging.getLogger(__name__)


class NotificationType(str, Enum):
    """Types of notifications."""
    VERIFICATION_UPDATE = "verification_update"
    NEW_MESSAGE = "new_message"
    NEW_REVIEW = "new_review"
    TRUST_SCORE_CHANGE = "trust_score_change"
    PAYMENT_SUCCESS = "payment_success"
    PAYMENT_FAILED = "payment_failed"
    SUBSCRIPTION_EXPIRING = "subscription_expiring"
    SCAM_WARNING = "scam_warning"
    SYSTEM_ALERT = "system_alert"


class NotificationService:
    """
    Service for sending push and in-app notifications.
    """
    
    def __init__(self):
        self.firebase_initialized = False
        self._init_firebase()
    
    def _init_firebase(self):
        """Initialize Firebase for push notifications."""
        if settings.FIREBASE_CREDENTIALS_PATH:
            try:
                # In production: initialize firebase_admin
                self.firebase_initialized = True
                logger.info("Firebase initialized for push notifications")
            except Exception as e:
                logger.warning(f"Firebase initialization failed: {e}")
    
    async def send_push_notification(
        self,
        user_id: str,
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Send push notification to user's devices.
        
        Args:
            user_id: Target user ID
            title: Notification title
            body: Notification body text
            data: Additional data payload
        
        Returns:
            bool: True if sent successfully
        """
        if settings.DEBUG:
            logger.info(f"[DEV] Push to {user_id}: {title} - {body}")
            return True
        
        if not self.firebase_initialized:
            logger.warning("Firebase not initialized, skipping push")
            return False
        
        # In production: send via Firebase Cloud Messaging
        try:
            logger.info(f"Sending push to {user_id}: {title}")
            return True
        except Exception as e:
            logger.error(f"Push notification failed: {e}")
            return False
    
    async def send_in_app_notification(
        self,
        user_id: str,
        notification_type: NotificationType,
        title: str,
        message: str,
        action_url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Create an in-app notification.
        
        Returns:
            str: Notification ID
        """
        notification_id = f"notif_{user_id}_{notification_type.value}"
        
        # In production: store in database
        logger.info(f"In-app notification for {user_id}: {title}")
        
        return notification_id
    
    async def notify_verification_update(
        self,
        user_id: str,
        status: str,
        document_type: str = None,
    ) -> None:
        """Send verification status update notification."""
        title = "Verification Update"
        body = f"Your {document_type or 'document'} verification status: {status}"
        
        await self.send_push_notification(user_id, title, body)
        await self.send_in_app_notification(
            user_id,
            NotificationType.VERIFICATION_UPDATE,
            title,
            body,
            action_url="/verification/status",
        )
    
    async def notify_new_message(
        self,
        user_id: str,
        sender_name: str,
        room_id: str,
        preview: str,
    ) -> None:
        """Send new message notification."""
        title = f"New message from {sender_name}"
        body = preview[:100] + "..." if len(preview) > 100 else preview
        
        await self.send_push_notification(
            user_id,
            title,
            body,
            data={"room_id": room_id},
        )
    
    async def notify_trust_score_change(
        self,
        user_id: str,
        old_score: float,
        new_score: float,
        reason: str,
    ) -> None:
        """Send trust score change notification."""
        change = new_score - old_score
        direction = "increased" if change > 0 else "decreased"
        
        title = f"Trust Score {direction.title()}"
        body = f"Your trust score has {direction} from {old_score:.0f} to {new_score:.0f}. {reason}"
        
        await self.send_in_app_notification(
            user_id,
            NotificationType.TRUST_SCORE_CHANGE,
            title,
            body,
            action_url="/profile/trust-score",
        )
    
    async def notify_scam_warning(
        self,
        user_id: str,
        context: str,
        details: str,
    ) -> None:
        """Send scam warning notification."""
        title = "⚠️ Potential Scam Detected"
        body = f"We detected suspicious activity: {details}"
        
        await self.send_push_notification(user_id, title, body)
        await self.send_in_app_notification(
            user_id,
            NotificationType.SCAM_WARNING,
            title,
            body,
            metadata={"context": context},
        )
    
    async def get_user_notifications(
        self,
        user_id: str,
        unread_only: bool = False,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """Get user's notifications."""
        # In production: fetch from database
        return []
    
    async def mark_as_read(
        self,
        user_id: str,
        notification_ids: List[str],
    ) -> int:
        """Mark notifications as read. Returns count marked."""
        # In production: update in database
        return len(notification_ids)


# Global notification service instance
notification_service = NotificationService()
