import decimal
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi import Request
from starlette import status
from enum import StrEnum

from models.BankingAgency import BankingAgency

class Event(StrEnum):
    DEPOSIT = 'deposit'
    WITHDRAW = 'withdraw'
    TRANSFER = 'transfer'

app = FastAPI()

bank = BankingAgency("EbanxDemo")

@app.get("/")
async def root():
    return {"message": "Hello Ebanx!"}

@app.get("/balance")
async def balance(account_id: str):
    if not bank.check_account_exists(account_id):
        return Response(
            content="0",
            status_code=status.HTTP_404_NOT_FOUND)
    account_balance = bank.get_account_balance(account_id)
    return Response(
            content=str(account_balance),
            status_code=status.HTTP_200_OK)

@app.post("/event")
async def event(request: Request):
    data = await request.json()

    type = data['type'] if 'type' in data else None
    origin =  data['origin']  if 'origin' in data else None
    destination = data['destination'] if 'destination' in data else None
    amount = decimal.Decimal(data['amount']) if 'amount' in data else decimal.Decimal('0')

    if type == Event.DEPOSIT:
        account_balance = bank.deposit_account(destination, amount)
        response_content =f'{{"destination": {{"id": "{destination}", "balance":{str(account_balance)}}}}}'
        return Response(
                content=response_content,
                status_code=status.HTTP_201_CREATED)
    elif type == Event.WITHDRAW:
        if not bank.check_account_exists(origin):
            return Response(
                content="0",
                status_code=status.HTTP_404_NOT_FOUND)
        account_balance = bank.withdraw_account(origin, amount)
        response_content = f'{{"origin": {{"id": "{origin}", "balance":{str(account_balance)}}}}}'
        return Response(
                content=response_content,
                status_code=status.HTTP_201_CREATED)
    elif type == Event.TRANSFER:
        if not bank.check_account_exists(origin):
            return Response(
                content="0",
                status_code=status.HTTP_404_NOT_FOUND)
        dest_account_balance = bank.transfer_account(origin, amount, destination)
        origin_account_balance = bank.get_account_balance(origin)
        response_content = f'{{"origin": {{"id": "{origin}", "balance":{str(origin_account_balance)}}}, '
        response_content = response_content + f'"destination": {{"id": "{destination}", "balance":{str(dest_account_balance)}}}}}'
        return Response(
                content=response_content,
                status_code=status.HTTP_201_CREATED)

    return Response(
        content="0",
        status_code=status.HTTP_400_BAD_REQUEST)

@app.post("/reset")
async def reset():
    bank.reset_accounts()
    return Response(
            content="OK",
            status_code=status.HTTP_200_OK)

