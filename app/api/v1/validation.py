from fastapi import APIRouter, Query
from app.schemas.base import BaseResponse
from app.services.validation_service import ValidationService

router = APIRouter()

@router.get("/email", response_model=BaseResponse)
async def validate_email(
    email: str = Query(..., description="The email address to validate.")
):
    result = ValidationService.validate_email(email)
    return BaseResponse(status="success", data=result)

@router.get("/address", response_model=BaseResponse)
async def validate_address(
    address: str = Query(..., description="The physical address to validate.")
):
    result = ValidationService.validate_address(address)
    return BaseResponse(status="success", data=result)
