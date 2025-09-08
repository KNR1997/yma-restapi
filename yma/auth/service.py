import logging

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED
from sqlalchemy.exc import IntegrityError

from yma.config import DISPATCH_JWT_ALG, DISPATCH_JWT_SECRET

from .models import UserRegister, YMAUser
from .security import get_password_hash

log = logging.getLogger(__name__)

# This adds the "Authorize" button in Swagger UI
security = HTTPBearer()

InvalidCredentialException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED, detail=[
        {"msg": "Could not validate credentials"}]
)


def get_by_email(*, db_session, email: str) -> YMAUser | None:
    """Returns a user object based on user email."""
    return db_session.query(YMAUser).filter(YMAUser.email == email).one_or_none()


def create(*, db_session, user_in: UserRegister) -> YMAUser:
    """Creates a new user for the Student Management System."""
    hashed_password = get_password_hash(user_in.password)

    user = YMAUser(
        full_name=user_in.full_name,
        email=user_in.email,
        password=hashed_password,
        role=user_in.role,
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def get_or_create(*, db_session, organization: str, user_in: UserRegister) -> YMAUser:
    """Gets an existing user or creates a new one."""
    user = get_by_email(db_session=db_session, email=user_in.email)

    if not user:
        try:
            user = create(
                db_session=db_session,
                organization=organization, user_in=user_in
            )
        except IntegrityError:
            db_session.rollback()
            log.exception(
                f"Unable to create user with email address {user_in.email}.")

    return user


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> YMAUser:
    """Get the current authenticated user from the JWT token."""

    db_session = request.state.db

    # Extract token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")

    token = auth_header.split(" ")[1]

    try:
        # Decode JWT
        payload = jwt.decode(token, DISPATCH_JWT_SECRET,
                             algorithms=[DISPATCH_JWT_ALG])
        # assuming you store user email in "sub"
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    # Fetch user from DB
    user = db_session.query(YMAUser).filter(YMAUser.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user
