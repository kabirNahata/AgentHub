from typing import Dict
from email_validator import validate_email, EmailNotValidError
from geopy.geocoders import Nominatim
from geopy.exc import GeopyError
from fastapi import HTTPException

class ValidationService:
    @staticmethod
    def validate_email(email: str) -> Dict[str, bool]:
        try:
            # Check that the email address is valid
            validation = validate_email(email, check_deliverability=False)
            return {"is_valid": True, "normalized_email": validation.normalized}
        except EmailNotValidError as e:
            raise HTTPException(status_code=400, detail=f"Invalid email address: {str(e)}")

    @staticmethod
    def validate_address(address: str) -> Dict[str, bool]:
        geolocator = Nominatim(user_agent="AgentHub/0.1 (contact@agenthub.dev)")
        try:
            location = geolocator.geocode(address)
            if location:
                return {
                    "is_valid": True,
                    "formatted_address": location.address,
                    "latitude": location.latitude,
                    "longitude": location.longitude
                }
            else:
                raise HTTPException(status_code=400, detail="Address not found")
        except GeopyError as e:
            raise HTTPException(status_code=503, detail=f"Address validation service unavailable: {str(e)}")
