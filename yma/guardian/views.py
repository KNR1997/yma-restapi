from fastapi import APIRouter, Depends, HTTPException, status

from yma.database.core import DbSession
from yma.auth.permissions import (
    AdminPermission,
    PermissionsDependency
)
from yma.database.service import CommonParameters, search_filter_sort_paginate
from .models import Guardian, GuardianCreate, GuardianPagination, GuardianRead, GuardianUpdate
from .service import create, get, update, delete

router = APIRouter()


@router.get("", response_model=GuardianPagination)
def get_guardians(common: CommonParameters):
    """Get all guardians, or only those matching a given search term."""
    return search_filter_sort_paginate(model=Guardian, **common)


@router.get("/{guardian_id}", response_model=GuardianRead)
def get_guardian(db_session: DbSession, guardian_id: int):
    """Get a guardian by its id."""
    guardian = get(db_session=db_session, guardian_id=guardian_id)
    if not guardian:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A guardian with this id does not exist."}],
        )
    return guardian


@router.post(
    "",
    response_model=GuardianRead,
    dependencies=[Depends(PermissionsDependency([AdminPermission]))]
)
def create_guardian(db_session: DbSession, guardian_in: GuardianCreate):
    """Create a guardian."""
    return create(db_session=db_session, guardian_in=guardian_in)


@router.put(
    "/{guardian_id}",
    response_model=GuardianRead,
    dependencies=[Depends(PermissionsDependency([AdminPermission]))]
)
def update_guardian(
    db_session: DbSession,
    guardian_id: int,
    guardian_in: GuardianUpdate
):
    """Update a guardian by its id."""
    guardian = get(db_session=db_session, guardian_id=guardian_id)
    if not guardian:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A guardian with this id does not exist."}],
        )
    guardian = update(
        db_session=db_session, guardian=guardian, guardian_in=guardian_in
    )
    return guardian


@router.delete(
    "/{guardian_id}",
    response_model=None,
    dependencies=[Depends(PermissionsDependency([AdminPermission]))],
)
def delete_guardian(db_session: DbSession, guardian_id: int):
    """Delete a guardian, returning only an HTTP 200 OK if successful."""
    guardian = get(db_session=db_session, guardian_id=guardian_id)
    if not guardian:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A guardian with this id does not exist."}],
        )
    delete(db_session=db_session, guardian_id=guardian_id)
