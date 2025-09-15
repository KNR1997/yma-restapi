from yma.repository import BaseRepository
from .models import ApiLog


class ApiLogRepository(BaseRepository[ApiLog]):
    def __init__(self):
        super().__init__(ApiLog)
