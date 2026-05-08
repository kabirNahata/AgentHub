from fastapi import APIRouter
from app.schemas.base import BaseResponse

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
                "amount": {"type": "number", "description": "The amount to convert."},
                "from_currency": {"type": "string", "description": "3-letter ISO currency code."},
                "to_currency": {"type": "string", "description": "3-letter ISO currency code."}
            },
            "required": ["amount", "from_currency", "to_currency"]
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
                "value": {"type": "number", "description": "The numeric value to convert."},
                "from_unit": {"type": "string", "description": "Source unit (e.g., 'meter')."},
                "to_unit": {"type": "string", "description": "Target unit (e.g., 'foot')."}
            },
            "required": ["value", "from_unit", "to_unit"]
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "result": {"type": "number"}
            }
        }
    },
    {
        "name": "Email Validation",
        "endpoint": "/api/v1/validate/email",
        "description": "Check if an email address is syntactically valid.",
        "input_schema": {
            "type": "object",
            "properties": {
                "email": {"type": "string", "description": "The email address to validate."}
            },
            "required": ["email"]
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "is_valid": {"type": "boolean"}
            }
        }
    },
    {
        "name": "Address Validation",
        "endpoint": "/api/v1/validate/address",
        "description": "Basic validation of a physical address.",
        "input_schema": {
            "type": "object",
            "properties": {
                "address": {"type": "string", "description": "The physical address to validate."}
            },
            "required": ["address"]
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "is_valid": {"type": "boolean"}
            }
        }
    },
    {
        "name": "Timezone Lookup",
        "endpoint": "/api/v1/lookup/timezone",
        "description": "Resolve a location name to its IANA timezone.",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "The name of the location."}
            },
            "required": ["location"]
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string"},
                "timezone": {"type": "string"}
            }
        }
    },
    {
        "name": "Jurisdiction Lookup",
        "endpoint": "/api/v1/lookup/jurisdiction",
        "description": "Check jurisdictional information for a location.",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "The name of the location."}
            },
            "required": ["location"]
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string"},
                "info": {"type": "object"}
            }
        }
    },
    {
        "name": "Factual Lookup",
        "endpoint": "/api/v1/lookup/facts",
        "description": "Query factual information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The factual question."}
            },
            "required": ["query"]
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "answer": {"type": "string"}
            }
        }
    },
    {
        "name": "Web Adapter Proxy",
        "endpoint": "/api/v1/adapter/proxy",
        "description": "Converts a human-facing website into clean, agent-readable JSON.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The URL of the website to adapt."}
            },
            "required": ["url"]
        },
        "output_schema": {
            "type": "object"
        }
    }
]

@router.get("/registry", response_model=BaseResponse, description="Service Discovery: Returns a list of all available agent-readable services.")
async def get_registry():
    return BaseResponse(
        status="success",
        data={"services": SERVICES_REGISTRY}
    )
