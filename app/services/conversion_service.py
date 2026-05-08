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
            try:
                response = await client.get(
                    f"https://api.frankfurter.dev/v1/latest",
                    params={"amount": amount, "from": from_curr, "to": to_curr}
                )
                if response.status_code == 404:
                    raise HTTPException(status_code=400, detail=f"Invalid currency code: {from_curr} or {to_curr}")
                response.raise_for_status()
                data = response.json()

                converted_amount = data["rates"][to_curr]
                # Avoid division by zero if amount is 0
                rate = converted_amount / amount if amount != 0 else 1.0

                return {
                    "converted_amount": converted_amount,
                    "rate": rate
                }
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=response.status_code, detail=f"External API error: {str(e)}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"An error occurred during conversion: {str(e)}")

    @staticmethod
    def convert_unit(value: float, from_unit: str, to_unit: str) -> float:
        if from_unit == to_unit:
            return value

        factor = ConversionService.UNIT_FACTORS.get(from_unit.lower(), {}).get(to_unit.lower())
        if factor:
            return value * factor

        raise HTTPException(status_code=400, detail=f"Unsupported unit conversion from {from_unit} to {to_unit}")
