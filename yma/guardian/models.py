from pydantic import BaseModel
from tortoise import fields, models

from yma.enums import GenderType
from yma.models import Pagination


class Guardian(models.Model):
    id = fields.BigIntField(pk=True, index=True)
    first_name = fields.CharField(max_length=30)
    last_name = fields.CharField(max_length=30)
    nic_number = fields.CharField(max_length=30, unique=True)
    phone_number = fields.CharField(max_length=10)
    gender = fields.CharEnumField(GenderType)

    class Meta:
        table = "guardian"

# Pydantic models


class GuardianBase(BaseModel):
    first_name: str
    last_name: str
    nic_number: str
    phone_number: str
    gender: GenderType

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
