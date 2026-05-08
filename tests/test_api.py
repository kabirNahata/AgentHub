import pytest
from fastapi.testclient import TestClient
from main import app, settings

client = TestClient(app)

API_KEY = settings.app_api_key
HEADERS = {"X-API-Key": API_KEY}

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "AgentHub" in response.json()["message"]

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_auth_failure():
    response = client.get("/convert/unit?value=1&from_unit=meter&to_unit=feet", headers={"X-API-Key": "wrong"})
    assert response.status_code == 403

def test_convert_unit_success():
    response = client.get("/convert/unit?value=1&from_unit=meter&to_unit=feet", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "converted_value" in data
    assert data["unit_label"] == "feet"
    # 1 meter is approx 3.28084 feet
    assert 3.28 < data["converted_value"] < 3.29

def test_convert_unit_invalid():
    response = client.get("/convert/unit?value=1&from_unit=meter&to_unit=second", headers=HEADERS)
    assert response.status_code == 400
    assert "Incompatible units" in response.json()["detail"]

def test_convert_currency_mock():
    # Since we don't have an OER key in the environment, it should use the mock
    response = client.get("/convert/currency?amount=200&from=USD&to=NPR", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["rate"] == 133.0
    assert data["converted_amount"] == 200 * 133.0

def test_validate_email_mock():
    response = client.get("/validate/email?email=test@example.com", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["valid"] is True

    response = client.get("/validate/email?email=invalid-email", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["valid"] is False

def test_resolve_timezone_mock():
    response = client.get("/resolve/timezone?city=Kathmandu", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["timezone_name"] == "Asia/Kathmandu"

    response = client.get("/resolve/timezone?city=27.7,85.3", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["timezone_name"] == "Asia/Kathmandu"
