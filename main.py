from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routers import stock_query, create_analysis
from routers import check_analysis_route
from routers import return_db_contents
from sqlalchemy.exc import SQLAlchemyError
import logging
from dotenv import load_dotenv
import os

ENV_PATH = os.getenv("ENV_PATH")
load_dotenv(ENV_PATH)

FRONTEND_URL = os.getenv("FRONTEND_URL")

# Set up the root logger to capture all messages (or as needed)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create a handler for error-level messages (or above)
error_handler = logging.FileHandler('errors.log', encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
error_handler.setFormatter(error_formatter)
logger.addHandler(error_handler)

# Create a handler for warning-level messages (or above)
warning_handler = logging.FileHandler('warnings.log', encoding='utf-8')
warning_handler.setLevel(logging.WARNING)
warning_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
warning_handler.setFormatter(warning_formatter)
logger.addHandler(warning_handler)


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

if FRONTEND_URL:
    origins.append(FRONTEND_URL)

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(stock_query.router)
app.include_router(check_analysis_route.router)
app.include_router(create_analysis.router)
app.include_router(return_db_contents.router)