"""
Document Model
Model for user documents and verification files.
"""

from datetime import datetime
from typing import Optional
from enum import Enum as PyEnum


class DocumentType(str, PyEnum):
    """Types of documents that can be uploaded."""
    CNIC = "cnic"
    PASSPORT = "passport"
    DRIVING_LICENSE = "driving_license"
    DOMICILE = "domicile"
    DEGREE = "degree"
    TRANSCRIPT = "transcript"
    EXPERIENCE_LETTER = "experience_letter"
    BUSINESS_LICENSE = "business_license"
    BANK_STATEMENT = "bank_statement"
    UTILITY_BILL = "utility_bill"
    OTHER = "other"


class DocumentStatus(str, PyEnum):
    """Document verification status."""
    PENDING = "pending"
    UNDER_REVIEW = "under_review"
    VERIFIED = "verified"
    REJECTED = "rejected"
    EXPIRED = "expired"


class Document:
    """
    Document model for storing user verification documents.
    
    Attributes:
        id: Unique document identifier
        user_id: Owner user ID
        document_type: Type of document
        
        # File Info
        file_url: Secure URL to document file
        file_name: Original file name
        file_size: File size in bytes
        mime_type: MIME type of file
        
        # Verification
        status: Current verification status
        verified_at: Verification timestamp
        verified_by: Admin/moderator who verified
        rejection_reason: Reason if rejected
        
        # AI Analysis
        ai_confidence_score: AI verification confidence (0-1)
        ai_analysis_result: Detailed AI analysis results
        forgery_detected: Whether AI detected potential forgery
        
        # Metadata
        expiry_date: Document expiry date if applicable
        document_number: Document reference number
        issuing_authority: Authority that issued document
        
        # Timestamps
        created_at: Upload timestamp
        updated_at: Last update timestamp
    """
    
    __tablename__ = "documents"
    
    id: str = ""
    user_id: str = ""
    document_type: DocumentType = DocumentType.OTHER
    
    # File Info
    file_url: str = ""
    file_name: str = ""
    file_size: int = 0
    mime_type: str = ""
    
    # Verification
    status: DocumentStatus = DocumentStatus.PENDING
    verified_at: Optional[datetime] = None
    verified_by: Optional[str] = None
    rejection_reason: Optional[str] = None
    
    # AI Analysis
    ai_confidence_score: float = 0.0
    ai_analysis_result: dict = {}
    forgery_detected: bool = False
    
    # Metadata
    expiry_date: Optional[datetime] = None
    document_number: Optional[str] = None
    issuing_authority: Optional[str] = None
    
    # Timestamps
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self) -> str:
        return f"<Document(id={self.id}, type={self.document_type}, status={self.status})>"
    
    @property
    def is_verified(self) -> bool:
        """Check if document is verified."""
        return self.status == DocumentStatus.VERIFIED
    
    @property
    def is_expired(self) -> bool:
        """Check if document has expired."""
        if self.expiry_date is None:
            return False
        return datetime.utcnow() > self.expiry_date
    
    @property
    def needs_review(self) -> bool:
        """Check if document needs manual review."""
        # Needs review if AI confidence is low or forgery suspected
        return (
            self.ai_confidence_score < 0.8 or
            self.forgery_detected or
            self.status == DocumentStatus.UNDER_REVIEW
        )
