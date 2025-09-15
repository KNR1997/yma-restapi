from typing import List, Tuple
from tortoise.expressions import Q

from .models import ApiLog
from .repository import ApiLogRepository


class ApiLogService:
    def __init__(self, repository: ApiLogRepository):
        self.repository = repository

    async def paginated(
        self, page: int, page_size: int, search: Q = Q(), order: list = []
    ) -> Tuple[int, List[ApiLog]]:
        return await self.repository.paginated(page, page_size, search, order)

