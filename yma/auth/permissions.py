import logging
from abc import ABC, abstractmethod
import json

from fastapi import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from yma.auth.service import get_current_user
from yma.enums import UserRoles

log = logging.getLogger(__name__)


def any_permission(permissions: list, request: Request) -> bool:
    for p in permissions:
        try:
            p(request=request)
            return True
        except HTTPException:
            pass
    return False


class BasePermission(ABC):
    """
    Abstract base permission for the Student Management System.
    """

    user_error_msg = [{"msg": "User not found. Please contact admin."}]
    user_error_code = HTTP_404_NOT_FOUND

    role_error_msg = [
        {"msg": "You don't have permission to access this resource."}]
    role_error_code = HTTP_403_FORBIDDEN

    role = None

    @abstractmethod
    def has_required_permissions(self, request: Request) -> bool: ...

    def __init__(self, request: Request):
        user = get_current_user(request=request)
        if not user:
            raise HTTPException(
                status_code=self.user_error_code, detail=self.user_error_msg)

        self.role = user.role  # Assuming your User model has a `.role`

        if not self.has_required_permissions(request):
            raise HTTPException(
                status_code=self.role_error_code, detail=self.role_error_msg)


class PermissionsDependency(object):
    """
    Permission dependency that is used to define and check all the permission
    classes from one place inside route definition.

    Use it as an argument to FastAPI's `Depends` as follows:

    .. code-block:: python

        app = FastAPI()

        @app.get(
            "/teapot/",
            dependencies=[Depends(
                PermissionsDependency([TeapotUserAgentPermission]))]
        )
        async def teapot() -> dict:
            return {"teapot": True}
    """

    def __init__(self, permissions_classes: list):
        self.permissions_classes = permissions_classes

    def __call__(self, request: Request):
        for permission_class in self.permissions_classes:
            permission_class(request=request)


class AdminPermission(BasePermission):
    def has_required_permissions(self, request: Request) -> bool:
        return self.role in [UserRoles.super_admin, UserRoles.admin]


class TeacherPermission(BasePermission):
    def has_required_permissions(self, request: Request) -> bool:
        return self.role in [UserRoles.teacher, UserRoles.admin]


class StudentPermission(BasePermission):
    def has_required_permissions(self, request: Request) -> bool:
        return self.role in [UserRoles.student, UserRoles.teacher, UserRoles.admin]
