from typing import List, Tuple
from tortoise.expressions import Q

from .models import Guardian, GuardianCreate, GuardianUpdate
from .repository import GuardianRepository


class GuardianService:
    def __init__(self, repository: GuardianRepository):
        self.repository = repository

    async def paginated_guardians(
        self, page: int, page_size: int, search: Q = Q(), order: list = []
    ) -> Tuple[int, List[Guardian]]:
        return await self.repository.paginated(page, page_size, search, order)

    async def get(self, guardian_id: int) -> Guardian | None:
        """Gets a guardian by id."""
        return await self.repository.get(id=guardian_id)

    async def get_by_name(self, name: str) -> Guardian | None:
        """Gets a guardian by name."""
        return await self.repository.get(name=name)

    async def create(self, guardian_in: GuardianCreate) -> Guardian:
        return await self.repository.create(**guardian_in.model_dump())

    async def update(self, guardian: Guardian, guardian_in: GuardianUpdate) -> Guardian:
        """Updates a guardian."""
        return await self.repository.update(guardian, **guardian_in.model_dump(exclude_unset=True))

    async def delete(self, guardian_id: int) -> bool:
        """Deletes a guardian."""
        return await self.repository.delete(guardian_id)
