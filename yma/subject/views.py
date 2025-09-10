from fastapi import APIRouter, Depends

from sqlalchemy.exc import IntegrityError


from yma.database.core import DbSession
from yma.auth.permissions import (
    AdminPermission,
    PermissionsDependency
)
from yma.database.service import CommonParameters, search_filter_sort_paginate
from yma.exceptions import DuplicateNameError, NotFoundError
from .models import Subject, SubjectCreate, SubjectPagination, SubjectRead, SubjectUpdate
from .service import create, get, update, delete, get_by_name

router = APIRouter()


@router.get("", response_model=SubjectPagination)
def get_subjects(common: CommonParameters):
    """Get all subjects, or only those matching a given search term."""
    return search_filter_sort_paginate(model=Subject, **common)


@router.get("/{subject_id}", response_model=SubjectRead)
def get_subject(db_session: DbSession, subject_id: int):
    """Get a subject by its id."""
    subject = get(db_session=db_session, subject_id=subject_id)
    if not subject:
        raise NotFoundError("A subject with this id does not exist.")
    return subject


@router.post(
    "",
    response_model=SubjectRead,
    dependencies=[Depends(PermissionsDependency([AdminPermission]))]
)
def create_subject(db_session: DbSession, subject_in: SubjectCreate):
    """Create a subject."""
    subject = get_by_name(db_session=db_session, name=subject_in.name)
    if subject:
        raise DuplicateNameError("name")
    return create(db_session=db_session, subject_in=subject_in)


@router.put(
    "/{subject_id}",
    response_model=SubjectRead,
    dependencies=[Depends(PermissionsDependency([AdminPermission]))]
)
def update_subject(
    db_session: DbSession,
    subject_id: int,
    subject_in: SubjectUpdate
):
    """Update a subject by its id."""
    subject = get(db_session=db_session, subject_id=subject_id)
    if not subject:
        raise NotFoundError("A subject with this id does not exist.")
    try:
        subject = update(
            db_session=db_session, subject=subject, subject_in=subject_in
        )
    except IntegrityError:
        db_session.rollback()   # 🔑 reset the session so middleware won’t choke
        raise DuplicateNameError("name")

    return subject


@router.delete(
    "/{subject_id}",
    response_model=None,
    dependencies=[Depends(PermissionsDependency([AdminPermission]))],
)
def delete_subject(db_session: DbSession, subject_id: int):
    """Delete a subject, returning only an HTTP 200 OK if successful."""
    subject = get(db_session=db_session, subject_id=subject_id)
    if not subject:
        raise NotFoundError("A subject with this id does not exist.")
    delete(db_session=db_session, subject_id=subject_id)
