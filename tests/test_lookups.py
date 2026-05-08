import pytest
from app.services.lookup_service import LookupService

def test_timezone_resolution():
    res = LookupService.resolve_timezone("London")
    assert res["timezone"] == "Europe/London"

def test_jurisdiction_check():
    res = LookupService.check_jurisdiction("California")
    assert res["info"]["country"] == "USA"

def test_factual_lookup():
    res = LookupService.factual_lookup("capital of france")
    assert res["answer"] == "Paris"
