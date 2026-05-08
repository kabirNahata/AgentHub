import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
API_KEY = "agenthub-dev-key-2024"
HEADERS = {"X-AgentHub-Key": API_KEY}

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to AgentHub" in response.json()["message"]

def test_registry_endpoint():
    response = client.get("/api/v1/registry", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "services" in data["data"]
    assert data["agent_info"]["is_agent_ready"] is True
    assert "timestamp" in data

def test_currency_endpoint():
    response = client.get("/api/v1/convert/currency?amount=100&from_currency=USD&to_currency=EUR", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["converted_amount"] == 92.0
    assert "timestamp" in data

def test_timezone_endpoint():
    response = client.get("/api/v1/lookup/timezone?location=Tokyo", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["data"]["timezone"] == "Asia/Tokyo"
    assert "timestamp" in response.json()

def test_adapter_endpoint():
    response = client.get("/api/v1/adapter/proxy?url=https://example-news.com", headers=HEADERS)
    assert response.status_code == 200
    assert "articles" in response.json()["data"]
    assert "timestamp" in response.json()

def test_auth_failure():
    response = client.get("/api/v1/registry")
    assert response.status_code == 422 # Missing header

    response = client.get("/api/v1/registry", headers={"X-AgentHub-Key": "wrong-key"})
    assert response.status_code == 401
