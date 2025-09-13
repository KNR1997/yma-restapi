from yma.repository import BaseRepository

from .models import Guardian


class GuardianRepository(BaseRepository[Guardian]):
    def __init__(self):
        super().__init__(Guardian)
