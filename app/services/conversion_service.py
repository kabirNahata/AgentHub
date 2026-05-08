import httpx
from typing import Dict
from fastapi import HTTPException

class ConversionService:
    UNIT_FACTORS = {
        "meter": {"foot": 3.28084, "inch": 39.3701},
        "kilogram": {"pound": 2.20462},
    }

    @staticmethod
    async def convert_currency(amount: float, from_curr: str, to_curr: str) -> Dict[str, float]:
        from_curr = from_curr.upper()
        to_curr = to_curr.upper()

        if from_curr == to_curr:
            return {"converted_amount": amount, "rate": 1.0}

        async with httpx.AsyncClient(follow_redirects=True) as client:
            # Primary: Frankfurter
            try:
                response = await client.get(
                    "https://api.frankfurter.app/latest",
                    params={"amount": amount, "from": from_curr, "to": to_curr}
                )
                if response.status_code == 200:
                    data = response.json()
                    converted_amount = data["rates"][to_curr]
                    rate = converted_amount / amount if amount != 0 else 1.0
                    return {"converted_amount": converted_amount, "rate": rate}
            except Exception:
                pass

            # Secondary: exchangerate-api.com (Free tier for exotic currencies like NPR)
            try:
                # Note: Free tier uses a slightly different endpoint and base currency approach
                response = await client.get(f"https://api.exchangerate-api.com/v4/latest/{from_curr}")
                if response.status_code == 200:
                    data = response.json()
                    if to_curr in data.get("rates", {}):
                        rate = data["rates"][to_curr]
                        converted_amount = amount * rate
                        return {"converted_amount": converted_amount, "rate": rate}

                if response.status_code == 404:
                     raise HTTPException(status_code=400, detail=f"Invalid currency code: {from_curr} or {to_curr}")

                response.raise_for_status()
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"An error occurred during conversion: {str(e)}")

        raise HTTPException(status_code=400, detail=f"Unsupported currency conversion: {from_curr} to {to_curr}")

    @staticmethod
    def convert_unit(value: float, from_unit: str, to_unit: str) -> float:
        if from_unit == to_unit:
            return value

        factor = ConversionService.UNIT_FACTORS.get(from_unit.lower(), {}).get(to_unit.lower())
        if factor:
            return value * factor

        raise HTTPException(status_code=400, detail=f"Unsupported unit conversion from {from_unit} to {to_unit}")
