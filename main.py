from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routers import stock_query, create_analysis
from routers import check_analysis_route
from sqlalchemy.exc import SQLAlchemyError
import logging

logging.basicConfig(filename="errors.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    # Optionally log the error here for debugging/monitoring:
    # logger.error(f"SQLAlchemy error occurred: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal database error occurred. Please try again later."}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # Log the error as needed
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."}
    )

app.include_router(stock_query.router)
app.include_router(check_analysis_route.router)
app.include_router(create_analysis.router)