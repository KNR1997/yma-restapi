from typing import Optional
from fastapi import APIRouter, Query
from tortoise.expressions import Q

from yma.exceptions import ResourceNotFoundException

from .models import EnrollmentCreate, EnrollmentPagination, EnrollmentRead, EnrollmentUpdate
from .repository import EnrollmentRepository
from .service import EnrollmentService


router = APIRouter()
service = EnrollmentService(EnrollmentRepository())


@router.get("", response_model=EnrollmentPagination)
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
    return EnrollmentPagination(
        data=data,
        itemsPerPage=10,
        page=page,
        page_size=page_size,
        total=total,
    )


@router.get("/{enrollment_id}", response_model=EnrollmentRead)
async def get_enrollment(enrollment_id: int):
    """Get a enrollment by its id."""
    enrollment = await service.get(enrollment_id)
    return enrollment


@router.post("", response_model=EnrollmentRead)
async def create_enrollment(enrollment_in: EnrollmentCreate):
    """Create a new enrollment."""
    return await service.create(enrollment_in)


@router.put("/{enrollment_id}", response_model=EnrollmentRead)
async def update_enrollment(
    enrollment_id: int,
    enrollment_in: EnrollmentUpdate
):
    """Update a enrollment by its id."""
    enrollment = await service.get(enrollment_id=enrollment_id)
    if not enrollment:
        raise ResourceNotFoundException(
            "A enrollment with this id does not exist.")
    return await service.update(enrollment=enrollment, enrollment_in=enrollment_in)


@router.delete("/{enrollment_id}", response_model=None)
async def delete_enrollment(enrollment_id: int):
    """Delete a enrollment, returning only an HTTP 200 OK if successful."""
    return await service.delete(enrollment_id)
