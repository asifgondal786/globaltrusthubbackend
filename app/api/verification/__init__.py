"""
Verification API Router
Document verification endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form

from app.dependencies import get_current_active_user, get_admin_user
from app.models.user import User
from app.models.document import DocumentType, DocumentStatus

router = APIRouter()


@router.post("/documents/upload")
async def upload_document(
    document_type: str = Form(...),
    document_number: str = Form(None),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
):
    """
    Upload a document for verification.
    
    - **document_type**: Type of document (cnic, passport, etc.)
    - **document_number**: Document reference number
    - **file**: Document file (JPEG, PNG, or PDF)
    """
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Allowed: JPEG, PNG, PDF",
        )
    
    # In production: save file, create document record, trigger AI analysis
    
    return {
        "message": "Document uploaded successfully",
        "document_id": "doc_123",
        "status": "pending",
        "estimated_review_time": "24-48 hours",
    }


@router.get("/documents")
async def list_my_documents(current_user: User = Depends(get_current_active_user)):
    """
    List current user's uploaded documents.
    """
    # In production: fetch from database
    return {
        "documents": [],
        "verification_status": current_user.verification_status,
    }


@router.get("/documents/{document_id}")
async def get_document_status(
    document_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """
    Get status of a specific document.
    """
    return {
        "document_id": document_id,
        "status": "pending",
        "uploaded_at": "2024-01-01T00:00:00Z",
    }


@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """
    Delete an uploaded document.
    """
    return {"message": f"Document {document_id} deleted"}


@router.get("/status")
async def get_verification_status(current_user: User = Depends(get_current_active_user)):
    """
    Get current user's overall verification status.
    """
    return {
        "user_id": current_user.id,
        "verification_status": current_user.verification_status,
        "verification_level": current_user.verification_level,
        "documents_submitted": 0,
        "documents_verified": 0,
        "documents_pending": 0,
        "next_steps": ["Submit CNIC", "Submit proof of address"],
    }


# Admin endpoints

@router.get("/admin/pending")
async def list_pending_verifications(
    page: int = 1,
    admin_user: User = Depends(get_admin_user),
):
    """
    List documents pending verification (admin only).
    """
    return {
        "documents": [],
        "total": 0,
        "page": page,
    }


@router.post("/admin/documents/{document_id}/verify")
async def verify_document(
    document_id: str,
    verified: bool,
    notes: str = None,
    admin_user: User = Depends(get_admin_user),
):
    """
    Verify or reject a document (admin only).
    """
    status_text = "verified" if verified else "rejected"
    return {
        "message": f"Document {document_id} has been {status_text}",
        "verified_by": admin_user.id,
    }


@router.post("/admin/users/{user_id}/verify-level")
async def set_verification_level(
    user_id: str,
    level: int,
    admin_user: User = Depends(get_admin_user),
):
    """
    Manually set user's verification level (admin only).
    """
    return {
        "message": f"User {user_id} verification level set to {level}",
        "set_by": admin_user.id,
    }
