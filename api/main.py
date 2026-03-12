from fastapi import FastAPI
from api.routes import transactions

app = FastAPI()

app.include_router(transactions.router)