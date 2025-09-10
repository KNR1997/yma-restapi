from fastapi import APIRouter, HTTPException, status

from yma.database.core import DbSession

from .models import AdminPasswordReset, UserLogin, UserLoginResponse, UserPasswordUpdate, UserRead, UserRegister
from .service import CurrentUser, create, get_by_email, get

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


@user_router.post("/{user_id}/change-password", response_model=UserRead)
def change_password(
    db_session: DbSession,
    user_id: int,
    password_update: UserPasswordUpdate,
    current_user: CurrentUser,
):
    """Change user password with proper validation"""
    user = get(db_session=db_session, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A user with this id does not exist."}],
        )

    # Only allow users to change their own password or owners to reset
    if user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=[{"msg": "Not authorized to change other user passwords"}],
        )

    # Validate current password if user is changing their own password
    if user.id == current_user.id:
        if not user.verify_password(password_update.current_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=[{"msg": "Invalid current password"}],
            )

    # Set new password
    try:
        user.set_password(password_update.new_password)
        db_session.commit()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[{"msg": str(e)}],
        ) from e

    return user


@user_router.post("/{user_id}/reset-password", response_model=UserRead)
def admin_reset_password(
    db_session: DbSession,
    user_id: int,
    password_reset: AdminPasswordReset,
    current_user: CurrentUser,
):
    """Admin endpoint to reset user password"""
    print('api trigger')
    # Verify current user is an admin
    if not current_user.is_admin():
        print('not a admin')
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=[{"msg": "Only admins can reset passwords"}],
        )

    user = get(db_session=db_session, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A user with this id does not exist."}],
        )

    try:
        user.set_password(password_reset.new_password)
        db_session.commit()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[{"msg": str(e)}],
        ) from e

    return user
