import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from pathlib import Path
from os import getenv
import logging, ngrok, json

from models.Bank import Bank

BASE_DIR = Path(__file__).resolve().parent

print(BASE_DIR)

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

bank = Bank("EbanxDemo")

@app.get("/")
async def root():
    return {"message": "Hello Ebanx!"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

if __name__ == "__main__":
    uvicorn.run("main:app", host=APPLICATION_HOST, port=APPLICATION_PORT, reload=True)