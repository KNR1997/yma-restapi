from yma.repository import BaseRepository

from .models import Enrollment


class EnrollmentRepository(BaseRepository[Enrollment]):
    def __init__(self):
        super().__init__(Enrollment)
