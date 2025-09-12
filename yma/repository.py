from typing import List, Optional, Tuple, Type, TypeVar, Generic
from tortoise.expressions import Q
from tortoise.models import Model

T = TypeVar("T", bound=Model)  # T is any Tortoise model


class BaseRepository(Generic[T]):
    model: Type[T]  # the model class (e.g., Course, Subject)

    def __init__(self, model: Type[T]):
        self.model = model

    async def paginated(
        self,
        page: int,
        page_size: int,
        search: Optional[Q] = None,
        order: Optional[List[str]] = None,
        prefetch: Optional[List[str]] = None
    ) -> Tuple[int, List[T]]:
        query = self.model.filter(search) if search else self.model.all()
        if prefetch:
            query = query.prefetch_related(*prefetch)
        if order:
            query = query.order_by(*order)

        total = await query.count()
        records = await query.offset((page - 1) * page_size).limit(page_size)
        return total, list(records)

    async def create(self, **kwargs) -> T:
        return await self.model.create(**kwargs)

    async def get(self, prefetch: Optional[List[str]] = None, **filters) -> Optional[T]:
        query = self.model.filter(**filters)
        if prefetch:
            query = query.prefetch_related(*prefetch)
        return await query.first()

    async def list(self) -> List[T]:
        return await self.model.all()

    async def update(self, instance: T, **kwargs) -> T:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await instance.save()
        return instance

    async def delete(self, instance_id: int) -> bool:
        instance = await self.get(id=instance_id)
        if not instance:
            return False
        await instance.delete()
        return True

    async def exists(self, **kwargs) -> bool:
        return await self.model.exists(**kwargs)
