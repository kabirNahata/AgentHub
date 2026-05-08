import pytest
from app.services.web_adapter_service import WebAdapterService

@pytest.mark.asyncio
async def test_web_adapter_service():
    url = "https://example.com"
    res = await WebAdapterService.fetch_structured_data(url)
    assert res["url"] == url
    assert "title" in res

@pytest.mark.asyncio
async def test_web_adapter_structure():
    url = "https://example.com"
    res = await WebAdapterService.fetch_structured_data(url)
    assert "headers" in res
    assert "links" in res
    assert "content_summary" in res
