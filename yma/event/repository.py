from typing import List, Optional, Tuple
from tortoise.expressions import Q

from .models import Event


class EventRepository:
    async def paginated(
        self,
        page: int,
        page_size: int,
        search: Optional[Q] = None,
        order: Optional[List[str]] = None,
        prefetch: Optional[List[str]] = None
    ) -> Tuple[int, List[Event]]:
        # Use default if no search
        query = Event.filter(search) if search else Event.all()
        if prefetch:
            query = query.prefetch_related(*prefetch)
        if order:
            query = query.order_by(*order)
        total = await query.count()
        records = await query.offset((page - 1) * page_size).limit(page_size)
        return total, list(records)

    async def create(self, **kwargs) -> Event:
        event = await Event.create(**kwargs)
        return event

    async def get(self, **filters) -> Optional[Event]:
        return await Event.filter(**filters).first()

    async def list(self) -> List[Event]:
        return await Event.all()

    async def update(self, event: Event, **kwargs) -> Event:
        for key, value in kwargs.items():
            setattr(event, key, value)
        await event.save()
        return event

    async def delete(self, event_id: int) -> bool:
        event = await self.get(id=event_id)
        if not event:
            return False
        await event.delete()
        return True

    async def exists(self, **kwards) -> bool:
        return await Event.exists(**kwards)
