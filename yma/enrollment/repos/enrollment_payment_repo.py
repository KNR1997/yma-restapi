from yma.repository import BaseRepository
from yma.enrollment.models import EnrollmentPayment


class EnrollmentPaymentRepository(BaseRepository[EnrollmentPayment]):
    def __init__(self):
        super().__init__(EnrollmentPayment)
