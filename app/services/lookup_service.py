from typing import Dict, Any

class LookupService:
    # Mock data
    TIMEZONES = {
        "New York": "America/New_York",
        "London": "Europe/London",
        "Tokyo": "Asia/Tokyo"
    }

    JURISDICTIONS = {
        "California": {"country": "USA", "type": "State"},
        "London": {"country": "UK", "type": "City"}
    }

    FACTS = {
        "capital of france": "Paris",
        "speed of light": "299,792,458 meters per second"
    }

    @staticmethod
    def resolve_timezone(location: str) -> Dict[str, str]:
        tz = LookupService.TIMEZONES.get(location)
        return {"location": location, "timezone": tz or "UTC"}

    @staticmethod
    def check_jurisdiction(location: str) -> Dict[str, Any]:
        info = LookupService.JURISDICTIONS.get(location)
        return {"location": location, "info": info or "Unknown jurisdiction"}

    @staticmethod
    def factual_lookup(query: str) -> Dict[str, str]:
        answer = LookupService.FACTS.get(query.lower())
        return {"query": query, "answer": answer or "I'm sorry, I don't have information on that topic."}
