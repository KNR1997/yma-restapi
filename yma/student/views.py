from typing import Optional
from fastapi import APIRouter, Query
from tortoise.expressions import Q
from tortoise.transactions import atomic

from yma.auth.repository import UserRepository
from yma.auth.services.user_service import UserService
from yma.course.models import CoursePagination
from yma.course.repos.course_repo import CourseRepository
from yma.course.service import CourseService
from yma.exceptions import ResourceNotFoundException

from .models import StudentCreate, StudentPagination, StudentRead, StudentUpdate
from .repository import StudentRepository
from .service import StudentService


router = APIRouter()
user_service = UserService(UserRepository())
course_service = CourseService(CourseRepository())
service = StudentService(StudentRepository())


@router.get("", response_model=StudentPagination)
async def paginated_students(
    page: int = Query(1, description="Page Number"),
    page_size: int = Query(10, description="Items Per Page"),
    search: Optional[str] = Query("", description="Subject Name for Search"),
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

    total, data = await service.paginated(page=page, page_size=page_size, search=q)
    return StudentPagination(
        data=data,
        itemsPerPage=10,
        page=page,
        page_size=page_size,
        total=total,
    )


@router.get("/{student_id}", response_model=StudentRead)
async def get_student(student_id: int):
    """Get a student by its id."""
    student = await service.get(student_id)
    return student


@atomic()
@router.post("", response_model=StudentRead)
async def create_student(student_in: StudentCreate):
    """Create a new student."""
    user = await user_service.create(student_in.user)
    student_in.user_id = user.id
    return await service.create(student_in)


@atomic()
@router.put("/{student_id}", response_model=StudentRead)
async def update_student(
    student_id: int,
    student_in: StudentUpdate
):
    """Update a student by its id."""
    student = await service.get(student_id=student_id)
    if not student:
        raise ResourceNotFoundException(
            "A student with this id does not exist.")
    user = await user_service.get(user_id=student.user.id)
    if not user:
        raise ResourceNotFoundException(
            "A user for student does not exist.")
    await user_service.update(user=user, user_in=student_in.user)
    return await service.update(student=student, student_in=student_in)


@router.delete("/{student_id}", response_model=None)
async def delete_student(student_id: int):
    """Delete a student, returning only an HTTP 200 OK if successful."""
    return await service.delete(student_id)


@router.get("/{student_id}/available-courses", response_model=CoursePagination)
async def get_available_courses(
    student_id: int,
    page: int = Query(1, description="Page Number"),
    page_size: int = Query(10, description="Items Per Page"),
):
    """Get available courses for student to enroll."""
    student = await service.get(student_id=student_id)
    if not student:
        raise ResourceNotFoundException(
            "A student with this id does not exist.")
    q = Q(grade=student.grade)
    total, data = await course_service.paginated(page=page, page_size=page_size, search=q)
    return CoursePagination(
        data=data,
        itemsPerPage=10,
        page=page,
        page_size=page_size,
        total=total,
    )
