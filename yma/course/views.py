from typing import Optional
from fastapi import APIRouter, Query
from tortoise.expressions import Q

from yma.exceptions import ResourceNotFoundException

from .models import CourseCreate, CoursePageData, CoursePagination, CourseRead, CourseUpdate
from .repos.course_repo import CourseRepository
from .service import CourseService


router = APIRouter()
service = CourseService(CourseRepository())


@router.get("", response_model=CoursePagination)
async def paginated_subjects(
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
    return CoursePagination(
        data=data,
        itemsPerPage=10,
        page=page,
        page_size=page_size,
        total=total,
    )


@router.get("/{course_id}", response_model=CoursePageData)
async def get_course(course_id: int):
    """Get a course by its id."""
    course = await service.get(course_id)
    return course


@router.post("", response_model=CourseRead)
async def create_course(course_in: CourseCreate):
    """Create a new course."""
    return await service.create(course_in)


@router.put("/{course_id}", response_model=CourseRead)
async def update_course(
    course_id: int,
    course_in: CourseUpdate
):
    """Update a course by its id."""
    course = await service.get(course_id=course_id)
    if not course:
        raise ResourceNotFoundException(
            "A course with this id does not exist.")
    return await service.update(course=course, course_in=course_in)


@router.delete("/{course_id}", response_model=None)
async def delete_course(course_id: int):
    """Delete a course, returning only an HTTP 200 OK if successful."""
    return await service.delete(course_id)
