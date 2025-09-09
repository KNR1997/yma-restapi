from sqlalchemy import Column, Integer, String
from yma.database.core import Base
from yma.models import Pagination, TimeStampMixin, YMABase


class Hall(Base, TimeStampMixin):
    """SQLAlchemy model for a Hall."""

    __tablename__ = "halls"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    capacity = Column(Integer)


# Pydantic models
class HallBase(YMABase):
    name: str
    capacity: int


class HallCreate(HallBase):
    pass


class HallUpdate(HallBase):
    pass


class HallRead(HallBase):
    id: int


class HallPagination(Pagination):
    data: list[HallRead]
