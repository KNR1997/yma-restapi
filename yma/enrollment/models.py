from pydantic import BaseModel
from tortoise import fields, models
import datetime
from datetime import time, date

from yma.course.models import Course, CourseRead
from yma.enums import EnrollmentStatusType
from yma.models import Pagination
from yma.student.models import Student, StudentRead
from yma.models import TimestampMixin


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


class EnrollmentPayment(models.Model, TimestampMixin):
    enrollment: fields.ForeignKeyRelation[Enrollment] = fields.ForeignKeyField(
        "models.Enrollment", related_name="enrollment_payments"
    )
    payment_month = fields.IntField()
    payment_year = fields.IntField()
    amount = fields.FloatField()
    # received_by: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
    #     "models.User", related_name="enrollment_payments"
    # )
    payment_date = fields.DateField(default=datetime.date.today)

    class Meta:
        table = "enrollment_payment"


# Pydantic models(Enrollment)
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


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


class EnrollmentUpdate(EnrollmentBase):
    pass


class EnrollmentRead(EnrollmentBase):
    id: int
    course: CourseRead
    student: StudentRead


class EnrollmentReadSimple(BaseModel):
    id: int
    course: CourseRead
    student: StudentRead


class EnrollmentPagination(Pagination):
    data: list[EnrollmentRead]


# Pydantic models(EnrollmentPayment)
class EnrollmentPaymentBase(BaseModel):
    payment_month: int
    payment_year: int
    amount: float
    payment_date: date

    model_config = {
        "from_attributes": True
    }


class EnrollmentPaymentCreate(BaseModel):
    enrollment_id: int
    payment_month: int
    payment_year: int
    amount: float


class EnrollmentPaymentRead(EnrollmentPaymentBase):
    id: int
    course: CourseRead
    student: StudentRead


class EnrollmentPaymentPagination(Pagination):
    data: list[EnrollmentPaymentRead]
