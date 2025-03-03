from fastapi import FastAPI
from .api import balance, event, reset

app = FastAPI()
app.include_router(balance.router)
app.include_router(event.router)
app.include_router(reset.router)

