from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Boolean, Float
from yma.database.core import Base
from yma.enums import CourseType, GradeType
from yma.models import Pagination, TimeStampMixin, YMABase


class Course(Base, TimeStampMixin):
    """SQLAlchemy model for a Course."""

    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    slug = Column(String(100))
    code = Column(String(100), unique=True)
    course_type = Column(Enum(CourseType), default=CourseType.ONLINE)
    grade = Column(Enum(GradeType))
    batch = Column(Integer, unique=True)
    is_active = Column(Boolean, default=True)
    fee = Column(Float, nullable=True)

    # relationships
    subject_id = Column(Integer, ForeignKey(
        "subjects.id", ondelete="SET NULL"), nullable=True)
    teacher_id = Column(Integer, ForeignKey(
        "users.id", ondelete="SET NULL"), nullable=True)


# Pydantic models
class CourseBase(YMABase):
    name: str
    slug: str
    code: str
    course_type: CourseType
    grade: GradeType
    batch: int
    is_active: bool
    fee: float
    subject_id: int
    teacher_id: int


class CourseCreate(CourseBase):
    pass


class CourseUpdate(CourseBase):
    pass


class CourseRead(CourseBase):
    id: int


class CoursePagination(Pagination):
    data: list[CourseRead]
