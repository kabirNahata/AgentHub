from fastapi import Header, HTTPException, status
from app.core.config import settings

async def verify_api_key(x_agenthub_key: str = Header(..., alias="X-AgentHub-Key")):
    if x_agenthub_key not in settings.api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
    return x_agenthub_key
