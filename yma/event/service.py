from typing import List, Tuple
from tortoise.expressions import Q

from .models import Event, EventCreate, EventUpdate
from .repository import EventRepository


class EventService:
    def __init__(self, repository: EventRepository):
        self.repository = repository

    async def paginated(
        self, page: int, page_size: int, search: Q = Q(), order: list = []
    ) -> Tuple[int, List[Event]]:
        return await self.repository.paginated(page, page_size, search, order)

    async def get(self, event_id: int) -> Event | None:
        """Gets a event by id."""
        return await self.repository.get(id=event_id)

    async def get_by_name(self, name: str) -> Event | None:
        """Gets a event by name."""
        return await self.repository.get(name=name)

    async def create(self, event_in: EventCreate) -> Event:
        return await self.repository.create(**event_in.model_dump())

    async def update(self, event: Event, event_in: EventUpdate) -> Event:
        """Updates a event."""
        return await self.repository.update(event, **event_in.model_dump(exclude_unset=True))

    async def delete(self, event_id: int) -> bool:
        """Deletes a event."""
        return await self.repository.delete(event_id)
