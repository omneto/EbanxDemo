import decimal

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import Request
from contextlib import asynccontextmanager
from pathlib import Path
from os import getenv
import logging, ngrok, json
from starlette import status
from enum import StrEnum

from models.BankingAgency import BankingAgency

class Event(StrEnum):
    DEPOSIT = 'deposit'
    WITHDRAW = 'withdraw'
    TRANSFER = 'transfer'

with open("secrets.json") as f:
    SECRETS = json.load(f)

NGROK_AUTH_TOKEN = SECRETS['NGROK_AUTH_TOKEN']
NGROK_EDGE = SECRETS['NGROK_EDGE']

logging.basicConfig(level=logging.INFO)

APPLICATION_HOST = "127.0.0.1"
APPLICATION_PORT = 5000

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Setting up Ngrok Tunnel")
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    ngrok.forward(
        addr=APPLICATION_PORT,
        labels=NGROK_EDGE,
        proto="labeled",
    )
    yield
    logging.info("Tearing Down Ngrok Tunnel")
    ngrok.disconnect()

app = FastAPI(lifespan=lifespan)

bank = BankingAgency("EbanxDemo")

@app.get("/")
async def root():
    return {"message": "Hello Ebanx!"}

@app.get("/balance")
async def balance(account_id: str):
    if not bank.check_account_exists(account_id):
        return JSONResponse(
            content={status.HTTP_400_BAD_REQUEST: "0"},
            status_code=status.HTTP_400_BAD_REQUEST)
    account_balance = bank.get_account_balance(account_id)
    return JSONResponse(
            content={"result": str(account_balance)},
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
        return JSONResponse(
                content={"destination": {"id": destination, "balance": str(account_balance)}},
                status_code=status.HTTP_200_OK)
    elif type == Event.WITHDRAW:
        if not bank.check_account_exists(origin):
            return JSONResponse(
                content={status.HTTP_404_NOT_FOUND: "0"},
                status_code=status.HTTP_404_NOT_FOUND)
        account_balance = bank.withdraw_account(origin, amount)
        return JSONResponse(
                content={"origin": {"id": origin, "balance": str(account_balance)}},
                status_code=status.HTTP_200_OK)
    elif type == Event.TRANSFER:
        if not bank.check_account_exists(origin):
            return JSONResponse(
                content={status.HTTP_404_NOT_FOUND: "0"},
                status_code=status.HTTP_404_NOT_FOUND)
        dest_account_balance = bank.transfer_account(origin, amount, destination)
        origin_account_balance = bank.get_account_balance(origin)
        return JSONResponse(
                content={"origin": {"id": origin, "balance": str(origin_account_balance)},
                         "destination": {"id": destination, "balance": str(dest_account_balance)}},
                status_code=status.HTTP_200_OK)

    return JSONResponse(
        content={status.HTTP_400_BAD_REQUEST: "0"},
        status_code=status.HTTP_400_BAD_REQUEST)

@app.post("/reset")
async def reset():
    bank.reset_accounts()
    return JSONResponse(
            content={status.HTTP_200_OK: "OK"},
            status_code=status.HTTP_200_OK)



#if __name__ == "__main__":
#    uvicorn.run("main:app", host=APPLICATION_HOST, port=APPLICATION_PORT, reload=True)