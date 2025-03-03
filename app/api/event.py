from fastapi import APIRouter, Depends
from fastapi.responses import Response
from fastapi import Request
from starlette import status
from app.utils import Event
import decimal

from app.api.dependencies import Dependencies
from app.src.banking_agency.BankingAgencyService import BankingAgencyService

router = APIRouter()

@router.post("/event")
async def event(request: Request, banking_agency_service: BankingAgencyService = Depends(Dependencies.get_banking_agency_service)):
    data = await request.json()

    type = data['type'] if 'type' in data else None
    origin = data['origin'] if 'origin' in data else None
    destination = data['destination'] if 'destination' in data else None
    amount = decimal.Decimal(data['amount']) if 'amount' in data else None

    if type == Event.DEPOSIT:
        banking_agency_service.validate_deposit_event(origin, destination)
        account_balance = await banking_agency_service.deposit_account(destination, amount)
        response_content = f'{{"destination": {{"id": "{destination}", "balance":{str(account_balance)}}}}}'
        return Response(
            content=response_content,
            status_code=status.HTTP_201_CREATED)
    elif type == Event.WITHDRAW:
        banking_agency_service.validate_withdraw_event(origin, destination)
        if not await banking_agency_service.check_account_exists(origin):
            return Response(
                content="0",
                status_code=status.HTTP_404_NOT_FOUND)
        account_balance = await banking_agency_service.withdraw_account(origin, amount)
        response_content = f'{{"origin": {{"id": "{origin}", "balance":{str(account_balance)}}}}}'
        return Response(
            content=response_content,
            status_code=status.HTTP_201_CREATED)
    elif type == Event.TRANSFER:
        banking_agency_service.validate_transfer_event(origin, amount, destination)
        if not await banking_agency_service.check_account_exists(origin):
            return Response(
                content="0",
                status_code=status.HTTP_404_NOT_FOUND)
        dest_account_balance = await banking_agency_service.transfer_account(origin, amount, destination)
        origin_account_balance = await banking_agency_service.get_account_balance(origin)
        response_content = f'{{"origin": {{"id": "{origin}", "balance":{str(origin_account_balance)}}}, '
        response_content = response_content + f'"destination": {{"id": "{destination}", "balance":{str(dest_account_balance)}}}}}'
        return Response(
            content=response_content,
            status_code=status.HTTP_201_CREATED)

    return Response(
        content="0",
        status_code=status.HTTP_400_BAD_REQUEST)