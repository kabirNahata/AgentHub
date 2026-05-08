import pytest
from app.services.web_adapter_service import WebAdapterService

@pytest.mark.asyncio
async def test_web_adapter_service():
    url = "https://example-news.com/tech"
    res = await WebAdapterService.fetch_structured_data(url)
    assert res["source"] == "Example News"
    assert len(res["articles"]) == 2

@pytest.mark.asyncio
async def test_web_adapter_generic():
    url = "https://google.com"
    res = await WebAdapterService.fetch_structured_data(url)
    assert res["url"] == url
    assert res["metadata"]["type"] == "generic_adapter"
