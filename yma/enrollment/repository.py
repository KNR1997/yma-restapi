from typing import List, Optional, Tuple
from tortoise.expressions import Q

from .models import Enrollment


class EnrollmentRepository:
    async def paginated(
        self,
        page: int,
        page_size: int,
        search: Optional[Q] = None,
        order: Optional[List[str]] = None,
        prefetch: Optional[List[str]] = None
    ) -> Tuple[int, List[Enrollment]]:
        # Use default if no search
        query = Enrollment.filter(search) if search else Enrollment.all()
        if prefetch:
            query = query.prefetch_related(*prefetch)
        if order:
            query = query.order_by(*order)
        total = await query.count()
        records = await query.offset((page - 1) * page_size).limit(page_size)
        return total, list(records)

    async def create(self, **kwargs) -> Enrollment:
        enrollment = await Enrollment.create(**kwargs)
        return enrollment

    async def get(self, **filters) -> Optional[Enrollment]:
        return await Enrollment.filter(**filters).first()

    async def list(self) -> List[Enrollment]:
        return await Enrollment.all()

    async def update(self, enrollment: Enrollment, **kwargs) -> Enrollment:
        for key, value in kwargs.items():
            setattr(enrollment, key, value)
        await enrollment.save()
        return enrollment

    async def delete(self, enrollment_id: int) -> bool:
        enrollment = await self.get(id=enrollment_id)
        if not enrollment:
            return False
        await enrollment.delete()
        return True

    async def exists(self, **kwards) -> bool:
        return await Enrollment.exists(**kwards)
