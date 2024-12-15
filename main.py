from fastapi import FastAPI
from routers import stock_query, analysis_router, add_data

app = FastAPI()

app.include_router(stock_query.router)
app.include_router(analysis_router.router)
app.include_router(add_data.router)