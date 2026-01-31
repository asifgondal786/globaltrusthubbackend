"""
Scam Language Analysis - Alerts
Alert generation for detected scam attempts.
"""

from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class AlertSeverity(str, Enum):
    """Alert severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertType(str, Enum):
    """Types of scam alerts."""
    SCAM_MESSAGE = "scam_message"
    SUSPICIOUS_PATTERN = "suspicious_pattern"
    REPEAT_OFFENDER = "repeat_offender"
    MASS_MESSAGING = "mass_messaging"
    FAKE_DOCUMENT = "fake_document"
    IMPERSONATION = "impersonation"


class ScamAlert:
    """Represents a scam detection alert."""
    
    def __init__(
        self,
        alert_type: AlertType,
        severity: AlertSeverity,
        user_id: str,
        target_id: Optional[str] = None,
        details: Optional[Dict] = None,
    ):
        self.id = f"alert_{datetime.utcnow().timestamp()}"
        self.alert_type = alert_type
        self.severity = severity
        self.user_id = user_id
        self.target_id = target_id
        self.details = details or {}
        self.created_at = datetime.utcnow()
        self.resolved = False
        self.resolved_at = None
        self.resolved_by = None
        self.resolution_notes = None
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "alert_type": self.alert_type.value,
            "severity": self.severity.value,
            "user_id": self.user_id,
            "target_id": self.target_id,
            "details": self.details,
            "created_at": self.created_at.isoformat(),
            "resolved": self.resolved,
        }


class AlertManager:
    """
    Manage scam detection alerts.
    """
    
    def __init__(self):
        self.alerts: List[ScamAlert] = []
        self.alert_counts: Dict[str, int] = {}  # user_id -> count
    
    def create_alert(
        self,
        alert_type: AlertType,
        user_id: str,
        scam_score: float,
        details: Dict,
        target_id: Optional[str] = None,
    ) -> ScamAlert:
        """
        Create a new alert based on detection results.
        """
        # Determine severity based on score and history
        user_history = self.alert_counts.get(user_id, 0)
        
        if scam_score >= 0.8 or user_history >= 3:
            severity = AlertSeverity.CRITICAL
        elif scam_score >= 0.6 or user_history >= 2:
            severity = AlertSeverity.HIGH
        elif scam_score >= 0.4:
            severity = AlertSeverity.MEDIUM
        else:
            severity = AlertSeverity.LOW
        
        alert = ScamAlert(
            alert_type=alert_type,
            severity=severity,
            user_id=user_id,
            target_id=target_id,
            details={
                "scam_score": scam_score,
                "previous_alerts": user_history,
                **details,
            },
        )
        
        # Store alert
        self.alerts.append(alert)
        self.alert_counts[user_id] = user_history + 1
        
        # Log alert
        logger.warning(
            f"SCAM ALERT [{severity.value.upper()}]: "
            f"Type={alert_type.value}, User={user_id}, Score={scam_score:.2f}"
        )
        
        # Trigger notifications for high severity
        if severity in [AlertSeverity.HIGH, AlertSeverity.CRITICAL]:
            self._send_notifications(alert)
        
        return alert
    
    def _send_notifications(self, alert: ScamAlert):
        """Send notifications for high-severity alerts."""
        # In production: notify admins, pause user actions, etc.
        logger.info(f"Sending notifications for alert {alert.id}")
    
    def resolve_alert(
        self,
        alert_id: str,
        resolved_by: str,
        notes: str,
        action_taken: str,
    ) -> Optional[ScamAlert]:
        """
        Resolve an alert.
        """
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.resolved = True
                alert.resolved_at = datetime.utcnow()
                alert.resolved_by = resolved_by
                alert.resolution_notes = notes
                alert.details["action_taken"] = action_taken
                
                logger.info(f"Alert {alert_id} resolved by {resolved_by}: {action_taken}")
                return alert
        
        return None
    
    def get_pending_alerts(
        self,
        severity: Optional[AlertSeverity] = None,
        limit: int = 50,
    ) -> List[ScamAlert]:
        """Get unresolved alerts."""
        pending = [a for a in self.alerts if not a.resolved]
        
        if severity:
            pending = [a for a in pending if a.severity == severity]
        
        # Sort by severity and time
        severity_order = {
            AlertSeverity.CRITICAL: 0,
            AlertSeverity.HIGH: 1,
            AlertSeverity.MEDIUM: 2,
            AlertSeverity.LOW: 3,
        }
        pending.sort(key=lambda a: (severity_order[a.severity], a.created_at))
        
        return pending[:limit]
    
    def get_user_alerts(
        self,
        user_id: str,
        include_resolved: bool = False,
    ) -> List[ScamAlert]:
        """Get alerts for a specific user."""
        user_alerts = [a for a in self.alerts if a.user_id == user_id]
        
        if not include_resolved:
            user_alerts = [a for a in user_alerts if not a.resolved]
        
        return user_alerts
    
    def get_statistics(self) -> Dict:
        """Get alert statistics."""
        total = len(self.alerts)
        resolved = sum(1 for a in self.alerts if a.resolved)
        pending = total - resolved
        
        by_severity = {}
        by_type = {}
        
        for alert in self.alerts:
            sev = alert.severity.value
            by_severity[sev] = by_severity.get(sev, 0) + 1
            
            typ = alert.alert_type.value
            by_type[typ] = by_type.get(typ, 0) + 1
        
        return {
            "total": total,
            "resolved": resolved,
            "pending": pending,
            "by_severity": by_severity,
            "by_type": by_type,
            "repeat_offenders": sum(1 for c in self.alert_counts.values() if c >= 3),
        }
    
    def should_auto_block(self, user_id: str) -> bool:
        """
        Determine if user should be auto-blocked.
        """
        user_alerts = self.get_user_alerts(user_id, include_resolved=True)
        
        # Auto-block conditions
        critical_count = sum(
            1 for a in user_alerts
            if a.severity == AlertSeverity.CRITICAL
        )
        
        recent_high = sum(
            1 for a in user_alerts
            if a.severity in [AlertSeverity.HIGH, AlertSeverity.CRITICAL]
            and (datetime.utcnow() - a.created_at).days < 7
        )
        
        return critical_count >= 2 or recent_high >= 3


# Global alert manager instance
alert_manager = AlertManager()
