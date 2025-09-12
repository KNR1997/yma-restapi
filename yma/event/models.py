from pydantic import BaseModel
from tortoise import fields

from tortoise import fields, models

from yma.course.models import Course
from yma.enums import EventStatusType, EventType
from yma.models import Pagination


class Event(models.Model):
    id = fields.BigIntField(pk=True)
    course: fields.ForeignKeyRelation[Course] = fields.ForeignKeyField(
        "models.Course", related_name="events"
    )
    event_type = fields.CharEnumField(EventType, index=True)
    code = fields.CharField(max_length=255, null=True)
    date = fields.DateField(null=True)
    start_time = fields.TimeField(null=True)
    end_time = fields.TimeField(null=True)
    reference = fields.CharField(max_length=255, null=True)
    status = fields.CharEnumField(EventStatusType, index=True)

    class Meta:
        table = "event"


# Pydantic models
class EventBase(BaseModel):
    course_id: str
    event_type: EventType
    code: str
    date: str
    start_time: str
    end_time: str
    reference: str
    status: EventStatusType

    model_config = {
        "from_attributes": True
    }


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    pass


class EventRead(EventBase):
    id: int


class EventPagination(Pagination):
    data: list[EventRead]
