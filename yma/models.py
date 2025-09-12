from pydantic import BaseModel
from tortoise import fields, models


class TimestampMixin:
    created_at = fields.DatetimeField(auto_now_add=True, index=True)
    updated_at = fields.DatetimeField(auto_now=True, index=True)


class Pagination(BaseModel):
    """Pydantic model for paginated results."""
    itemsPerPage: int
    page: int
    page_size: int
    total: int
