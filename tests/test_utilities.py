import pytest
from app.services.conversion_service import ConversionService
from app.services.validation_service import ValidationService
from fastapi import HTTPException

@pytest.mark.asyncio
async def test_currency_conversion():
    res = await ConversionService.convert_currency(100, "USD", "EUR")
    assert "converted_amount" in res
    assert "rate" in res
    assert res["rate"] > 0

def test_unit_conversion():
    res = ConversionService.convert_unit(1, "meter", "foot")
    assert res == 3.28084

def test_email_validation():
    assert ValidationService.validate_email("test@example.com")["is_valid"] is True
    assert ValidationService.validate_email("user.name+tag@sub.example.com")["is_valid"] is True
    with pytest.raises(HTTPException) as excinfo:
        ValidationService.validate_email("invalid-email")
    assert excinfo.value.status_code == 400

def test_address_validation():
    # We might want to mock this in a real scenario to avoid external dependencies in tests
    # But for now, let's just handle potential errors or use a known valid address
    try:
        res = ValidationService.validate_address("1600 Pennsylvania Avenue NW, Washington, DC")
        assert res["is_valid"] is True
    except HTTPException as e:
        if e.status_code == 503:
             pytest.skip("External geocoding service unavailable")
        raise e

    with pytest.raises(HTTPException) as excinfo:
        ValidationService.validate_address("thisisnotarealaddress1234567890")
    assert excinfo.value.status_code == 400
