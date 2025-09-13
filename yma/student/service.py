from typing import List, Tuple
from tortoise.expressions import Q

from .models import Student, StudentCreate, StudentUpdate
from .repository import StudentRepository


class StudentService:
    def __init__(self, repository: StudentRepository):
        self.repository = repository

    async def paginated(
        self, page: int, page_size: int, search: Q = Q(), order: list = []
    ) -> Tuple[int, List[Student]]:
        return await self.repository.paginated(page, page_size, search, order, prefetch=['user'])

    async def get(self, student_id: int) -> Student | None:
        """Gets a student by id."""
        return await self.repository.get(id=student_id, prefetch=['user'])

    async def get_by_name(self, name: str) -> Student | None:
        """Gets a student by name."""
        return await self.repository.get(name=name)

    async def create(self, student_in: StudentCreate) -> Student:
        return await self.repository.create(
            user_id=student_in.user_id,
            student_number=student_in.student_number,
            grade=student_in.grade,
            is_admission_payed=False,
        )

    async def update(self, student: Student, student_in: StudentUpdate) -> Student:
        """Updates a student."""
        return await self.repository.update(
            student, 
            student_number=student_in.student_number,
            grade=student_in.grade,
        )

    async def delete(self, student_id: int) -> bool:
        """Deletes a student."""
        return await self.repository.delete(student_id)
