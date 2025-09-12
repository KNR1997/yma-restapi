from typing import List, Optional, Tuple
from tortoise.expressions import Q

from .models import Guardian


class GuardianRepository:
    async def paginated(
        self,
        page: int,
        page_size: int,
        search: Optional[Q] = None,
        order: Optional[List[str]] = None,
        prefetch: Optional[List[str]] = None
    ) -> Tuple[int, List[Guardian]]:
        # Use default if no search
        query = Guardian.filter(search) if search else Guardian.all()
        if prefetch:
            query = query.prefetch_related(*prefetch)
        if order:
            query = query.order_by(*order)
        total = await query.count()
        records = await query.offset((page - 1) * page_size).limit(page_size)
        return total, list(records)

    async def create(self, **kwargs) -> Guardian:
        guardian = await Guardian.create(**kwargs)
        return guardian

    async def get(self, **filters) -> Optional[Guardian]:
        return await Guardian.filter(**filters).first()

    async def list(self) -> List[Guardian]:
        return await Guardian.all()

    async def update(self, guardian: Guardian, **kwargs) -> Guardian:
        for key, value in kwargs.items():
            setattr(guardian, key, value)
        await guardian.save()
        return guardian

    async def delete(self, guardian_id: int) -> bool:
        guardian = await self.get(id=guardian_id)
        if not guardian:
            return False
        await guardian.delete()
        return True

    async def exists(self, **kwards) -> bool:
        return await Guardian.exists(**kwards)
