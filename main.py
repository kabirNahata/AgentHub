import os
import time
from typing import Optional

import httpx
import pint
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException, Query
from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")

    app_api_key: str = "agenthub_test_key"
    open_exchange_rates_key: Optional[str] = None
    abstract_api_key: Optional[str] = None
    timezonedb_key: Optional[str] = None

settings = Settings()
app = FastAPI(title="AgentHub", version="0.1")
ureg = pint.UnitRegistry()

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.app_api_key:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_api_key

@app.get("/")
async def root():
    return {"message": "Welcome to AgentHub v0.1 API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

# Currency Conversion
class CurrencyResponse(BaseModel):
    rate: float
    converted_amount: float
    timestamp: int

@app.get("/convert/currency", response_model=CurrencyResponse)
async def convert_currency(
    amount: float = Query(..., description="Amount to convert"),
    from_currency: str = Query(..., alias="from", description="Source currency code (e.g. USD)"),
    to_currency: str = Query(..., alias="to", description="Target currency code (e.g. EUR)"),
    api_key: str = Depends(verify_api_key)
):
    if not settings.open_exchange_rates_key:
        # Fallback for dev/missing key
        rate = 1.0 # Mock rate
        if from_currency == "USD" and to_currency == "NPR":
            rate = 133.0
        return {
            "rate": rate,
            "converted_amount": amount * rate,
            "timestamp": int(time.time())
        }

    try:
        url = f"https://openexchangerates.org/api/latest.json?app_id={settings.open_exchange_rates_key}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

        rates = data.get("rates", {})
        if from_currency not in rates or to_currency not in rates:
            raise HTTPException(status_code=400, detail="Invalid currency code")

        # OER base is usually USD
        from_rate = rates[from_currency]
        to_rate = rates[to_currency]

        actual_rate = to_rate / from_rate

        return {
            "rate": actual_rate,
            "converted_amount": amount * actual_rate,
            "timestamp": data.get("timestamp", int(time.time()))
        }
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))

# Email Validation
class EmailResponse(BaseModel):
    valid: bool
    reason: str

@app.get("/validate/email", response_model=EmailResponse)
async def validate_email(
    email: str = Query(..., description="Email address to validate"),
    api_key: str = Depends(verify_api_key)
):
    if not settings.abstract_api_key:
        # Fallback/Mock
        is_valid = "@" in email and "." in email.split("@")[-1]
        return {
            "valid": is_valid,
            "reason": "Basic format check (Mock)" if is_valid else "Invalid format (Mock)"
        }

    try:
        url = f"https://emailvalidation.abstractapi.com/v1/?api_key={settings.abstract_api_key}&email={email}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

        # Abstract API returns quality_score, is_valid_format, etc.
        is_valid = data.get("is_valid_format", {}).get("value", False) and data.get("deliverability") == "DELIVERABLE"

        return {
            "valid": is_valid,
            "reason": f"Quality score: {data.get('quality_score')}"
        }
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))

# Timezone Resolution
class TimezoneResponse(BaseModel):
    timezone_name: str
    utc_offset: str
    local_time: str

def format_offset(seconds: int) -> str:
    sign = "+" if seconds >= 0 else "-"
    seconds = abs(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{sign}{hours:02d}:{minutes:02d}"

@app.get("/resolve/timezone", response_model=TimezoneResponse)
async def resolve_timezone(
    location: str = Query(..., alias="city", description="City name or coordinates"),
    api_key: str = Depends(verify_api_key)
):
    if not settings.timezonedb_key:
        # Fallback/Mock
        if "Kathmandu" in location or "27.7" in location:
            return {
                "timezone_name": "Asia/Kathmandu",
                "utc_offset": "+05:45",
                "local_time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time() + 5.75 * 3600))
            }
        return {
            "timezone_name": "UTC",
            "utc_offset": "+00:00",
            "local_time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        }

    try:
        if "," in location:
            lat, lng = location.split(",")
            url = f"http://api.timezonedb.com/v2.1/get-time-zone?key={settings.timezonedb_key}&format=json&by=position&lat={lat.strip()}&lng={lng.strip()}"
        else:
            if "/" in location:
                url = f"http://api.timezonedb.com/v2.1/get-time-zone?key={settings.timezonedb_key}&format=json&by=zone&zone={location}"
            else:
                raise HTTPException(status_code=400, detail="Please provide coordinates (lat,lng) or a valid Timezone Name (e.g. Asia/Kathmandu)")

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

        if data.get("status") != "OK":
            raise HTTPException(status_code=400, detail=data.get("message", "Error from TimeZoneDB"))

        return {
            "timezone_name": data.get("zoneName"),
            "utc_offset": format_offset(int(data.get("gmtOffset"))),
            "local_time": data.get("formatted")
        }
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))

# Unit Conversion
class UnitResponse(BaseModel):
    converted_value: float
    unit_label: str

@app.get("/convert/unit", response_model=UnitResponse)
async def convert_unit(
    value: float = Query(..., description="Value to convert"),
    from_unit: str = Query(..., description="Source unit (e.g. meter)"),
    to_unit: str = Query(..., description="Target unit (e.g. feet)"),
    api_key: str = Depends(verify_api_key)
):
    try:
        quantity = value * ureg(from_unit)
        converted = quantity.to(to_unit)
        return {
            "converted_value": converted.magnitude,
            "unit_label": to_unit
        }
    except pint.UndefinedUnitError as e:
        raise HTTPException(status_code=400, detail=f"Undefined unit: {str(e)}")
    except pint.DimensionalityError as e:
        raise HTTPException(status_code=400, detail=f"Incompatible units: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
