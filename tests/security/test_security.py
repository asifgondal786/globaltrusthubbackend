"""
Security Tests
Tests for security-related functionality.
"""

import pytest


class TestInputValidation:
    """Tests for input validation security."""
    
    def test_sql_injection_prevention(self):
        """Test SQL injection attempts are handled safely."""
        # Pydantic models and parameterized queries prevent SQL injection
        malicious_input = "'; DROP TABLE users; --"
        
        from app.schemas.user_schema import UserCreate
        
        # Should raise validation error or sanitize
        with pytest.raises(Exception):
            UserCreate(
                email=malicious_input,
                password="ValidPass123",
                full_name="Test",
            )
    
    def test_xss_prevention(self):
        """Test XSS attempts are sanitized."""
        from app.utils.text_processing import sanitize_text
        
        malicious_input = "<script>alert('xss')</script>"
        sanitized = sanitize_text(malicious_input)
        
        assert "<script>" not in sanitized
    
    def test_cnic_validation(self):
        """Test CNIC format validation."""
        from app.schemas.user_schema import UserVerificationUpdate
        
        # Valid CNIC
        data = UserVerificationUpdate(cnic_number="12345-6789012-3")
        assert data.cnic_number == "1234567890123"  # Normalized
        
        # Invalid CNIC should raise
        with pytest.raises(Exception):
            UserVerificationUpdate(cnic_number="invalid")


class TestAuthentication:
    """Tests for authentication security."""
    
    def test_password_length_requirement(self):
        """Test minimum password length is enforced."""
        from app.schemas.auth_schema import RegisterRequest
        
        with pytest.raises(Exception):
            RegisterRequest(
                email="test@example.com",
                password="short",  # Too short
                full_name="Test User",
            )
    
    def test_password_complexity_requirement(self):
        """Test password complexity is enforced."""
        from app.schemas.user_schema import UserCreate
        
        # Password without uppercase should fail
        with pytest.raises(Exception):
            UserCreate(
                email="test@example.com",
                password="alllowercase123",
                full_name="Test",
            )


class TestRateLimiting:
    """Tests for rate limiting."""
    
    def test_rate_limiter_initialization(self):
        """Test rate limiter can be initialized."""
        from app.core.rate_limiter import RateLimiter
        
        limiter = RateLimiter(requests_per_period=10, period_seconds=60)
        assert limiter.requests_per_period == 10


class TestDataMasking:
    """Tests for sensitive data masking."""
    
    def test_email_masking(self):
        """Test email addresses are properly masked."""
        from app.utils.text_processing import mask_sensitive_data
        
        text = "Contact me at user@example.com"
        masked = mask_sensitive_data(text)
        
        assert "user@example.com" not in masked
        assert "@example.com" in masked  # Domain preserved
    
    def test_phone_masking(self):
        """Test phone numbers are properly masked."""
        from app.utils.text_processing import mask_sensitive_data
        
        text = "Call me at 03001234567"
        masked = mask_sensitive_data(text)
        
        assert "03001234567" not in masked
    
    def test_cnic_masking(self):
        """Test CNIC numbers are properly masked."""
        from app.utils.text_processing import mask_sensitive_data
        
        text = "My CNIC is 12345-6789012-3"
        masked = mask_sensitive_data(text)
        
        assert "6789012" not in masked


class TestScamDetection:
    """Tests for scam detection security."""
    
    def test_scam_pattern_detection(self):
        """Test scam patterns are detected."""
        from app.ai_ml.scam_language_analysis.nlp_preprocessing import detect_patterns
        
        scam_text = "Send money immediately to get guaranteed visa approval!"
        patterns = detect_patterns(scam_text)
        
        assert len(patterns) > 0
    
    def test_clean_text_detected_as_safe(self):
        """Test legitimate text is not flagged."""
        from app.ai_ml.scam_language_analysis.nlp_preprocessing import calculate_scam_score
        
        clean_text = "I am interested in applying to universities in the UK."
        score, reasons = calculate_scam_score(clean_text)
        
        assert score < 0.3  # Low scam probability


class TestPermissions:
    """Tests for permission system."""
    
    def test_role_permission_mapping(self):
        """Test roles have correct permissions."""
        from app.core.permissions import has_permission, UserRole, Permission
        
        # Student can view profile
        assert has_permission(UserRole.STUDENT, Permission.VIEW_PROFILE)
        
        # Student cannot manage users
        assert not has_permission(UserRole.STUDENT, Permission.MANAGE_USERS)
        
        # Admin can manage users
        assert has_permission(UserRole.ADMIN, Permission.MANAGE_USERS)
    
    def test_admin_has_all_permissions(self):
        """Test admin has all permissions."""
        from app.core.permissions import get_role_permissions, UserRole, Permission
        
        admin_permissions = get_role_permissions(UserRole.ADMIN)
        all_permissions = list(Permission)
        
        for perm in all_permissions:
            assert perm in admin_permissions
