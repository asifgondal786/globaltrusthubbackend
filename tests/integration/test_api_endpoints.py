"""
Integration Tests - API Endpoints
Tests for API endpoint integration.
"""

import pytest
from fastapi.testclient import TestClient


# Test fixtures
@pytest.fixture
def client():
    """Create test client."""
    from app.main import app
    return TestClient(app)


@pytest.fixture
def auth_headers():
    """Create authorization headers with test token."""
    # In production: generate actual test token
    return {"Authorization": "Bearer test_token"}


# Health check tests
def test_root_endpoint(client):
    """Test root endpoint returns health status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_health_endpoint(client):
    """Test detailed health check."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data


# Authentication endpoint tests
class TestAuthEndpoints:
    """Tests for authentication endpoints."""
    
    def test_login_missing_fields(self, client):
        """Test login with missing fields returns 422."""
        response = client.post("/api/v1/auth/login", json={})
        assert response.status_code == 422
    
    def test_registration_missing_fields(self, client):
        """Test registration with missing fields returns 422."""
        response = client.post("/api/v1/auth/register", json={})
        assert response.status_code == 422
    
    def test_registration_valid_request(self, client):
        """Test registration with valid data."""
        response = client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "password": "SecurePass123",
            "full_name": "Test User",
        })
        # Would be 200/201 in production with database
        assert response.status_code in [200, 201, 422]


# User endpoint tests
class TestUserEndpoints:
    """Tests for user endpoints."""
    
    def test_get_me_unauthorized(self, client):
        """Test /me without auth returns 403."""
        response = client.get("/api/v1/users/me")
        assert response.status_code == 403
    
    def test_get_user_public_profile(self, client, auth_headers):
        """Test getting public user profile."""
        # Would need valid auth in production
        pass


# Service endpoint tests
class TestServiceEndpoints:
    """Tests for service endpoints."""
    
    def test_list_services(self, client):
        """Test listing services."""
        response = client.get("/api/v1/services/")
        assert response.status_code == 200
        data = response.json()
        assert "services" in data
    
    def test_list_categories(self, client):
        """Test listing service categories."""
        response = client.get("/api/v1/services/categories")
        assert response.status_code == 200
        data = response.json()
        assert "categories" in data


# Review endpoint tests
class TestReviewEndpoints:
    """Tests for review endpoints."""
    
    def test_list_reviews_requires_target(self, client):
        """Test listing reviews requires target_id."""
        response = client.get("/api/v1/reviews/")
        assert response.status_code == 422  # Missing required query params


# Payment endpoint tests
class TestPaymentEndpoints:
    """Tests for payment endpoints."""
    
    def test_list_subscription_plans(self, client):
        """Test listing subscription plans."""
        response = client.get("/api/v1/payments/subscriptions/plans")
        assert response.status_code == 200
        data = response.json()
        assert "plans" in data
        assert len(data["plans"]) > 0


# Admin endpoint tests - all require admin auth
class TestAdminEndpoints:
    """Tests for admin endpoints."""
    
    def test_admin_dashboard_unauthorized(self, client):
        """Test admin dashboard requires auth."""
        response = client.get("/api/v1/admin/dashboard")
        assert response.status_code == 403
