from typing import Optional
from fastapi import APIRouter, Query
from tortoise.expressions import Q

from yma.exceptions import ConflictException, ResourceNotFoundException

from .models import HallCreate, HallPagination, HallRead, HallUpdate
from .repository import HallRepository
from .service import HallService


router = APIRouter()
service = HallService(HallRepository())


@router.get("", response_model=HallPagination)
async def paginated_halls(
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

    total, data = await service.paginated_halls(page=page, page_size=page_size, search=q)
    return HallPagination(
        data=data,
        itemsPerPage=10,
        page=page,
        page_size=page_size,
        total=total,
    )


@router.get("/{hall_id}", response_model=HallRead)
async def get_hall(hall_id: int):
    """Get a hall by its id."""
    hall = await service.get(hall_id)
    return hall


@router.post("", response_model=HallRead)
async def create_hall(hall_in: HallCreate):
    """Create a new hall."""
    if await service.get_by_name(name=hall_in.name):
        raise ConflictException(
            "Hall with this name already exists", field="name")
    return await service.create(hall_in)


@router.put("/{hall_id}", response_model=HallRead)
async def update_hall(
    hall_id: int,
    hall_in: HallUpdate
):
    """Update a hall by its id."""
    hall = await service.get(hall_id=hall_id)
    if not hall:
        raise ResourceNotFoundException(
            "A hall with this id does not exist.")
    if hall_in.name != hall.name:
        if await service.get_by_name(name=hall_in.name):
            raise ConflictException(
                "Hall with this name already exists", field="name")
    return await service.update(hall=hall, hall_in=hall_in)


@router.delete("/{hall_id}", response_model=None)
async def delete_hall(hall_id: int):
    """Delete a hall, returning only an HTTP 200 OK if successful."""
    return await service.delete(hall_id)
