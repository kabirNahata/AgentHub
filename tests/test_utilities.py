import pytest
from app.services.conversion_service import ConversionService
from app.services.validation_service import ValidationService
from fastapi import HTTPException

async def test_currency_conversion(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"EUR": 85.0}}

    mocker.patch("httpx.AsyncClient.get", return_value=mock_response)

    res = await ConversionService.convert_currency(100, "USD", "EUR")
    assert res["converted_amount"] == 85.0
    assert res["rate"] == 0.85

async def test_currency_conversion_npr_fallback(mocker):
    # Mock Frankfurter failure
    mock_frankfurter = mocker.Mock()
    mock_frankfurter.status_code = 404

    # Mock Exchangerate-API success
    mock_exchangerate = mocker.Mock()
    mock_exchangerate.status_code = 200
    mock_exchangerate.json.return_value = {"rates": {"NPR": 130.0}}

    mocker.patch("httpx.AsyncClient.get", side_effect=[mock_frankfurter, mock_exchangerate])

    res = await ConversionService.convert_currency(100, "USD", "NPR")
    assert res["converted_amount"] == 13000.0
    assert res["rate"] == 130.0

def test_unit_conversion():
    res = ConversionService.convert_unit(1, "meter", "foot")
    assert res == 3.28084

def test_email_validation():
    assert ValidationService.validate_email("test@example.com")["is_valid"] is True
    assert ValidationService.validate_email("user.name+tag@sub.example.com")["is_valid"] is True
    with pytest.raises(HTTPException) as excinfo:
        ValidationService.validate_email("invalid-email")
    assert excinfo.value.status_code == 400

def test_address_validation(mocker):
    mock_geolocator = mocker.patch("app.services.validation_service.Nominatim")
    mock_instance = mock_geolocator.return_value

    # Mock success
    mock_location = mocker.Mock()
    mock_location.address = "1600 Pennsylvania Avenue NW, Washington, DC"
    mock_location.latitude = 38.8977
    mock_location.longitude = -77.0365
    mock_instance.geocode.return_value = mock_location

    res = ValidationService.validate_address("1600 Pennsylvania Ave NW")
    assert res["is_valid"] is True
    assert res["formatted_address"] == "1600 Pennsylvania Avenue NW, Washington, DC"

    # Mock failure
    mock_instance.geocode.return_value = None
    with pytest.raises(HTTPException) as excinfo:
        ValidationService.validate_address("thisisnotarealaddress1234567890")
    assert excinfo.value.status_code == 400
