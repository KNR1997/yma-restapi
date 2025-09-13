from pydantic import BaseModel
from uuid import UUID
from tortoise import fields, models

from yma.auth.models import UserCreate, UserRead, UserUpdate
from yma.enums import GradeType
from yma.models import Pagination


class Student(models.Model):
    user = fields.OneToOneField("models.YMAUser", related_name="student")
    student_number = fields.CharField(max_length=30, unique=True, index=True)
    grade = fields.CharEnumField(GradeType, index=True)
    is_admission_payed = fields.BooleanField(default=False)

    class Meta:
        table = "student"


# Pydantic models
class StudentBase(BaseModel):
    student_number: str
    grade: GradeType

    model_config = {
        "from_attributes": True
    }


class StudentCreate(BaseModel):
    user: UserCreate
    student_number: str
    grade: GradeType
    user_id: UUID | None = None


class StudentUpdate(BaseModel):
    user: UserUpdate
    student_number: str
    grade: GradeType
    user_id: UUID | None = None


class StudentRead(StudentBase):
    id: int
    user: UserRead


class StudentPagination(Pagination):
    data: list[StudentRead]
