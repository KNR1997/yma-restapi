from typing import List, Tuple
from tortoise.expressions import Q

from .models import Enrollment, EnrollmentCreate, EnrollmentUpdate
from .repository import EnrollmentRepository


class EnrollmentService:
    def __init__(self, repository: EnrollmentRepository):
        self.repository = repository

    async def paginated(
        self, page: int, page_size: int, search: Q = Q(), order: list = []
    ) -> Tuple[int, List[Enrollment]]:
        return await self.repository.paginated(page, page_size, search, order, prefetch=['course', 'student', 'student__user'])

    async def get(self, enrollment_id: int) -> Enrollment | None:
        """Gets a enrollment by id."""
        return await self.repository.get(id=enrollment_id, prefetch=['course', 'student', 'student__user'])

    async def is_exist(self, student_id: int, course_id: int) -> bool:
        """Gets a enrollment by student_id and course_id."""
        return await self.repository.exists(student_id=student_id, course_id=course_id)

    async def create(self, enrollment_in: EnrollmentCreate) -> Enrollment:
        return await self.repository.create(
            student_id=enrollment_in.student_id,
            course_id=enrollment_in.course_id,
            is_active=False,
        )

    async def update(self, enrollment: Enrollment, enrollment_in: EnrollmentUpdate) -> Enrollment:
        """Updates a enrollment."""
        return await self.repository.update(enrollment, **enrollment_in.model_dump(exclude_unset=True))

    async def delete(self, enrollment_id: int) -> bool:
        """Deletes a enrollment."""
        return await self.repository.delete(enrollment_id)
