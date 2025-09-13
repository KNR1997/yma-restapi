from datetime import datetime
from typing import Optional
from uuid import UUID
import bcrypt

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, EmailStr, field_validator
from tortoise import fields, models

from yma.enums import UserRole
from yma.models import Pagination


class YMAUser(models.Model):
    id = fields.UUIDField(pk=True, index=True)
    full_name = fields.TextField(null=True)
    first_name = fields.TextField(null=True)
    last_name = fields.TextField(null=True)
    name_with_initials = fields.TextField(null=True)
    username = fields.CharField(max_length=30, null=True)
    email = fields.CharField(max_length=191, unique=True, index=True)
    phone = fields.CharField(max_length=20, null=True)
    nic = fields.TextField(max_length=30, null=True)
    password = fields.TextField()
    is_active = fields.BooleanField(default=True)
    last_login = fields.DatetimeField(null=True)
    role = fields.CharEnumField(UserRole)

    class Meta:
        table = "user"


def hash_password(password: str):
    """Hash a password using bcrypt."""
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


class UserLogin(BaseModel):
    email: str
    password: str


class JWTPayload(BaseModel):
    user_id: str
    email: str
    # is_superuser: bool
    exp: datetime


class JWTOut(BaseModel):
    token: str
    email: str
    username: str
    role: str
    permissions: list[str]


class UserRegister(UserLogin):
    full_name: str
    first_name: str
    last_name: str
    name_with_initials: str
    username: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.student


class UserPasswordUpdate(BaseModel):
    """Pydantic model for password updates only."""

    current_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v):
        """Validate the new password for length and complexity."""
        if not v or len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        if not (any(c.isupper() for c in v) and any(c.islower() for c in v)):
            raise ValueError(
                "Password must contain both uppercase and lowercase characters")
        return v

    @field_validator("current_password")
    @classmethod
    def password_required(cls, v):
        """Ensure the current password is provided."""
        if not v:
            raise ValueError("Current password is required")
        return v


class AdminPasswordReset(BaseModel):
    """Pydantic model for admin password resets."""

    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v):
        """Validate the new password for length and complexity."""
        if not v or len(v) < 8:
            print('less than 8 characters')
            raise RequestValidationError(
                "Password must be at least 8 characters long")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        if not (any(c.isupper() for c in v) and any(c.islower() for c in v)):
            raise ValueError(
                "Password must contain both uppercase and lowercase characters")
        return v


class UserCreate(BaseModel):
    """Pydantic model for creating a new user."""

    full_name: str
    first_name: str
    last_name: str
    name_with_initials: str
    email: EmailStr
    password: str
    role: Optional[str] = None

    @field_validator("password", mode="before")
    @classmethod
    def hash(cls, v):
        """Hash the password before storing."""
        return hash_password(str(v))


class UserUpdate(BaseModel):
    """Pydantic model for updating user data."""

    full_name: str
    first_name: str
    last_name: str
    name_with_initials: str
    nic: str | None = None
    username: str
    email: EmailStr
    role: str | None = None


class UserRead(BaseModel):
    id: UUID
    full_name: str
    first_name: str | None
    last_name: str | None
    name_with_initials: str | None
    nic: str | None
    username: str | None
    email: EmailStr
    role: UserRole

    model_config = {
        "from_attributes": True
    }


class UserLoginResponse(BaseModel):
    token: str
    role: str
    email: EmailStr
    full_name: str
    permissions: list[str]


class UserPagination(Pagination):
    data: list[UserRead]
