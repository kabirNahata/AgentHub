from typing import Dict, Any
from geopy.geocoders import Nominatim
from geopy.exc import GeopyError
from fastapi import HTTPException
import httpx

class LookupService:
    # Expanded mock data for facts and jurisdictions
    JURISDICTIONS = {
        "California": {"country": "USA", "type": "State"},
        "London": {"country": "UK", "type": "City"},
        "Tokyo": {"country": "Japan", "type": "City"},
        "Paris": {"country": "France", "type": "City"},
        "New York": {"country": "USA", "type": "City"},
        "Texas": {"country": "USA", "type": "State"},
        "Berlin": {"country": "Germany", "type": "City"},
        "Sydney": {"country": "Australia", "type": "City"}
    }

    FACTS = {
        "capital of france": "Paris",
        "speed of light": "299,792,458 meters per second",
        "largest planet": "Jupiter",
        "boiling point of water": "100 degrees Celsius",
        "first man on the moon": "Neil Armstrong",
        "capital of japan": "Tokyo",
        "square root of 144": "12",
        "mount everest height": "8,848 meters"
    }

    @staticmethod
    async def resolve_timezone(location: str) -> Dict[str, str]:
        geolocator = Nominatim(user_agent="AgentHub/0.1 (contact@agenthub.dev)")
        try:
            loc = geolocator.geocode(location)
            if not loc:
                raise HTTPException(status_code=400, detail=f"Location not found: {location}")

            async with httpx.AsyncClient(timeout=10.0) as client:
                try:
                    response = await client.get(
                        "https://timeapi.io/api/Time/current/coordinate",
                        params={"latitude": loc.latitude, "longitude": loc.longitude}
                    )
                    if response.status_code == 200:
                        data = response.json()
                        return {
                            "location": location,
                            "timezone": data.get("timeZone", "Unknown"),
                            "current_time": data.get("dateTime", "Unknown")
                        }
                except (httpx.TimeoutException, httpx.RequestError):
                    # Fallback to coordinate-based approximation if timeapi.io is down
                    pass

                return {
                    "location": location,
                    "latitude": loc.latitude,
                    "longitude": loc.longitude,
                    "timezone": "Unknown",
                    "info": "Could not resolve timezone name from external API, but coordinates found."
                }

        except GeopyError as e:
            raise HTTPException(status_code=503, detail=f"Geocoding service unavailable: {str(e)}")
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    @staticmethod
    def check_jurisdiction(location: str) -> Dict[str, Any]:
        info = LookupService.JURISDICTIONS.get(location)
        if not info:
             # Basic attempt to be "real" - just return what we have or a 404
             raise HTTPException(status_code=404, detail=f"Jurisdiction info not found for: {location}")
        return {"location": location, "info": info}

    @staticmethod
    def factual_lookup(query: str) -> Dict[str, str]:
        answer = LookupService.FACTS.get(query.lower())
        if not answer:
            raise HTTPException(status_code=404, detail=f"No factual information found for: {query}")
        return {"query": query, "answer": answer}
