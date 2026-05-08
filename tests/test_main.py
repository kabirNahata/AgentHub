from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
API_KEY = "agenthub-dev-key-2024"
HEADERS = {"X-AgentHub-Key": API_KEY}

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]

def test_currency_endpoint(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"EUR": 85.0}}
    mocker.patch("httpx.AsyncClient.get", return_value=mock_response)

    response = client.get("/api/v1/convert/currency?amount=100&from_currency=USD&to_currency=EUR", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["converted_amount"] == 85.0

def test_timezone_endpoint(mocker):
    # Mock Geocoder
    mock_geolocator = mocker.patch("app.services.lookup_service.Nominatim")
    mock_geo_instance = mock_geolocator.return_value
    mock_location = mocker.Mock()
    mock_location.latitude = 35.6895
    mock_location.longitude = 139.6917
    mock_geo_instance.geocode.return_value = mock_location

    # Mock TimeAPI
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "timeZone": "Asia/Tokyo",
        "dateTime": "2024-01-01T12:00:00"
    }
    mocker.patch("httpx.AsyncClient.get", return_value=mock_response)

    response = client.get("/api/v1/lookup/timezone?location=Tokyo", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["data"]["timezone"] == "Asia/Tokyo"

def test_adapter_endpoint(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.url = "https://example.com"
    mock_response.headers = {"Content-Type": "text/html"}
    mock_response.text = "<html><head><title>Example</title></head><body><h1>Hello</h1></body></html>"
    mock_response.is_redirect = False
    mocker.patch("httpx.AsyncClient.get", return_value=mock_response)

    response = client.get("/api/v1/adapter/proxy?url=https://example.com", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "Example"

def test_email_validation_endpoint():
    response = client.get("/api/v1/validate/email?email=test@example.com", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["data"]["is_valid"] is True
