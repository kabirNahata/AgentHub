import pytest
from app.services.conversion_service import ConversionService
from app.services.validation_service import ValidationService

def test_currency_conversion():
    res = ConversionService.convert_currency(100, "USD", "EUR")
    assert res["converted_amount"] == 92.0
    assert res["rate"] == 0.92

def test_unit_conversion():
    res = ConversionService.convert_unit(1, "meter", "foot")
    assert res == 3.28084

def test_email_validation():
    assert ValidationService.validate_email("test@example.com")["is_valid"] is True
    assert ValidationService.validate_email("user.name+tag@sub.example.com")["is_valid"] is True
    assert ValidationService.validate_email("invalid-email")["is_valid"] is False

def test_address_validation():
    assert ValidationService.validate_address("123 Main St, New York, NY")["is_valid"] is True
    assert ValidationService.validate_address("JustAString")["is_valid"] is False
