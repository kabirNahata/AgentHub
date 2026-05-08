import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_health_endpoint(mocker):
    # Mock external calls in health check
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mocker.patch("httpx.AsyncClient.get", return_value=mock_response)

    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"
    assert "version" in data
    assert "app_name" in data
    assert "external_dependencies" in data

async def test_web_adapter_real_structure(mocker):
    from app.services.web_adapter_service import WebAdapterService

    url = "https://example.com"

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.url = url
    mock_response.headers = {"Content-Type": "text/html"}
    mock_response.text = "<html><head><title>Example</title></head><body><h1>Hello</h1><a href='/test'>Link</a></body></html>"
    mock_response.is_redirect = False

    mocker.patch("httpx.AsyncClient.get", return_value=mock_response)

    res = await WebAdapterService.fetch_structured_data(url)

    assert res["url"] == url
    assert res["status"] == "extracted"
    assert res["title"] == "Example"
    assert "links" in res
    assert len(res["links"]) > 0
