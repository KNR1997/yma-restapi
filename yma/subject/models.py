from pydantic import BaseModel, Field
from tortoise import fields, models

from yma.models import Pagination


class Subject(models.Model):
    id = fields.BigIntField(pk=True, index=True)
    name = fields.CharField(max_length=20, unique=True)
    code = fields.CharField(max_length=20)

    class Meta:
        table = "subject"


# Pydantic models
class SubjectBase(BaseModel):
    name: str = Field(description="Maths")
    code: str = Field(description="MAT")

    model_config = {
        "from_attributes": True
    }


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(SubjectBase):
    pass


class SubjectRead(SubjectBase):
    id: int


class SubjectPagination(Pagination):
    data: list[SubjectRead]
