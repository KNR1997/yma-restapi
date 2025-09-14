from typing import List, Tuple
from tortoise.expressions import Q

from yma.course.repos.course_topic_repo import CourseTopicRepository

from .models import CourseTopicCreate, CourseTopic, CourseTopicCreateRequest


class CourseTopicService:
    def __init__(self, repository: CourseTopicRepository):
        self.repository = repository

    async def paginated(
        self, page: int, page_size: int, search: Q = Q(), order: list = []
    ) -> Tuple[int, List[CourseTopic]]:
        return await self.repository.paginated(page, page_size, search, order)

    async def create_or_update_course_topics(self, course_id: int, data: CourseTopicCreateRequest):
        delete_ids = data.course_topics.delete or []
        upserts = data.course_topics.upsert or []

        # 1. Bulk delete in one query
        if delete_ids:
            await self.repository.bulk_delete(topic_ids=delete_ids)

        if not upserts:
            return

        # 2. Split into "updates" and "creates"
        update_ids = [t.id for t in upserts if t.id]
        create_items = [t for t in upserts if not t.id]

        # 3. Fetch all existing topics for this course at once
        existing_topics = await self.repository.get_by_ids(update_ids)
        existing_by_id = {t.id: t for t in existing_topics}

        # 4. Fetch all topic names in this course (to check duplicates)
        existing_names = await self.repository.get_all_names(course_id=course_id)

        # 5. Process updates
        for topic_data in upserts:
            if topic_data.id:  # update
                topic = existing_by_id.get(topic_data.id)
                if not topic:
                    raise ValidationException(
                        validation={"id": ["Topic does not exist."]})

                # If name changed → check uniqueness
                if topic_data.name and topic_data.name != topic.name:
                    if topic_data.name in existing_names:
                        raise ValidationException(
                            validation={"name": ["Topic already exists with this name."]})
                    existing_names.discard(topic.name)  # remove old
                    existing_names.add(topic_data.name)  # add new

                await self.repository.update(
                    topic_data.id,
                    **topic_data.model_dump(exclude_unset=True)
                )

        # 6. Process creates
        for topic_data in create_items:
            if topic_data.name in existing_names:
                raise ValidationException(
                    validation={"name": ["Topic already exists with this name."]})
            existing_names.add(topic_data.name)

            await self.repository.create(
                course_id=course_id,
                name=topic_data.name,
                description=topic_data.description
            )

