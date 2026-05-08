from fastapi import APIRouter
from typing import List
from app.schemas.base import RegistryEntry, BaseResponse

router = APIRouter()

# In a real app, this might be dynamic. For v1, we'll keep it as a registry of our core services.
SERVICES_REGISTRY = [
    {
        "name": "Currency Conversion",
        "endpoint": "/api/v1/convert/currency",
        "description": "Convert between different currencies using real-time rates.",
        "input_schema": {
            "type": "object",
            "properties": {
                "from_currency": {"type": "string", "description": "3-letter ISO currency code."},
                "to_currency": {"type": "string", "description": "3-letter ISO currency code."},
                "amount": {"type": "number", "description": "The amount to convert."}
            }
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "converted_amount": {"type": "number"},
                "rate": {"type": "number"}
            }
        }
    },
    {
        "name": "Unit Conversion",
        "endpoint": "/api/v1/convert/unit",
        "description": "Convert between different units of measurement.",
        "input_schema": {
            "type": "object",
            "properties": {
                "value": {"type": "number"},
                "from_unit": {"type": "string"},
                "to_unit": {"type": "string"}
            }
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "result": {"type": "number"}
            }
        }
    }
]

@router.get("/registry", response_model=BaseResponse, description="Service Discovery: Returns a list of all available agent-readable services.")
async def get_registry():
    return BaseResponse(
        status="success",
        data={"services": SERVICES_REGISTRY}
    )
