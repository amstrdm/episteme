from fastapi import FastAPI
from routers import stock_query, add_data, check_existing_analysis, create_analysis

app = FastAPI()

app.include_router(stock_query.router)
app.include_router(check_existing_analysis.router)
app.include_router(create_analysis.router)