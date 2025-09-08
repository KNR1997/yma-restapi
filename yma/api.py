"""This module defines the main Dispatch API endpoints."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette.responses import JSONResponse

from yma.auth.views import auth_router as auth_router
from yma.subject.views import router as subject_router

from yma.auth.service import get_current_user


class ErrorMessage(BaseModel):
    """Represents a single error message."""

    msg: str


class ErrorResponse(BaseModel):
    """Defines the structure for API error responses."""

    detail: list[ErrorMessage] | None = None


api_router = APIRouter(
    default_response_class=JSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)

# Public routes
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])

# Private (authenticated) routes
authenticated_api_router = APIRouter(dependencies=[Depends(get_current_user)])
authenticated_api_router.include_router(
    subject_router, prefix="/subjects", tags=["Subjects"])

# Mount the private router into the main one
api_router.include_router(authenticated_api_router)
