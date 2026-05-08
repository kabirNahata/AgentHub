from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)
API_KEY = "agenthub-dev-key-2024"
HEADERS = {"X-AgentHub-Key": API_KEY}

def test_adapter_ssrf_protection_localhost():
    """Test that requests to localhost are blocked."""
    response = client.get("/api/v1/adapter/proxy?url=http://localhost:8000", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["status"] == "error"
    assert "restricted" in data["data"]["error_message"]

def test_adapter_ssrf_protection_private_ip():
    """Test that requests to private IP ranges are blocked."""
    response = client.get("/api/v1/adapter/proxy?url=http://192.168.1.1", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["status"] == "error"
    assert "restricted" in data["data"]["error_message"]

def test_adapter_ssrf_protection_invalid_scheme():
    """Test that non-http/https schemes are blocked."""
    response = client.get("/api/v1/adapter/proxy?url=file:///etc/passwd", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["status"] == "error"
    assert "restricted" in data["data"]["error_message"]

def test_adapter_valid_url():
    """Test that a valid public URL still works."""
    response = client.get("/api/v1/adapter/proxy?url=https://example.com", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    if data["data"]["status"] == "extracted":
        assert "Example Domain" in data["data"]["title"]
    else:
        assert "restricted" not in data["data"]["error_message"]

def test_adapter_ssrf_protection_ipv6_loopback():
    """Test that IPv6 loopback is blocked."""
    response = client.get("/api/v1/adapter/proxy?url=http://[::1]", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["status"] == "error"
    assert "restricted" in data["data"]["error_message"]
