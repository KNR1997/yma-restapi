import os
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse
from tortoise.contrib.fastapi import register_tortoise
from dotenv import load_dotenv

from yma.api import api_router
from yma.config import TORTOISE_ORM
from yma.exceptions import BaseAppException

from .logging import configure_logging

log = logging.getLogger(__name__)

# we configure the logging level and format
configure_logging()

app = FastAPI()

# Global exception handler


@app.exception_handler(BaseAppException)
async def app_exception_handler(request, exc):
    log.error("Application error: %s", exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "field": getattr(exc, "field", None)  # for field-specific errors
        }
    )


# Register middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load environment variables from .env file
load_dotenv()


# --------- MySQL Config ---------
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,   # ❌ stop auto-creating tables
    add_exception_handlers=True,
)

app.include_router(api_router)
