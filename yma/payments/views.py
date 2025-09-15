from typing import Optional
from fastapi import APIRouter, Query
from tortoise.expressions import Q

from yma.exceptions import ConflictException, ResourceNotFoundException
from yma.payments.models import PaymentPagination, PaymentCreate, PaymentRead
from yma.payments.repository import PaymentRepository
from yma.payments.service import PaymentService
from yma.enrollment.repos import EnrollmentRepository
from yma.enums import PaymentType


router = APIRouter()
service = PaymentService(PaymentRepository())


@router.get("", response_model=PaymentPagination)
async def paginated_payments(
    payment_type: PaymentType,
    page: int = Query(1, description="Page Number"),
    page_size: int = Query(10, description="Items Per Page"),
    search: Optional[str] = Query("", description="Subject Name for Search"),
    searchJoin: str = Query(
        "and", description="'and' or 'or' join for multiple search conditions"),
):
    q = Q(payment_type=payment_type)
    if search:
        # Example: search="name:english;status:active"
        filters = search.split(";")
        for f in filters:
            try:
                field, value = f.split(":", 1)
                lookup = {f"{field}__icontains": value}
                condition = Q(**lookup)
                if searchJoin.lower() == "or":
                    q |= condition
                else:
                    q &= condition
            except ValueError:
                continue  # skip invalid filter format

    total, data = await service.paginated(page=page, page_size=page_size, search=q)
    return PaymentPagination(
        data=data,
        itemsPerPage=10,
        page=page,
        page_size=page_size,
        total=total,
    )
