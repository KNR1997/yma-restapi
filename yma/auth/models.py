import string
import secrets
from datetime import datetime, timedelta

import bcrypt
from jose import jwt
from pydantic import BaseModel, EmailStr
from pydantic import field_validator

from yma.config import (
    DISPATCH_JWT_SECRET,
    DISPATCH_JWT_ALG,
    DISPATCH_JWT_EXP,
)
from sqlalchemy import Column, Enum, String, Integer
from yma.database.core import Base
from yma.models import TimeStampMixin, YMABase
from yma.enums import UserRoles
from .security import verify_password


def generate_password():
    """Generate a random, strong password with at least one lowercase, one uppercase, and three digits."""
    alphanumeric = string.ascii_letters + string.digits
    while True:
        password = "".join(secrets.choice(alphanumeric) for i in range(10))
        # Ensure password meets complexity requirements
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >= 3
        ):
            break
    return password


def hash_password(password: str):
    """Hash a password using bcrypt."""
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


class YMAUser(Base, TimeStampMixin):
    """SQLAlchemy model for a YMA user."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(200), nullable=False)
    email = Column(String(100), unique=True)
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRoles), default=UserRoles.student, nullable=False)

    def verify_password(self, password: str) -> bool:
        return verify_password(password, self.password)

    @property
    def token(self):
        now = datetime.utcnow()
        exp = now + timedelta(seconds=DISPATCH_JWT_EXP)
        payload = {"sub": self.email, "role": self.role.value, "exp": exp}
        return jwt.encode(payload, DISPATCH_JWT_SECRET, algorithm=DISPATCH_JWT_ALG)


class UserBase(YMABase):
    """Base Pydantic model for user data."""

    email: EmailStr

    @field_validator("email")
    @classmethod
    def email_required(cls, v):
        """Ensure the email field is not empty."""
        if not v:
            raise ValueError("Must not be empty string and must be a email")
        return v


class UserLogin(BaseModel):
    email: str
    password: str


class UserRegister(UserLogin):
    full_name: str
    email: EmailStr
    password: str
    role: UserRoles = UserRoles.student


class UserCreate(YMABase):
    """Pydantic model for creating a new user."""

    email: EmailStr
    password: str | None = None
    role: str | None = None

    @field_validator("password", mode="before")
    @classmethod
    def hash(cls, v):
        """Hash the password before storing."""
        return hash_password(str(v))


class UserRead(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: UserRoles

    class Config:
        orm_mode = True


class UserLoginResponse(BaseModel):
    token: str
    role: str
    email: EmailStr
    full_name: str
    permissions: list[str]
