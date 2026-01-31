"""
File Upload Utilities
Helpers for file validation and processing.
"""

from typing import Tuple, Optional
from pathlib import Path
import hashlib
import magic  # python-magic for mime type detection


ALLOWED_IMAGE_TYPES = {
    "image/jpeg": [".jpg", ".jpeg"],
    "image/png": [".png"],
    "image/webp": [".webp"],
}

ALLOWED_DOCUMENT_TYPES = {
    "application/pdf": [".pdf"],
    "image/jpeg": [".jpg", ".jpeg"],
    "image/png": [".png"],
}

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10MB


def validate_file_type(content: bytes, expected_types: dict) -> Tuple[bool, str]:
    """
    Validate file type using magic bytes.
    
    Args:
        content: File content bytes
        expected_types: Dict of allowed mime types and extensions
    
    Returns:
        Tuple[bool, str]: (is_valid, detected_mime_type)
    """
    try:
        mime = magic.Magic(mime=True)
        detected_type = mime.from_buffer(content)
        
        is_valid = detected_type in expected_types
        return is_valid, detected_type
    except Exception:
        return False, "unknown"


def validate_file_size(content: bytes, max_size: int) -> bool:
    """Check if file size is within limit."""
    return len(content) <= max_size


def compute_file_hash(content: bytes) -> str:
    """
    Compute SHA-256 hash of file content.
    Used for duplicate detection and integrity verification.
    """
    return hashlib.sha256(content).hexdigest()


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal attacks.
    """
    # Remove path separators and special characters
    sanitized = Path(filename).name
    
    # Replace problematic characters
    for char in ['<', '>', ':', '"', '|', '?', '*', '\0']:
        sanitized = sanitized.replace(char, '_')
    
    # Limit length
    if len(sanitized) > 255:
        name, ext = sanitized.rsplit('.', 1) if '.' in sanitized else (sanitized, '')
        sanitized = name[:250] + ('.' + ext if ext else '')
    
    return sanitized


def get_file_extension(filename: str, mime_type: str) -> str:
    """
    Get appropriate file extension based on mime type.
    """
    # Map of mime types to preferred extensions
    mime_to_ext = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
        "application/pdf": ".pdf",
    }
    
    # Try to get extension from mime type first
    if mime_type in mime_to_ext:
        return mime_to_ext[mime_type]
    
    # Fall back to filename extension
    parts = filename.rsplit('.', 1)
    if len(parts) > 1:
        return '.' + parts[1].lower()
    
    return '.bin'


def validate_image_upload(
    content: bytes,
    filename: str,
) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Validate an image upload.
    
    Returns:
        Tuple[bool, Optional[str], Optional[str]]: (is_valid, mime_type, error_message)
    """
    # Check size
    if not validate_file_size(content, MAX_IMAGE_SIZE):
        return False, None, f"Image too large. Max size: {MAX_IMAGE_SIZE // (1024*1024)}MB"
    
    # Check type
    is_valid, mime_type = validate_file_type(content, ALLOWED_IMAGE_TYPES)
    if not is_valid:
        return False, mime_type, f"Invalid image type: {mime_type}. Allowed: JPEG, PNG, WebP"
    
    return True, mime_type, None


def validate_document_upload(
    content: bytes,
    filename: str,
) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Validate a document upload.
    
    Returns:
        Tuple[bool, Optional[str], Optional[str]]: (is_valid, mime_type, error_message)
    """
    # Check size
    if not validate_file_size(content, MAX_DOCUMENT_SIZE):
        return False, None, f"Document too large. Max size: {MAX_DOCUMENT_SIZE // (1024*1024)}MB"
    
    # Check type
    is_valid, mime_type = validate_file_type(content, ALLOWED_DOCUMENT_TYPES)
    if not is_valid:
        return False, mime_type, f"Invalid document type: {mime_type}. Allowed: PDF, JPEG, PNG"
    
    return True, mime_type, None
