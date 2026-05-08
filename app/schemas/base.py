from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class AgentReadyCertification(BaseModel):
    is_agent_ready: bool = Field(
        True,
        description="Indicates if the service meets the AgentReady standard (stable schemas, machine-readable docs)."
    )
    schema_version: str = Field("0.1", description="The version of the response schema.")

class BaseResponse(BaseModel):
    status: str = Field(..., description="The status of the request (e.g., 'success', 'error').")
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="The ISO-formatted UTC timestamp when the response was generated."
    )
    agent_info: AgentReadyCertification = Field(default_factory=AgentReadyCertification)
    data: Optional[Any] = Field(None, description="The structured data returned by the service.")
    error: Optional[Dict[str, Any]] = Field(None, description="Detailed error information for machine consumption.")

class RegistryEntry(BaseModel):
    name: str = Field(..., description="The name of the service.")
    endpoint: str = Field(..., description="The API endpoint URL.")
    description: str = Field(..., description="What the service does.")
    input_schema: Dict[str, Any] = Field(..., description="JSON Schema for the expected input.")
    output_schema: Dict[str, Any] = Field(..., description="JSON Schema for the expected output.")
