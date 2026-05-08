from fastapi import APIRouter, Query
from app.schemas.base import BaseResponse
from app.services.web_adapter_service import WebAdapterService

router = APIRouter()

@router.get("/proxy", response_model=BaseResponse, description="Web Adapter: Converts a human-facing website into a clean, agent-readable JSON response.")
async def adapter_proxy(
    url: str = Query(..., description="The URL of the website to adapt.")
):
    result = await WebAdapterService.fetch_structured_data(url)
    return BaseResponse(status="success", data=result)
