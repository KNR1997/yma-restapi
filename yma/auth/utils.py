from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from starlette.requests import Request

import jwt
from jose import JWTError, jwt

from yma.config import YMA_JWT_ALG, YMA_JWT_SECRET

from .models import JWTPayload, YMAUser

# This adds the "Authorize" button in Swagger UI
security = HTTPBearer()


def create_access_token(*, data: JWTPayload):
    payload = data.model_dump().copy()
    encoded_jwt = jwt.encode(payload, YMA_JWT_SECRET, algorithm=YMA_JWT_ALG)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> YMAUser:
    """Get the current authenticated user from the JWT token."""

    # Extract token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")

    token = auth_header.split(" ")[1]

    try:
        # Decode JWT
        payload = jwt.decode(
            token,
            YMA_JWT_SECRET,
            algorithms=[YMA_JWT_ALG]
        )
        # assuming you store user email in "sub"
        email: str = payload.get("email")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = await YMAUser.get_or_none(email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user

CurrentUser = Annotated[YMAUser, Depends(get_current_user)]
