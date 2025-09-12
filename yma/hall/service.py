from typing import List, Tuple
from tortoise.expressions import Q

from .models import Hall, HallCreate, HallUpdate
from .repository import HallRepository


class HallService:
    def __init__(self, repository: HallRepository):
        self.repository = repository

    async def paginated_halls(
        self, page: int, page_size: int, search: Q = Q(), order: list = []
    ) -> Tuple[int, List[Hall]]:
        return await self.repository.paginated(page, page_size, search, order)

    async def get(self, hall_id: int) -> Hall | None:
        """Gets a hall by id."""
        return await self.repository.get(id=hall_id)

    async def get_by_name(self, name: str) -> Hall | None:
        """Gets a hall by name."""
        return await self.repository.get(name=name)

    async def create(self, hall_in: HallCreate) -> Hall:
        return await self.repository.create(**hall_in.model_dump())

    async def update(self, hall: Hall, hall_in: HallUpdate) -> Hall:
        """Updates a hall."""
        return await self.repository.update(hall, **hall_in.model_dump(exclude_unset=True))

    async def delete(self, hall_id: int) -> bool:
        """Deletes a hall."""
        return await self.repository.delete(hall_id)
