from pydantic import BaseModel
from tortoise import fields, models

from yma.models import Pagination


class Hall(models.Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    capacity = fields.IntField()

    class Meta:
        table = "hall"


# Pydantic models
class HallBase(BaseModel):
    name: str
    capacity: int

    model_config = {
        "from_attributes": True
    }


class HallCreate(BaseModel):
    name: str
    capacity: int


class HallUpdate(HallCreate):
    ...


class HallRead(HallBase):
    id: int


class HallPagination(Pagination):
    data: list[HallRead]
