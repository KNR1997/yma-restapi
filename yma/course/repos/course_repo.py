from typing import List, Optional, Tuple
from tortoise.expressions import Q

from ..models import Course


class CourseRepository:
    async def paginated(
        self,
        page: int,
        page_size: int,
        search: Optional[Q] = None,
        order: Optional[List[str]] = None,
        prefetch: Optional[List[str]] = None
    ) -> Tuple[int, List[Course]]:
        # Use default if no search
        query = Course.filter(search) if search else Course.all()
        if prefetch:
            query = query.prefetch_related(*prefetch)
        if order:
            query = query.order_by(*order)
        total = await query.count()
        records = await query.offset((page - 1) * page_size).limit(page_size)
        return total, list(records)

    async def get_student_enrolled_paginated(
        self,
        student_id: int,
        page: int,
        page_size: int,
        search: Optional[Q] = None,
        order: Optional[List[str]] = None,
        prefetch: Optional[List[str]] = None
    ) -> Tuple[int, List[Course]]:
        # Use default if no search
        query = Course.filter(
            enrollments__student_id=student_id,
            enrollments__is_active=True
        )
        if search:
            query = query.filter(search)
        if prefetch:
            query = query.prefetch_related(*prefetch)
        if order:
            query = query.order_by(*order)
        total = await query.count()
        records = await query.offset((page - 1) * page_size).limit(page_size)
        return total, list(records)

    async def create(self, **kwargs) -> Course:
        course = await Course.create(**kwargs)
        return course

    async def get(self, prefetch: Optional[List[str]] = None, **filters) -> Optional[Course]:
        if prefetch:
            return await Course.filter(**filters).first().prefetch_related(*prefetch)
        else:
            return await Course.filter(**filters).first()

    async def list(self) -> List[Course]:
        return await Course.all()

    async def update(self, course: Course, **kwargs) -> Course:
        for key, value in kwargs.items():
            setattr(course, key, value)
        await course.save()
        return course

    async def delete(self, course_id: int) -> bool:
        course = await self.get(id=course_id)
        if not course:
            return False
        await course.delete()
        return True

    async def exists(self, **kwards) -> bool:
        return await Course.exists(**kwards)
