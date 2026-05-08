import pytest
from app.services.web_adapter_service import WebAdapterService

async def test_web_adapter_service(mocker):
    url = "https://example.com"

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.url = url
    mock_response.headers = {"Content-Type": "text/html"}
    mock_response.text = "<html><head><title>Example</title></head><body><h1>Hello</h1></body></html>"
    mock_response.is_redirect = False
    mocker.patch("httpx.AsyncClient.get", return_value=mock_response)

    res = await WebAdapterService.fetch_structured_data(url)
    assert res["url"] == url
    assert "title" in res

async def test_web_adapter_structure(mocker):
    url = "https://example.com"

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.url = url
    mock_response.headers = {"Content-Type": "text/html"}
    mock_response.text = "<html><head><title>Example</title></head><body><h1>Hello</h1><a href='/test'>Link</a></body></html>"
    mock_response.is_redirect = False
    mocker.patch("httpx.AsyncClient.get", return_value=mock_response)

    res = await WebAdapterService.fetch_structured_data(url)
    assert "headers" in res
    assert "links" in res
    assert "content_summary" in res
