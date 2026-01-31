"""
Email Service
Email sending functionality.
"""

from typing import List, Optional
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """
    Service for sending emails.
    Uses SMTP when credentials are configured, otherwise logs.
    """
    
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.EMAIL_FROM
        self._has_smtp_credentials = bool(self.smtp_user and self.smtp_password)
    
    async def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None,
    ) -> bool:
        """
        Send an email.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Plain text body
            html_body: Optional HTML body
        
        Returns:
            bool: True if sent successfully
        """
        # If no SMTP credentials configured, just log and return
        if not self._has_smtp_credentials:
            logger.info(f"[NO SMTP] Email would be sent to {to}")
            logger.info(f"[NO SMTP] Subject: {subject}")
            logger.info(f"[NO SMTP] Body:\n{body}")
            return True
        
        # Send actual email using SMTP
        try:
            import aiosmtplib
            
            # Create message
            message = MIMEMultipart("alternative")
            message["From"] = self.from_email
            message["To"] = to
            message["Subject"] = subject
            
            # Add plain text part
            message.attach(MIMEText(body, "plain"))
            
            # Add HTML part if provided
            if html_body:
                message.attach(MIMEText(html_body, "html"))
            
            # Send email
            await aiosmtplib.send(
                message,
                hostname=self.smtp_host,
                port=self.smtp_port,
                username=self.smtp_user,
                password=self.smtp_password,
                start_tls=True,
            )
            
            logger.info(f"✅ Email sent successfully to {to}: {subject}")
            return True
            
        except ImportError:
            logger.error("aiosmtplib not installed. Run: pip install aiosmtplib")
            logger.info(f"[FALLBACK] Email to {to}: {subject}")
            logger.info(f"[FALLBACK] Body:\n{body}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to send email to {to}: {e}")
            return False
    
    async def send_verification_email(self, email: str, token: str) -> bool:
        """Send email verification link."""
        verification_url = f"https://globaltrusthub.com/verify-email?token={token}"
        
        subject = "Verify Your GlobalTrustHub Email"
        body = f"""
Welcome to GlobalTrustHub!

Please verify your email by clicking the link below:
{verification_url}

This link expires in 24 hours.

If you didn't create an account, please ignore this email.

Best regards,
GlobalTrustHub Team
        """
        
        return await self.send_email(email, subject, body)
    
    async def send_password_reset_email(self, email: str, token: str) -> bool:
        """Send password reset link."""
        reset_url = f"https://globaltrusthub.com/reset-password?token={token}"
        
        subject = "Reset Your GlobalTrustHub Password"
        body = f"""
You requested a password reset for your GlobalTrustHub account.

Click the link below to reset your password:
{reset_url}

This link expires in 1 hour.

If you didn't request this, please ignore this email or contact support.

Best regards,
GlobalTrustHub Team
        """
        
        return await self.send_email(email, subject, body)
    
    async def send_verification_status_email(
        self,
        email: str,
        status: str,
        details: str = None,
    ) -> bool:
        """Send verification status update."""
        subject = f"GlobalTrustHub: Verification {status.title()}"
        body = f"""
Your verification status has been updated.

Status: {status.upper()}
{f'Details: {details}' if details else ''}

Log in to your account to view more details.

Best regards,
GlobalTrustHub Team
        """
        
        return await self.send_email(email, subject, body)
    
    async def send_bulk_email(
        self,
        recipients: List[str],
        subject: str,
        body: str,
    ) -> dict:
        """Send email to multiple recipients."""
        results = {"sent": 0, "failed": 0}
        
        for recipient in recipients:
            success = await self.send_email(recipient, subject, body)
            if success:
                results["sent"] += 1
            else:
                results["failed"] += 1
        
        return results


# Global email service instance
email_service = EmailService()
