from fastapi import APIRouter, Query
from app.schemas.base import BaseResponse
from app.services.conversion_service import ConversionService

router = APIRouter()

@router.get("/currency", response_model=BaseResponse)
async def convert_currency(
    amount: float = Query(..., description="The amount to convert."),
    from_currency: str = Query(..., description="3-letter ISO code of the source currency."),
    to_currency: str = Query(..., description="3-letter ISO code of the target currency.")
):
    result = await ConversionService.convert_currency(amount, from_currency, to_currency)
    return BaseResponse(status="success", data=result)

@router.get("/unit", response_model=BaseResponse)
async def convert_unit(
    value: float = Query(..., description="The numeric value to convert."),
    from_unit: str = Query(..., description="Source unit (e.g., 'meter')."),
    to_unit: str = Query(..., description="Target unit (e.g., 'foot').")
):
    result = ConversionService.convert_unit(value, from_unit, to_unit)
    return BaseResponse(status="success", data={"result": result})
