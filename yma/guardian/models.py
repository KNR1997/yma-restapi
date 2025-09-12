from pydantic import BaseModel, Field
from tortoise import fields, models

from yma.enums import GradeType
from yma.models import Pagination


class Guardian(models.Model):
    id = fields.BigIntField(pk=True, index=True)
    first_name = fields.CharField(max_length=30)
    last_name = fields.CharField(max_length=30)
    nic_number = fields.CharField(max_length=30, unique=True)
    phone_number = fields.CharField(max_length=10)
    gender = fields.CharEnumField(GradeType)

    class Meta:
        table = "guardian"

# Pydantic models


class GuardianBase(BaseModel):
    first_name: str
    last_name: str
    nic_number: str
    phone_number: str
    gender: GradeType

    model_config = {
        "from_attributes": True
    }


class GuardianCreate(GuardianBase):
    pass


class GuardianUpdate(GuardianBase):
    pass


class GuardianRead(GuardianBase):
    id: int


class GuardianPagination(Pagination):
    data: list[GuardianRead]
