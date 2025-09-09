from datetime import datetime, timedelta, timezone

from pydantic import EmailStr
from pydantic import Field, StringConstraints, ConfigDict, BaseModel
from pydantic import SecretStr

from typing import Annotated, ClassVar
from sqlalchemy import Column, DateTime, event

# Pydantic models...


class TimeStampMixin:
    """Adds created_at and updated_at timestamps."""

    created_at = Column(DateTime, default=lambda: datetime.now(
        timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(
        timezone.utc), nullable=False)

    @staticmethod
    def _update_timestamp(mapper, connection, target):
        """Automatically set updated_at before UPDATE."""
        target.updated_at = datetime.now(timezone.utc)

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, "before_update", cls._update_timestamp)


class YMABase(BaseModel):
    """Base Pydantic model with shared config for Dispatch models."""
    model_config: ClassVar[ConfigDict] = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        str_strip_whitespace=True,
        json_encoders={
            # custom output conversion for datetime
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if v else None,
            SecretStr: lambda v: v.get_secret_value() if v else None,
        },
    )

class Pagination(YMABase):
    """Pydantic model for paginated results."""
    itemsPerPage: int
    page: int
    page_size: int
    total: int
