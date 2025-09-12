from tortoise.expressions import Q

from yma.repository import BaseRepository

from ..models import CourseTopic


class CourseTopicRepository(BaseRepository[CourseTopic]):
    def __init__(self):
        super().__init__(CourseTopic)
