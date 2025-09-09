from fastapi import APIRouter, HTTPException, status

from yma.database.core import DbSession

from .models import UserLogin, UserLoginResponse, UserRead, UserRegister
from .service import CurrentUser, create, get_by_email

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
            "permissions": [user.role.value],
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


@auth_router.get("/me", response_model=UserRead)
def get_me(*, current_user: CurrentUser):
    # Create a response dict that includes settings
    response_data = {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "role": current_user.role.value
    }

    return response_data
