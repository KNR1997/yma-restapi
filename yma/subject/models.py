from sqlalchemy import Column, String, Integer
from yma.db_core.core import Base
from yma.models import TimeStampMixin, YMABase


class Subject(Base, TimeStampMixin):
    """SQLAlchemy model for a Subject."""

    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)


# Pydantic models
class SubjectBase(YMABase):
    name: str


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(SubjectBase):
    pass


class SubjectRead(SubjectBase):
    id: int
    name: str
