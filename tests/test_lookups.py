import pytest
from app.services.lookup_service import LookupService

async def test_timezone_resolution(mocker):
    # Mock Geocoder
    mock_geolocator = mocker.patch("app.services.lookup_service.Nominatim")
    mock_geo_instance = mock_geolocator.return_value
    mock_location = mocker.Mock()
    mock_location.latitude = 51.5074
    mock_location.longitude = -0.1278
    mock_geo_instance.geocode.return_value = mock_location

    # Mock TimeAPI
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "timeZone": "Europe/London",
        "dateTime": "2024-01-01T12:00:00"
    }
    mocker.patch("httpx.AsyncClient.get", return_value=mock_response)

    res = await LookupService.resolve_timezone("London")
    assert res["timezone"] == "Europe/London"
    assert res["location"] == "London"

def test_jurisdiction_check():
    res = LookupService.check_jurisdiction("California")
    assert res["info"]["country"] == "USA"

def test_factual_lookup():
    res = LookupService.factual_lookup("capital of france")
    assert res["answer"] == "Paris"
