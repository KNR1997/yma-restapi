from fastapi import APIRouter, Depends, HTTPException, status

from yma.database.core import DbSession
from yma.auth.permissions import (
    AdminPermission,
    PermissionsDependency
)
from yma.database.service import CommonParameters, search_filter_sort_paginate
from .models import Hall, HallCreate, HallPagination, HallRead, HallUpdate
from .service import create, get, update, delete

router = APIRouter()


@router.get("", response_model=HallPagination)
def get_halls(common: CommonParameters):
    """Get all halls, or only those matching a given search term."""
    return search_filter_sort_paginate(model=Hall, **common)


@router.get("/{hall_id}", response_model=HallRead)
def get_hall(db_session: DbSession, hall_id: int):
    """Get a hall by its id."""
    hall = get(db_session=db_session, hall_id=hall_id)
    if not hall:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A hall with this id does not exist."}],
        )
    return hall


@router.post(
    "",
    response_model=HallRead,
    dependencies=[Depends(PermissionsDependency([AdminPermission]))]
)
def create_hall(db_session: DbSession, hall_in: HallCreate):
    """Create a hall."""
    return create(db_session=db_session, hall_in=hall_in)


@router.put(
    "/{hall_id}",
    response_model=HallRead,
    dependencies=[Depends(PermissionsDependency([AdminPermission]))]
)
def update_hall(
    db_session: DbSession,
    hall_id: int,
    hall_in: HallUpdate
):
    """Update a hall by its id."""
    hall = get(db_session=db_session, hall_id=hall_id)
    if not hall:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A hall with this id does not exist."}],
        )
    hall = update(
        db_session=db_session, hall=hall, hall_in=hall_in
    )
    return hall


@router.delete(
    "/{hall_id}",
    response_model=None,
    dependencies=[Depends(PermissionsDependency([AdminPermission]))],
)
def delete_hall(db_session: DbSession, hall_id: int):
    """Delete a hall, returning only an HTTP 200 OK if successful."""
    hall = get(db_session=db_session, hall_id=hall_id)
    if not hall:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A hall with this id does not exist."}],
        )
    delete(db_session=db_session, hall_id=hall_id)
