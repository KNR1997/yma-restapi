"""This module defines the main Dispatch API endpoints."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette.responses import JSONResponse

from yma.auth.views import auth_router as auth_router, user_router
from yma.subject.views import router as subject_router
from yma.settings.views import router as settings_router
from yma.course.views import router as course_router
from yma.hall.views import router as hall_router
from yma.guardian.views import router as guardian_router

from yma.auth.service import get_current_user


class ErrorMessage(BaseModel):
    """Represents a single error message."""

    msg: str


class ErrorResponse(BaseModel):
    """Defines the structure for API error responses."""

    detail: list[ErrorMessage] | None = None


api_router = APIRouter(
    prefix="/api/v1",
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
api_router.include_router(
    settings_router, prefix="/settings", tags=["Settings"])

# Private (authenticated) routes
authenticated_api_router = APIRouter(dependencies=[Depends(get_current_user)])
authenticated_api_router.include_router(
    user_router, prefix="/users", tags=["Users"])
authenticated_api_router.include_router(
    subject_router, prefix="/subjects", tags=["Subjects"])
authenticated_api_router.include_router(
    course_router, prefix="/courses", tags=["Courses"])
authenticated_api_router.include_router(
    hall_router, prefix="/halls", tags=["Halls"])
authenticated_api_router.include_router(
    guardian_router, prefix="/guardians", tags=["Guardians"])


# Mount the private router into the main one
api_router.include_router(authenticated_api_router)
