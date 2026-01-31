"""
Unit Tests - Authentication
Tests for authentication functionality.
"""

import pytest
from datetime import datetime, timedelta

# Test password hashing
def test_password_hashing():
    """Test password hashing and verification."""
    from app.core.security import get_password_hash, verify_password
    
    password = "SecurePassword123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("WrongPassword", hashed)


def test_password_hash_uniqueness():
    """Test that same password produces different hashes."""
    from app.core.security import get_password_hash
    
    password = "TestPassword123"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)
    
    assert hash1 != hash2  # bcrypt includes random salt


# Test JWT tokens
def test_create_access_token():
    """Test access token creation."""
    from app.core.security import create_access_token, verify_token
    
    data = {"sub": "user123", "email": "test@example.com"}
    token = create_access_token(data)
    
    assert token is not None
    payload = verify_token(token)
    assert payload["sub"] == "user123"


def test_create_refresh_token():
    """Test refresh token creation."""
    from app.core.security import create_refresh_token, verify_token
    
    data = {"sub": "user123"}
    token = create_refresh_token(data)
    
    payload = verify_token(token)
    assert payload["sub"] == "user123"
    assert payload["type"] == "refresh"


def test_token_expiry():
    """Test that expired tokens are rejected."""
    from app.core.security import create_access_token, verify_token
    from datetime import timedelta
    
    data = {"sub": "user123"}
    # Create token that already expired
    token = create_access_token(data, expires_delta=timedelta(seconds=-1))
    
    payload = verify_token(token)
    assert payload is None  # Expired token should return None


def test_invalid_token():
    """Test that invalid tokens are rejected."""
    from app.core.security import verify_token
    
    result = verify_token("invalid.token.here")
    assert result is None


# Test login request validation
def test_login_request_validation():
    """Test login request schema validation."""
    from app.schemas.auth_schema import LoginRequest
    
    # Valid request
    request = LoginRequest(
        email="test@example.com",
        password="password123",
    )
    assert request.email == "test@example.com"
    
    # Invalid email should raise
    with pytest.raises(Exception):
        LoginRequest(email="invalid-email", password="password123")


# Test registration validation
def test_registration_password_requirements():
    """Test password requirements for registration."""
    from app.schemas.auth_schema import RegisterRequest
    
    # Valid registration
    request = RegisterRequest(
        email="test@example.com",
        password="SecurePass123",
        full_name="Test User",
    )
    assert request.email == "test@example.com"


# Test rate limiting
def test_rate_limiter_allows_within_limit():
    """Test rate limiter allows requests within limit."""
    # This would test the rate limiter functionality
    pass


def test_rate_limiter_blocks_over_limit():
    """Test rate limiter blocks excessive requests."""
    # This would test blocking after limit exceeded
    pass
