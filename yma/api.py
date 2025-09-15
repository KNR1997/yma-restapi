"""This module defines the main YMA API endpoints."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette.responses import JSONResponse

from yma.auth.utils import get_current_user
from yma.auth.views import auth_router
from yma.auth.views import user_router
from yma.course.views import router as course_router
from yma.enrollment.views import router as enrollment_router
from yma.event.views import router as event_router
from yma.guardian.views import router as guardian_router
from yma.hall.views import router as hall_router
from yma.student.views import router as student_router
from yma.subject.views import router as subject_router
from yma.settings.views import router as settings_router
from yma.api_log.views import router as api_log_router
from yma.payments.views import router as payments_router


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
api_router.include_router(settings_router, prefix="/settings", tags=["Settings"])

# Private (authenticated) routes
authenticated_api_router = APIRouter(dependencies=[Depends(get_current_user)])
authenticated_api_router.include_router(user_router, prefix="/users", tags=["Users"])
authenticated_api_router.include_router(subject_router, prefix="/subjects", tags=["Subject"])
authenticated_api_router.include_router(course_router, prefix="/courses", tags=["Course"])
authenticated_api_router.include_router(enrollment_router, prefix="/enrollments", tags=["Enrollment"])
authenticated_api_router.include_router(event_router, prefix="/events", tags=["Event"])
authenticated_api_router.include_router(guardian_router, prefix="/guardians", tags=["Guardian"])
authenticated_api_router.include_router(hall_router, prefix="/halls", tags=["Hall"])
authenticated_api_router.include_router(student_router, prefix="/students", tags=["Student"])
authenticated_api_router.include_router(api_log_router, prefix="/apis", tags=["Api"])
authenticated_api_router.include_router(payments_router, prefix="/payments", tags=["Payments"])

# Mount the private router into the main one
api_router.include_router(authenticated_api_router)
