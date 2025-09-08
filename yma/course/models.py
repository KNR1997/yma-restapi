from sqlalchemy import Column, Integer, String
from yma.db_core.core import Base
from yma.models import TimeStampMixin


class Course(Base, TimeStampMixin):
    """SQLAlchemy model for a Subject."""

    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
