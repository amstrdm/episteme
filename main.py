from fastapi import FastAPI
from routers import stock_query

app = FastAPI()

app.include_router(stock_query.router)