from fastapi import APIRouter, Depends
from starlette import status
from fastapi.responses import Response

from app.api.dependencies import Dependencies
from app.src.banking_agency.BankingAgencyService import BankingAgencyService

router = APIRouter()

@router.post("/reset")
async def reset(banking_agency_service: BankingAgencyService = Depends(Dependencies.get_banking_agency_service)):
    await banking_agency_service.reset_accounts()
    return Response(
        content="OK",
        status_code=status.HTTP_200_OK)