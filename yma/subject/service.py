from typing import List, Tuple
from tortoise.expressions import Q

from .models import Subject, SubjectCreate, SubjectUpdate
from .repository import SubjectRepository


class SubjectService:
    def __init__(self, repository: SubjectRepository):
        self.repository = repository

    async def paginated(
        self, page: int, page_size: int, search: Q = Q(), order: list = []
    ) -> Tuple[int, List[Subject]]:
        return await self.repository.paginated(page, page_size, search, order)

    async def list_subjects(self) -> list[Subject]:
        return await self.repository.list()

    async def get(self, subject_id: int) -> Subject | None:
        """Gets a subject by id."""
        return await self.repository.get(id=subject_id)

    async def get_by_name(self, name: str) -> Subject | None:
        """Gets a subject by name."""
        return await self.repository.get(name=name)

    async def create(self, subject_in: SubjectCreate) -> Subject:
        return await self.repository.create(**subject_in.model_dump())

    async def update(self, subject: Subject, subject_in: SubjectUpdate) -> Subject:
        """Updates a subject."""
        return await self.repository.update(subject, **subject_in.model_dump(exclude_unset=True))

    async def delete(self, subject_id: int) -> bool:
        """Deletes a subject."""
        return await self.repository.delete(subject_id)
