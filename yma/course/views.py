from fastapi import APIRouter, Depends, HTTPException, status

from yma.database.core import DbSession
from yma.auth.permissions import (
    AdminPermission,
    PermissionsDependency
)
from yma.database.service import CommonParameters, search_filter_sort_paginate
from .models import Course, CourseCreate, CoursePagination, CourseRead, CourseUpdate
from .service import create, get, update, delete

router = APIRouter()


@router.get("", response_model=CoursePagination)
def get_courses(common: CommonParameters):
    """Get all courses, or only those matching a given search term."""
    return search_filter_sort_paginate(model=Course, **common)


@router.get("/{course_id}", response_model=CourseRead)
def get_course(db_session: DbSession, course_id: int):
    """Get a course by its id."""
    course = get(db_session=db_session, course_id=course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A course with this id does not exist."}],
        )
    return course


@router.post(
    "",
    response_model=CourseRead,
    dependencies=[Depends(PermissionsDependency([AdminPermission]))]
)
def create_course(db_session: DbSession, course_in: CourseCreate):
    """Create a course."""
    return create(db_session=db_session, course_in=course_in)


@router.put(
    "/{course_id}",
    response_model=CourseRead,
    dependencies=[Depends(PermissionsDependency([AdminPermission]))]
)
def update_course(
    db_session: DbSession,
    course_id: int,
    course_in: CourseUpdate
):
    """Update a course by its id."""
    course = get(db_session=db_session, course_id=course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A course with this id does not exist."}],
        )
    course = update(
        db_session=db_session, course=course, course_in=course_in
    )
    return course


@router.delete(
    "/{course_id}",
    response_model=None,
    dependencies=[Depends(PermissionsDependency([AdminPermission]))],
)
def delete_course(db_session: DbSession, course_id: int):
    """Delete a course, returning only an HTTP 200 OK if successful."""
    course = get(db_session=db_session, course_id=course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A course with this id does not exist."}],
        )
    delete(db_session=db_session, course_id=course_id)
