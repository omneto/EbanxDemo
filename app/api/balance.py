from fastapi import APIRouter, Depends
from starlette import status
from fastapi.responses import Response

from app.api.dependencies import Dependencies
from app.src.banking_agency.BankingAgencyService import BankingAgencyService


router = APIRouter()

@router.get("/balance")
async def balance(account_id: str, banking_agency_service: BankingAgencyService = Depends(Dependencies.get_banking_agency_service)):
    if not await banking_agency_service.check_account_exists(account_id):
        return Response(
            content="0",
            status_code=status.HTTP_404_NOT_FOUND)
    account_balance = await banking_agency_service.get_account_balance(account_id)
    return Response(
            content=str(account_balance),
            status_code=status.HTTP_200_OK)