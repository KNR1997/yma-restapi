from yma.repository import BaseRepository
from yma.student.models import Student


class StudentRepository(BaseRepository[Student]):
    def __init__(self):
        super().__init__(Student)
