import pytest
from app.services.lookup_service import LookupService

@pytest.mark.asyncio
async def test_timezone_resolution():
    res = await LookupService.resolve_timezone("London")
    assert "timezone" in res
    # Depending on the API, it might return Europe/London or something similar
    assert res["location"] == "London"

def test_jurisdiction_check():
    res = LookupService.check_jurisdiction("California")
    assert res["info"]["country"] == "USA"

def test_factual_lookup():
    res = LookupService.factual_lookup("capital of france")
    assert res["answer"] == "Paris"
