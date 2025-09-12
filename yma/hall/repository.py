from typing import List, Optional, Tuple
from tortoise.expressions import Q

from .models import Hall


class HallRepository:
    async def paginated(
        self,
        page: int,
        page_size: int,
        search: Optional[Q] = None,
        order: Optional[List[str]] = None,
        prefetch: Optional[List[str]] = None
    ) -> Tuple[int, List[Hall]]:
        # Use default if no search
        query = Hall.filter(search) if search else Hall.all()
        if prefetch:
            query = query.prefetch_related(*prefetch)
        if order:
            query = query.order_by(*order)
        total = await query.count()
        records = await query.offset((page - 1) * page_size).limit(page_size)
        return total, list(records)

    async def create(self, **kwargs) -> Hall:
        hall = await Hall.create(**kwargs)
        return hall

    async def get(self, **filters) -> Optional[Hall]:
        return await Hall.filter(**filters).first()

    async def list(self) -> List[Hall]:
        return await Hall.all()

    async def update(self, hall: Hall, **kwargs) -> Hall:
        for key, value in kwargs.items():
            setattr(hall, key, value)
        await hall.save()
        return hall

    async def delete(self, hall_id: int) -> bool:
        hall = await self.get(id=hall_id)
        if not hall:
            return False
        await hall.delete()
        return True

    async def exists(self, **kwards) -> bool:
        return await Hall.exists(**kwards)
