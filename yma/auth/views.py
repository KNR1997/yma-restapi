from fastapi import APIRouter, HTTPException, status

from yma.db_core.core import DbSession

from .models import UserLogin, UserLoginResponse, UserRead, UserRegister
from .service import create, get_by_email

auth_router = APIRouter()
user_router = APIRouter()


@auth_router.post("/register", response_model=UserRead)
def register_user(
    user_in: UserRegister,
    db_session: DbSession,
):
    existing_user = get_by_email(db_session=db_session, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "msg": "A user with this email already exists.",
                "loc": ["email"],
                "type": "value_error",
            }],
        )
    return create(db_session=db_session, user_in=user_in)


@auth_router.post("/login", response_model=UserLoginResponse)
def login_user(
    user_in: UserLogin,
    db_session: DbSession,
):
    user = get_by_email(db_session=db_session, email=user_in.email)
    if user and user.verify_password(user_in.password):
        return {
            "token": user.token,
            "role": user.role.value,
            "email": user.email,
            "full_name": user.full_name,
        }

    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=[
            {
                "msg": "Invalid email.",
                "loc": ["email"],
                "type": "value_error"
            },
            {
                "msg": "Invalid password.",
                "loc": ["password"],
                "type": "value_error"
            },
        ],
    )
