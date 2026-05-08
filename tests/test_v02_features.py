import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"
    assert "version" in data
    assert "app_name" in data

@pytest.mark.asyncio
async def test_web_adapter_real_structure():
    from app.services.web_adapter_service import WebAdapterService
    # Use a reliable URL for testing, or mock it.
    # Since I've updated the service to be "real", it will try to fetch.
    # For testing purposes without external network dependecy in all environments,
    # we might want to mock httpx, but let's see if we can test the structure.

    url = "https://example.com"
    res = await WebAdapterService.fetch_structured_data(url)

    assert res["url"] == url
    assert "status" in res
    assert "title" in res
    assert "headers" in res
    assert "links" in res
    assert "content_summary" in res
