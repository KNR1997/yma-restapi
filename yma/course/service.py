from typing import List, Tuple
from tortoise.expressions import Q

from yma.course.repos.course_repo import CourseRepository

from .models import Course, CourseCreate, CourseUpdate


class CourseService:
    def __init__(self, repository: CourseRepository):
        self.repository = repository

    async def paginated(
        self, page: int, page_size: int, search: Q = Q(), order: list = []
    ) -> Tuple[int, List[Course]]:
        return await self.repository.paginated(page, page_size, search, order)

    async def get_student_enrolled_paginated(
        self, student_id: int, page: int, page_size: int, search: Q = Q(), order: list = []
    ) -> Tuple[int, List[Course]]:
        return await self.repository.get_student_enrolled_paginated(student_id, page, page_size, search, order)

    async def get(self, course_id: int) -> Course | None:
        """Gets a course by id."""
        return await self.repository.get(id=course_id, prefetch=['subject', 'teacher'])

    async def get_by_name(self, name: str) -> Course | None:
        """Gets a course by name."""
        return await self.repository.get(name=name)

    async def create(self, course_in: CourseCreate) -> Course:
        return await self.repository.create(**course_in.model_dump())

    async def update(self, course: Course, course_in: CourseUpdate) -> Course:
        """Updates a course."""
        return await self.repository.update(course, **course_in.model_dump(exclude_unset=True))

    async def delete(self, course_id: int) -> bool:
        """Deletes a course."""
        return await self.repository.delete(course_id)
