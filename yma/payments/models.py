import datetime
from pydantic import BaseModel
from tortoise import fields, models
from uuid import UUID

from yma.enums import PayerType, PaymentMethodType, PaymentType
from yma.models import TimestampMixin, Pagination


class Payment(models.Model, TimestampMixin):
    payer_type = fields.CharEnumField(PayerType)
    payer_user = fields.ForeignKeyField("models.YMAUser", null=True, related_name="payments_made")
    payer_name = fields.CharField(max_length=255, null=True)
    payee_type = fields.CharEnumField(PayerType)
    payee_user = fields.ForeignKeyField("models.YMAUser", null=True, related_name="payments_received")
    payee_name = fields.CharField(max_length=255, null=True)
    amount = fields.FloatField()
    payment_type = fields.CharEnumField(PaymentType, description="Payment type(CourseFee, Admission, Salary)")
    payment_method = fields.CharEnumField(PaymentMethodType)
    reference = fields.CharField(max_length=255, null=True)
    # received_by: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
    #     "models.User", related_name="payments",
    # )
    payment_date = fields.DateField(default=datetime.date.today)

    class Meta:
        table = "payment"


# Pydantic models(Payment)
class PaymentBase(BaseModel):
    payer_type: PayerType
    payee_type: PayerType
    amount: float
    payment_type: PaymentType

    model_config = {
        "from_attributes": True
    }


class PaymentCreate(BaseModel):
    payer_user_id: UUID
    amount: float


class PaymentUpdate(PaymentCreate):
    ...


class PaymentRead(PaymentBase):
    id: int


class PaymentPagination(Pagination):
    data: list[PaymentRead]
