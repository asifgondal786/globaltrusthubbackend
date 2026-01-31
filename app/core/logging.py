"""
Logging Module
Structured logging setup for GlobalTrustHub.
"""

import logging
import os
import sys
from datetime import datetime
from typing import Optional
import json

from app.config import settings


class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging.
    Outputs logs in JSON format for easy parsing.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        if hasattr(record, "action"):
            log_data["action"] = record.action
        
        return json.dumps(log_data)


class ColoredFormatter(logging.Formatter):
    """
    Colored formatter for console output during development.
    """
    
    COLORS = {
        "DEBUG": "\033[36m",    # Cyan
        "INFO": "\033[32m",     # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",    # Red
        "CRITICAL": "\033[35m", # Magenta
        "RESET": "\033[0m",     # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        reset = self.COLORS["RESET"]
        
        # Format timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Build formatted message
        formatted = (
            f"{color}[{timestamp}] "
            f"{record.levelname:8} "
            f"{reset}{record.name}: "
            f"{record.getMessage()}"
        )
        
        if record.exc_info:
            formatted += f"\n{self.formatException(record.exc_info)}"
        
        return formatted


def setup_logging(log_level: Optional[str] = None) -> None:
    """
    Configure application logging.
    
    Args:
        log_level: Optional log level override (DEBUG, INFO, WARNING, ERROR)
    """
    level = log_level or ("DEBUG" if settings.DEBUG else "INFO")
    
    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Clear existing handlers
    root_logger.handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Use colored formatter for development, JSON for production
    if settings.DEBUG:
        console_handler.setFormatter(ColoredFormatter())
    else:
        console_handler.setFormatter(JSONFormatter())
    
    root_logger.addHandler(console_handler)
    
    # File handler for production
    if not settings.DEBUG:
        os.makedirs("logs", exist_ok=True)
        file_handler = logging.FileHandler("logs/app.log")
        file_handler.setLevel(level)
        file_handler.setFormatter(JSONFormatter())
        root_logger.addHandler(file_handler)
    
    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name.
    
    Args:
        name: Logger name (typically __name__)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)


class AuditLogger:
    """
    Audit logger for security and compliance events.
    Logs important user actions and system events.
    """
    
    def __init__(self):
        self.logger = logging.getLogger("audit")
    
    def log_action(
        self,
        action: str,
        user_id: str,
        details: dict,
        request_id: Optional[str] = None,
    ) -> None:
        """
        Log an auditable action.
        
        Args:
            action: Action type (e.g., "login", "verification_submit")
            user_id: User performing the action
            details: Additional action details
            request_id: Optional request correlation ID
        """
        extra = {
            "user_id": user_id,
            "action": action,
            "request_id": request_id,
        }
        self.logger.info(
            f"AUDIT: {action} by user {user_id} - {details}",
            extra=extra,
        )
    
    def log_security_event(
        self,
        event_type: str,
        details: dict,
        severity: str = "warning",
    ) -> None:
        """
        Log a security-related event.
        
        Args:
            event_type: Type of security event
            details: Event details
            severity: Event severity level
        """
        log_method = getattr(self.logger, severity, self.logger.warning)
        log_method(f"SECURITY: {event_type} - {details}")


# Global audit logger instance
audit_logger = AuditLogger()
