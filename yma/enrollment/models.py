from pydantic import BaseModel
from tortoise import fields, models

from yma.course.models import Course
from yma.enums import EnrollmentStatusType
from yma.models import Pagination
from yma.student.models import Student


class Enrollment(models.Model):
    student: fields.ForeignKeyRelation[Student] = fields.ForeignKeyField(
        "models.Student", related_name="enrollments"
    )
    course: fields.ForeignKeyRelation[Course] = fields.ForeignKeyField(
        "models.Course", related_name="enrollments"
    )
    status = fields.CharEnumField(
        EnrollmentStatusType, default=EnrollmentStatusType.LOCKED, index=True)
    last_payment_month = fields.IntField(
        description="Last paid month (1-12)", default=0)
    last_payment_year = fields.IntField(
        description="Last paid year", default=0)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "enrollment"


# Pydantic models
class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int
    status: EnrollmentStatusType
    last_payment_month: int
    last_payment_year: int
    is_active: bool

    model_config = {
        "from_attributes": True
    }


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentUpdate(EnrollmentBase):
    pass


class EnrollmentRead(EnrollmentBase):
    id: int


class EnrollmentPagination(Pagination):
    data: list[EnrollmentRead]
