import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to AgentHub" in response.json()["message"]

def test_registry_endpoint():
    response = client.get("/api/v1/registry")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "services" in data["data"]
    assert data["agent_info"]["is_agent_ready"] is True

def test_currency_endpoint():
    response = client.get("/api/v1/convert/currency?amount=100&from_currency=USD&to_currency=EUR")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["converted_amount"] == 92.0

def test_timezone_endpoint():
    response = client.get("/api/v1/lookup/timezone?location=Tokyo")
    assert response.status_code == 200
    assert response.json()["data"]["timezone"] == "Asia/Tokyo"

def test_adapter_endpoint():
    response = client.get("/api/v1/adapter/proxy?url=https://example.com")
    assert response.status_code == 200
    assert "title" in response.json()["data"]
