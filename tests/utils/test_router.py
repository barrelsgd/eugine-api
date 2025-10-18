"""Tests for utils router."""

from fastapi.testclient import TestClient

from src.config import settings


def test_health_check(client: TestClient) -> None:
    """Test health check endpoint."""
    response = client.get(f"{settings.API_V1_STR}/utils/health-check/")
    
    assert response.status_code == 200
    content = response.json()
    assert content is True  # Health check returns boolean


def test_test_email(client: TestClient, superuser_token_headers: dict[str, str]) -> None:
    """Test email testing endpoint."""
    email_to = "test@example.com"
    response = client.post(
        f"{settings.API_V1_STR}/utils/test-email/?email_to={email_to}",
        headers=superuser_token_headers,
    )
    
    assert response.status_code == 201
    content = response.json()
    assert "message" in content
