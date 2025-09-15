from typing import List, Tuple
from tortoise.expressions import Q

from yma.enrollment.models import EnrollmentPayment, EnrollmentCreate, EnrollmentPaymentCreate
from yma.enrollment.repos import EnrollmentPaymentRepository


class EnrollmentPaymentService:
    def __init__(self, repository: EnrollmentPaymentRepository):
        self.repository = repository

    async def paginated(
        self, page: int, page_size: int, search: Q = Q(), order: list = []
    ) -> Tuple[int, List[EnrollmentPayment]]:
        return await self.repository.paginated(page, page_size, search, order)

    async def get(self, enrollment_id: int) -> EnrollmentPayment | None:
        """Gets a enrollment by id."""
        return await self.repository.get(id=enrollment_id, prefetch=['course', 'student', 'student__user'])

    async def is_exist(self, student_id: int, course_id: int) -> bool:
        """Gets a enrollment by student_id and course_id."""
        return await self.repository.exists(student_id=student_id, course_id=course_id)

    async def create(self, enrollment_in: EnrollmentPaymentCreate) -> EnrollmentPayment:
        return await self.repository.create(
            student_id=enrollment_in.student_id,
            course_id=enrollment_in.course_id,
            is_active=False,
        )

    # async def update(self, enrollment: EnrollmentPayment, enrollment_in: EnrollmentUpdate) -> EnrollmentPayment:
    #     """Updates a enrollment."""
    #     return await self.repository.update(enrollment, **enrollment_in.model_dump(exclude_unset=True))

    async def delete(self, enrollment_id: int) -> bool:
        """Deletes a enrollment."""
        return await self.repository.delete(enrollment_id)
