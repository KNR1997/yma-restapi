from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from tortoise.expressions import Q

from yma.auth.permissions import AdminPermission, PermissionsDependency
from yma.auth.utils import CurrentUser, create_access_token
from yma.config import YMA_JWT_EXP
from yma.exceptions import ConflictException, ResourceNotFoundException

from .models import AdminPasswordReset, JWTOut, JWTPayload, UserCreate, UserLogin, UserPagination, UserRead, UserRegister, UserUpdate, YMAUser
from yma.enums import UserRole

from .repository import UserRepository
from .services.user_service import UserService
from .services.auth_service import AuthService


auth_router = APIRouter()
user_router = APIRouter()

user_service = UserService(UserRepository())
auth_service = AuthService(UserRepository())


@auth_router.post("/register", response_model=UserRead)
async def register_user(user_in: UserRegister):
    existing_user = await user_service.get_by_email(email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{
                "msg": "A user with this email already exists.",
                "loc": ["email"],
                "type": "value_error",
            }],
        )
    return await auth_service.register(user_in=user_in)


@auth_router.post("/login", summary="Get token", response_model=JWTOut)
async def login_access_token(credentials: UserLogin):
    user = await auth_service.authenticate(credentials)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username")
    role: UserRole = user.role

    # await user_service.update_last_login(user.id)
    access_token_expires = timedelta(minutes=YMA_JWT_EXP)
    expire = datetime.now(timezone.utc) + access_token_expires

    return JWTOut(
        token=create_access_token(
            data=JWTPayload(
                user_id=str(user.id),
                email=user.email,
                exp=expire,
            )
        ),
        email=user.email,
        username=user.username,
        role=role,
        permissions=[role]
    )


@auth_router.get("/me", response_model=UserRead)
def get_me(*, current_user: CurrentUser):
    # Create a response dict that includes settings
    response_data = {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "name_with_initials": current_user.name_with_initials,
        "nic": current_user.nic,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role.value
    }

    return response_data


@user_router.get("", response_model=UserPagination)
async def paginated_users(
    page: int = Query(1, description="Page Number"),
    page_size: int = Query(10, description="Items Per Page"),
    search: Optional[str] = Query(""),
    searchJoin: str = Query(
        "and", description="'and' or 'or' join for multiple search conditions"),
):
    q = Q()
    if search:
        # Example: search="name:english;status:active"
        filters = search.split(";")
        for f in filters:
            try:
                field, value = f.split(":", 1)
                lookup = {f"{field}__icontains": value}
                condition = Q(**lookup)
                if searchJoin.lower() == "or":
                    q |= condition
                else:
                    q &= condition
            except ValueError:
                continue  # skip invalid filter format

    total, data = await user_service.paginated(page=page, page_size=page_size, search=q)
    return UserPagination(
        data=data,
        itemsPerPage=10,
        page=page,
        page_size=page_size,
        total=total,
    )


@user_router.post(
    "",
    response_model=UserRead,
)
async def create_user(
    user_in: UserCreate,
    current_user: CurrentUser,
    dependencies=[Depends(PermissionsDependency([AdminPermission]))]
):
    """Creates a new user."""
    if await user_service.get_by_email(email=user_in.email):
        raise ConflictException(
            "User with this email already exists", field="email")

    user = await user_service.create(user_in=user_in)
    return user


@user_router.put(
    "/{user_id}",
    dependencies=[Depends(PermissionsDependency([AdminPermission]))],
    response_model=UserRead,
)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    current_user: CurrentUser,
):
    """Update a user."""
    user = await user_service.get(user_id=user_id)
    if not user:
        raise ResourceNotFoundException(
            "A subject with this id does not exist.")
    return await user_service.update(user=user, user_in=user_in)


@user_router.post("/{user_id}/reset-password", response_model=UserRead)
def admin_reset_password(
    user_id: int,
    password_reset: AdminPasswordReset,
    current_user: CurrentUser,
):
    # """Admin endpoint to reset user password"""
    # # Verify current user is an admin
    # if not current_user.is_admin():
    #     print('not a admin')
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail=[{"msg": "Only admins can reset passwords"}],
    #     )

    # user = get(db_session=db_session, user_id=user_id)
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=[{"msg": "A user with this id does not exist."}],
    #     )

    # try:
    #     user.set_password(password_reset.new_password)
    #     db_session.commit()
    # except ValueError as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=[{"msg": str(e)}],
    #     ) from e

    # return user
    ...
