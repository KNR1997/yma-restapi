import typing
import uuid
import logging
from typing import Union

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextvars import ContextVar
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from starlette.responses import Response, StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from .logging import configure_logging
from yma.api import api_router

log = logging.getLogger(__name__)

# we configure the logging level and format
configure_logging()

DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/fastapi_starter"
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# ContextVar for request ID
REQUEST_ID_CTX_KEY = "request_id"
_request_id_ctx_var: ContextVar[str | None] = ContextVar(
    REQUEST_ID_CTX_KEY, default=None)


def get_request_id() -> str | None:
    return _request_id_ctx_var.get()


class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = str(uuid.uuid4())
        ctx_token = _request_id_ctx_var.set(request_id)

        session = scoped_session(SessionLocal, scopefunc=get_request_id)
        request.state.db = session()

        try:
            response = await call_next(request)
            request.state.db.commit()
            return response
        except Exception as e:
            # log.exception(f"Request {request_id} failed: {e}")
            request.state.db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal Server Error"},
            )
        finally:
            request.state.db.close()
            session.remove()
            _request_id_ctx_var.reset(ctx_token)


async def validation_exception_handler(request: Request, exc):
    log.warning(
        f"Validation error on {request.method} {request.url.path} | {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


async def generic_exception_handler(request: Request, exc: Exception):
    log.error(
        f"Unhandled error on {request.method} {request.url.path} | {exc}",
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> StreamingResponse:
        try:
            response = await call_next(request)
        except ValidationError as e:
            log.exception(e)
            response = JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={
                    "detail": e.errors()}
            )
        except ValueError as e:
            log.exception(e)
            response = JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"detail": [
                    {"msg": "Unknown", "loc": ["Unknown"], "type": "Unknown"}]},
            )
        except Exception as e:
            print('exception happends---------')
            log.exception(e)
            response = JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": [
                    {"msg": "Unknown", "loc": ["Unknown"], "type": "Unknown"}]},
            )

        return response


app = FastAPI()

# CORS settings - we'll configure this in code instead of from env
CORS_ORIGINS: typing.List[str] = ["*"]
CORS_ALLOW_CREDENTIALS: bool = True
CORS_ALLOW_METHODS: typing.List[str] = ["*"]
CORS_ALLOW_HEADERS: typing.List[str] = ["*"]


# Register middlewares
app.add_middleware(DBSessionMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
)

# Register exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


# we add all API routes to the Web API framework
app.include_router(api_router)
