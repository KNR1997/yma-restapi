from sqlalchemy import Column, Enum, Integer, String
from yma.database.core import Base
from yma.enums import GenderType
from yma.models import Pagination, TimeStampMixin, YMABase


class Guardian(Base, TimeStampMixin):
    """SQLAlchemy model for a Guardian."""

    __tablename__ = "guardians"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    nic_number = Column(String(100), unique=True)
    phone_number = Column(String(100))
    gender = Column(Enum(GenderType))


# Pydantic models
class GuardianBase(YMABase):
    first_name: str
    last_name: str
    nic_number: str
    phone_number: str
    gender: GenderType


class GuardianCreate(GuardianBase):
    pass


class GuardianUpdate(GuardianBase):
    pass


class GuardianRead(GuardianBase):
    id: int


class GuardianPagination(Pagination):
    data: list[GuardianRead]
