import logging
from abc import ABC, abstractmethod

from fastapi import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from yma.auth.utils import get_current_user
from yma.enums import UserRole

log = logging.getLogger(__name__)


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

    async def __call__(self, request: Request):
        """
        Async entry point for permission validation.
        This is what FastAPI's dependency system will call.
        """
        user = await get_current_user(request=request)
        if not user:
            raise HTTPException(
                status_code=self.user_error_code, detail=self.user_error_msg
            )

        self.role = user.role  # Assuming your User model has a `.role`

        if not self.has_required_permissions(request):
            raise HTTPException(
                status_code=self.role_error_code, detail=self.role_error_msg
            )


class PermissionsDependency(object):
    """
    Permission dependency that is used to define and check all the permission
    classes from one place inside route definition.
    """

    def __init__(self, permissions_classes: list):
        self.permissions_classes = permissions_classes

    async def __call__(self, request: Request):
        for permission_class in self.permissions_classes:
            permission = permission_class()
            await permission(request=request)


class AdminPermission(BasePermission):
    def has_required_permissions(self, request: Request) -> bool:
        return self.role in [UserRole.super_admin, UserRole.admin]


class TeacherPermission(BasePermission):
    def has_required_permissions(self, request: Request) -> bool:
        return self.role in [UserRole.teacher, UserRole.admin]


class StudentPermission(BasePermission):
    def has_required_permissions(self, request: Request) -> bool:
        return self.role in [UserRole.student, UserRole.teacher, UserRole.admin]
