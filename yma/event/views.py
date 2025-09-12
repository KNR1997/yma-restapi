from typing import Optional
from fastapi import APIRouter, Query
from tortoise.expressions import Q

from yma.exceptions import ResourceNotFoundException

from .models import EventCreate, EventPagination, EventRead, EventUpdate
from .repository import EventRepository
from .service import EventService


router = APIRouter()
service = EventService(EventRepository())


@router.get("", response_model=EventPagination)
async def paginated_events(
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
    return EventPagination(
        data=data,
        itemsPerPage=10,
        page=page,
        page_size=page_size,
        total=total,
    )


@router.get("/{event_id}", response_model=EventRead)
async def get_event(event_id: int):
    """Get a event by its id."""
    event = await service.get(event_id)
    return event


@router.post("", response_model=EventRead)
async def create_event(event_in: EventCreate):
    """Create a new event."""
    return await service.create(event_in)


@router.put("/{event_id}", response_model=EventRead)
async def update_event(
    event_id: int,
    event_in: EventUpdate
):
    """Update a event by its id."""
    event = await service.get(event_id=event_id)
    if not event:
        raise ResourceNotFoundException(
            "A event with this id does not exist.")
    return await service.update(event=event, event_in=event_in)


@router.delete("/{event_id}", response_model=None)
async def delete_event(event_id: int):
    """Delete a event, returning only an HTTP 200 OK if successful."""
    return await service.delete(event_id)
