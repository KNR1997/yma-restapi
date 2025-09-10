import uuid
import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextvars import ContextVar
from sqlalchemy.orm import scoped_session
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from yma.database.utils import SessionLocal
from yma.exceptions import AppException

from .logging import configure_logging
from yma.api import api_router

log = logging.getLogger(__name__)

# we configure the logging level and format
configure_logging()

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
        except Exception:
            request.state.db.rollback()
            raise   # let exception handlers do their job
            # )
        finally:
            request.state.db.close()
            session.remove()
            _request_id_ctx_var.reset(ctx_token)


app = FastAPI()


# ---- Exception Handlers ----
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    log.warning(f"Handled AppException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    log.error(
        f"Unhandled error on {request.method} {request.url.path}: {exc}",
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={"detail": [{"msg": "Internal Server Error"}]},
    )


# Register middlewares
app.add_middleware(DBSessionMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# we add all API routes to the Web API framework
app.include_router(api_router)
