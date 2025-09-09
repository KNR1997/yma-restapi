from sqlalchemy import Column, Date, Time, Enum, ForeignKey, Integer, String
from yma.database.core import Base
from yma.enums import EventType, YMAEventStatusType, YMAEventType
from yma.models import Pagination, TimeStampMixin, YMABase


class Event(Base, TimeStampMixin):
    """SQLAlchemy model for a Event."""

    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    code = Column(String(100), unique=True)
    event_type = Column(Enum(YMAEventType))
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    reference = Column(String(255))
    status = Column(Enum(YMAEventStatusType))

    # relationships
    course_id = Column(Integer, ForeignKey(
        "courses.id", ondelete="SET NULL"), nullable=True)


# Pydantic models
class EventBase(YMABase):
    code: str
    event_type: EventType
    date: str
    start_time: str
    end_time: str
    reference: str
    status: YMAEventStatusType


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    pass


class EventRead(EventBase):
    id: int


class EventPagination(Pagination):
    data: list[EventRead]
