from fastapi import FastAPI
from routers import stock_query, create_analysis
from routers import check_analysis_route

app = FastAPI()

app.include_router(stock_query.router)
app.include_router(check_analysis_route.router)
app.include_router(create_analysis.router)