from fastapi import APIRouter, Query
from app.schemas.base import BaseResponse
from app.services.lookup_service import LookupService

router = APIRouter()

@router.get("/timezone", response_model=BaseResponse)
async def resolve_timezone(
    location: str = Query(..., description="The name of the location to resolve timezone for.")
):
    result = await LookupService.resolve_timezone(location)
    return BaseResponse(status="success", data=result)

@router.get("/jurisdiction", response_model=BaseResponse)
async def check_jurisdiction(
    location: str = Query(..., description="The name of the location to check jurisdiction for.")
):
    result = LookupService.check_jurisdiction(location)
    return BaseResponse(status="success", data=result)

@router.get("/facts", response_model=BaseResponse)
async def factual_lookup(
    query: str = Query(..., description="The factual question to answer.")
):
    result = LookupService.factual_lookup(query)
    return BaseResponse(status="success", data=result)
