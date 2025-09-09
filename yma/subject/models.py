from slugify import slugify

from sqlalchemy.event import listen
from sqlalchemy import Column, String, Integer
from yma.database.core import Base
from yma.models import Pagination, TimeStampMixin, YMABase


class Subject(Base, TimeStampMixin):
    """SQLAlchemy model for a Subject."""

    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    slug = Column(String(100))
    code = Column(String(100), unique=True)


def generate_slug(target, value, oldvalue, initiator):
    """Creates a reasonable slug based on subject name."""
    if value and (not target.slug or value != oldvalue):
        target.slug = slugify(value, separator="_")


listen(Subject.name, "set", generate_slug)


# Pydantic models
class SubjectBase(YMABase):
    name: str
    code: str


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(SubjectBase):
    pass


class SubjectRead(SubjectBase):
    id: int


class SubjectPagination(Pagination):
    data: list[SubjectRead]
