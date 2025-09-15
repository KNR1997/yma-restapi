from tortoise.expressions import Q
from typing import List, Optional, Set, Tuple

from yma.repository import BaseRepository
from yma.payments.models import Payment


class PaymentRepository(BaseRepository[Payment]):
    def __init__(self):
        super().__init__(Payment)
