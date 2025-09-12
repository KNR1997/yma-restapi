from typing import Optional
from fastapi import APIRouter, Query
from tortoise.expressions import Q

from yma.exceptions import ResourceNotFoundException

from .models import GuardianCreate, GuardianPagination, GuardianRead, GuardianUpdate
from .repository import GuardianRepository
from .service import GuardianService


router = APIRouter()
service = GuardianService(GuardianRepository())


@router.get("", response_model=GuardianPagination)
async def paginated_guardians(
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

    total, data = await service.paginated_guardians(page=page, page_size=page_size, search=q)
    return GuardianPagination(
        data=data,
        itemsPerPage=10,
        page=page,
        page_size=page_size,
        total=total,
    )


@router.get("/{guardian_id}", response_model=GuardianRead)
async def get_guardian(guardian_id: int):
    """Get a guardian by its id."""
    guardian = await service.get(guardian_id)
    return guardian


@router.post("", response_model=GuardianRead)
async def create_guardian(guardian_in: GuardianCreate):
    """Create a new guardian."""
    return await service.create(guardian_in)


@router.put("/{guardian_id}", response_model=GuardianRead)
async def update_guardian(
    guardian_id: int,
    guardian_in: GuardianUpdate
):
    """Update a guardian by its id."""
    guardian = await service.get(guardian_id=guardian_id)
    if not guardian:
        raise ResourceNotFoundException(
            "A guardian with this id does not exist.")
    return await service.update(guardian=guardian, guardian_in=guardian_in)


@router.delete("/{guardian_id}", response_model=None)
async def delete_guardian(guardian_id: int):
    """Delete a guardian, returning only an HTTP 200 OK if successful."""
    return await service.delete(guardian_id)
