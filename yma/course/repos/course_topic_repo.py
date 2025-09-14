from tortoise.expressions import Q
from typing import List, Optional, Set, Tuple

from yma.repository import BaseRepository

from ..models import CourseTopic


class CourseTopicRepository(BaseRepository[CourseTopic]):
    def __init__(self):
        super().__init__(CourseTopic)

    async def bulk_delete(self, topic_ids: List[int]) -> int:
        """
        Delete multiple topics by IDs in one query.
        Returns number of rows deleted.
        """
        return await CourseTopic.filter(id__in=topic_ids).delete()

    async def get_by_ids(self, ids: List[int]) -> List[CourseTopic]:
        """
        Fetch multiple topics by IDs.
        """
        return await CourseTopic.filter(id__in=ids)

    async def get_all_names(self, course_id: int) -> Set[str]:
        """
        Get all topic names for a given course.
        Useful for duplicate checks.
        """
        rows = await CourseTopic.filter(course_id=course_id).values_list("name", flat=True)
        return set(rows)

    async def update(self, topic_id: int, **kwargs) -> Optional[CourseTopic]:
        course = await self.get(id=topic_id)
        if not course:
            return None
        for key, value in kwargs.items():
            setattr(course, key, value)
        await course.save()
        return course
