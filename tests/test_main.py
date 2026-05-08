from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]

def test_currency_endpoint():
    response = client.get("/api/v1/convert/currency?amount=100&from_currency=USD&to_currency=EUR")
    assert response.status_code == 200
    data = response.json()
    assert "converted_amount" in data["data"]
    assert data["data"]["converted_amount"] > 0

def test_timezone_endpoint():
    response = client.get("/api/v1/lookup/timezone?location=Tokyo")
    assert response.status_code == 200
    assert "timezone" in response.json()["data"]

def test_adapter_endpoint():
    response = client.get("/api/v1/adapter/proxy?url=https://example.com")
    assert response.status_code == 200
    assert "title" in response.json()["data"]
def test_email_validation_endpoint():
    response = client.get("/api/v1/validate/email?email=test@example.com")
    assert response.status_code == 200
    assert response.json()["data"]["is_valid"] is True
