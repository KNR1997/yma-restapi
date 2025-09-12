from pydantic import BaseModel
from tortoise import fields, models
from uuid import UUID

from yma.auth.models import UserRead, YMAUser
from yma.enums import CourseType, GradeType
from yma.models import Pagination
from yma.subject.models import Subject, SubjectRead


class Course(models.Model):
    id = fields.BigIntField(pk=True, index=True)
    course_type = fields.CharEnumField(CourseType, null=True, index=True)
    name = fields.CharField(max_length=150, unique=True, index=True)
    code = fields.CharField(max_length=150, index=True)
    subject: fields.ForeignKeyRelation[Subject] = fields.ForeignKeyField(
        "models.Subject", related_name="courses"
    )
    teacher: fields.ForeignKeyRelation[YMAUser] = fields.ForeignKeyField(
        "models.YMAUser", related_name="courses"
    )
    grade = fields.CharEnumField(GradeType, index=True)
    batch = fields.IntField(default=1, index=True)
    is_active = fields.BooleanField(default=True)
    fee = fields.FloatField(null=True)

    class Meta:
        table = "course"


class CourseTopic(models.Model):
    id = fields.BigIntField(pk=True, index=True)
    course: fields.ForeignKeyRelation[Course] = fields.ForeignKeyField(
        "models.Course", related_name="course_topics"
    )
    name = fields.TextField()
    description = fields.TextField(null=True)

    class Meta:
        table = "course_topic"


# Pydantic models
class CourseBase(BaseModel):
    name: str
    code: str
    course_type: CourseType
    grade: GradeType
    batch: int
    is_active: bool
    fee: float
    subject_id: int
    teacher_id: UUID

    model_config = {
        "from_attributes": True
    }


class CourseCreate(BaseModel):
    name: str
    code: str
    course_type: CourseType
    grade: GradeType
    batch: int
    fee: float
    subject_id: int
    teacher_id: UUID


class CourseUpdate(BaseModel):
    fee: float
    course_type: CourseType


class CourseRead(CourseBase):
    id: int


class CoursePageData(CourseRead):
    subject: SubjectRead
    teacher: UserRead


class CoursePagination(Pagination):
    data: list[CourseRead]
