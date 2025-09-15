from typing import List, Tuple
from tortoise.expressions import Q

from yma.payments.models import Payment, PaymentCreate
from yma.payments.repository import PaymentRepository
from yma.enrollment.repos import EnrollmentRepository
from yma.enums import PayerType, PaymentMethodType, PaymentType


class PaymentService:
    def __init__(self, repository: PaymentRepository):
        self.repository = repository

    async def paginated(
        self, page: int, page_size: int, search: Q = Q(), order: list = []
    ) -> Tuple[int, List[Payment]]:
        return await self.repository.paginated(page, page_size, search, order)

    # async def get(self, hall_id: int) -> Hall | None:
    #     """Gets a hall by id."""
    #     return await self.repository.get(id=hall_id)

    # async def get_by_name(self, name: str) -> Hall | None:
    #     """Gets a hall by name."""
    #     return await self.repository.get(name=name)

    async def create(self, payment_in: PaymentCreate) -> Payment:
        return await self.repository.create(**payment_in.model_dump())

    async def create_admission_payment(self, payment_in: PaymentCreate) -> Payment:
        return await self.repository.create(
            payer_type=PayerType.STUDENT,
            payer_user_id=payment_in.payer_user_id,
            payee_type=PayerType.INSTITUTE,
            payment_type=PaymentType.ADMISSION_FEE,
            payment_method=PaymentMethodType.CASH,
            amount=payment_in.amount,
        )

    async def create_course_payment(self, payment_in: PaymentCreate) -> Payment:
        return await self.repository.create(
            payer_type=PayerType.STUDENT,
            payer_user_id=payment_in.payer_user_id,
            payee_type=PayerType.INSTITUTE,
            payment_type=PaymentType.COURSE_FEE,
            payment_method=PaymentMethodType.CASH,
            amount=payment_in.amount,
        )

    # async def update(self, hall: Hall, hall_in: HallUpdate) -> Hall:
    #     """Updates a hall."""
    #     return await self.repository.update(hall, **hall_in.model_dump(exclude_unset=True))

    # async def delete(self, hall_id: int) -> bool:
    #     """Deletes a hall."""
    #     return await self.repository.delete(hall_id)
