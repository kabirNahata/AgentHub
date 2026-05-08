from typing import Dict

class ConversionService:
    # Mock data for v1
    CURRENCY_RATES = {
        "USD": {"EUR": 0.92, "GBP": 0.79, "JPY": 150.0},
        "EUR": {"USD": 1.09, "GBP": 0.86, "JPY": 163.0},
    }

    UNIT_FACTORS = {
        "meter": {"foot": 3.28084, "inch": 39.3701},
        "kilogram": {"pound": 2.20462},
    }

    @staticmethod
    def convert_currency(amount: float, from_curr: str, to_curr: str) -> Dict[str, float]:
        if from_curr == to_curr:
            return {"converted_amount": amount, "rate": 1.0}

        rate = ConversionService.CURRENCY_RATES.get(from_curr.upper(), {}).get(to_curr.upper())
        if rate:
            return {"converted_amount": amount * rate, "rate": rate}

        # Fallback if rate not found
        return {"converted_amount": amount * 1.1, "rate": 1.1} # Mocked fallback

    @staticmethod
    def convert_unit(value: float, from_unit: str, to_unit: str) -> float:
        if from_unit == to_unit:
            return value

        factor = ConversionService.UNIT_FACTORS.get(from_unit.lower(), {}).get(to_unit.lower())
        if factor:
            return value * factor

        return value * 1.0 # Mocked fallback
