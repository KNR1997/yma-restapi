from typing import List, Optional, Tuple
from tortoise.expressions import Q

from .models import YMAUser


class UserRepository:
    async def paginated(
        self,
        page: int,
        page_size: int,
        search: Optional[Q] = None,
        order: Optional[List[str]] = None,
        prefetch: Optional[List[str]] = None
    ) -> Tuple[int, List[YMAUser]]:
        # Use default if no search
        query = YMAUser.filter(search) if search else YMAUser.all()
        if prefetch:
            query = query.prefetch_related(*prefetch)
        if order:
            query = query.order_by(*order)
        total = await query.count()
        records = await query.offset((page - 1) * page_size).limit(page_size)
        return total, list(records)

    async def create(self, **kwargs, ) -> YMAUser:
        user = await YMAUser.create(**kwargs)
        return user

    async def get(
        self, 
        prefetch: Optional[List[str]] = None, 
        **filters
    ) -> Optional[YMAUser]:
        if prefetch:
            return await YMAUser.filter(**filters).prefetch_related(*prefetch).first()
        else:
            return await YMAUser.filter(**filters).first()

    async def list(self) -> List[YMAUser]:
        return await YMAUser.all()

    async def update(self, YMAUser: YMAUser, **kwargs) -> YMAUser:
        for key, value in kwargs.items():
            setattr(YMAUser, key, value)
        await YMAUser.save()
        return YMAUser

    async def delete(self, YMAUser_id: int) -> bool:
        YMAUser = await self.get(id=YMAUser_id)
        if not YMAUser:
            return False
        await YMAUser.delete()
        return True

    async def exists(self, **kwards) -> bool:
        return await YMAUser.exists(**kwards)
