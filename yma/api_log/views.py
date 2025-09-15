from typing import Optional
from fastapi import APIRouter, Query
from tortoise.expressions import Q

from yma.exceptions import ConflictException, ResourceNotFoundException

from .models import ApiCreate, ApiPagination, ApiRead, ApiUpdate
from .repository import ApiLogRepository
from .service import ApiLogService


router = APIRouter()
service = ApiLogService(ApiLogRepository())


@router.get("", response_model=ApiPagination)
async def paginated_apis(
    page: int = Query(1, description="Page Number"),
    page_size: int = Query(10, description="Items Per Page"),
    search: Optional[str] = Query("", description="Subject Name for Search"),
    searchJoin: str = Query(
        "and", description="'and' or 'or' join for multiple search conditions"),
):
    q = Q()
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

    total, data = await service.paginated_apis(page=page, page_size=page_size, search=q)
    return apiPagination(
        data=data,
        itemsPerPage=10,
        page=page,
        page_size=page_size,
        total=total,
    )
