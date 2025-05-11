import os
import secrets
import logging

from fastapi import FastAPI, Request, Security, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader

from sqlalchemy.exc import SQLAlchemyError

from dotenv import load_dotenv

from routers import stock_query, create_analysis
from routers import check_analysis_route
from routers import return_db_contents


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

# API-KEY config
API_KEY_NAME = "X-API-KEY"
SECRET_KEY = os.getenv("SECRET_API_KEY")

if not SECRET_KEY:
    logging.error("FATAL ERROR: SECRET_API_KEY environment variable not set.")
    # Option 1: Raise error to prevent startup
    raise ValueError("SECRET_API_KEY environment variable not set. Application cannot start securely.")

api_key_header_auth = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header:str = Security(api_key_header_auth)):
    """
    Dependency function to validate the API key from the X-API-Key header.
    Raises HTTPException 401 if the key is missing or invalid.
    """
    if not api_key_header:
        logging.warning(f"API Key missing from '{API_KEY_NAME}' header.")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"API Key required in '{API_KEY_NAME}' header.",
            headers={"WWW-Authenticate": "API Key"},
        )
    
    if not secrets.compare_digest(api_key_header, SECRET_KEY):
        logging.warning("Invalid API Key received.")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key provided.",
            headers={"WWW-Authenticate": "API Key"},
        )
    
    return api_key_header

app = FastAPI(dependencies=[Depends(get_api_key)])

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler():
    # Optionally log the error here for debugging/monitoring:
    # logger.error(f"SQLAlchemy error occurred: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal database error occurred. Please try again later."}
    )

@app.exception_handler(Exception)
async def generic_exception_handler():
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