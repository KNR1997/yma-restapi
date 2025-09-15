from typing import Optional
from fastapi import APIRouter, Depends, Query
from tortoise.expressions import Q

from yma.auth.permissions import AdminPermission, PermissionsDependency
from yma.exceptions import ConflictException, ResourceNotFoundException

from .models import SubjectCreate, SubjectPagination, SubjectRead, SubjectUpdate
from .repository import SubjectRepository
from .service import SubjectService


router = APIRouter()
service = SubjectService(SubjectRepository())


@router.get("", response_model=SubjectPagination)
async def paginated_subjects(
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

    total, data = await service.paginated(page=page, page_size=page_size, search=q)
    return SubjectPagination(
        data=data,
        itemsPerPage=10,
        page=page,
        page_size=page_size,
        total=total,
    )


@router.get("/{subject_id}", response_model=SubjectRead)
async def get_subject(subject_id: int):
    """Get a subject by its id."""
    subject = await service.get(subject_id)
    return subject


@router.post(
    "",
    response_model=SubjectRead,
    dependencies=[Depends(PermissionsDependency([AdminPermission]))]
)
async def create_subject(subject_in: SubjectCreate):
    """Create a new subject."""
    if await service.get_by_name(name=subject_in.name):
        raise ConflictException(
            "Subject with this name already exists", field="name")
    return await service.create(subject_in)


@router.put("/{subject_id}", response_model=SubjectRead)
async def update_subject(
    subject_id: int,
    subject_in: SubjectUpdate
):
    """Update a subject by its id."""
    subject = await service.get(subject_id=subject_id)
    if not subject:
        raise ResourceNotFoundException(
            "A subject with this id does not exist.")
    if subject_in.name != subject.name:
        if await service.get_by_name(name=subject_in.name):
            raise ConflictException(
                "Subject with this name already exists", field="name")
    return await service.update(subject=subject, subject_in=subject_in)


@router.delete("/{subject_id}", response_model=None)
async def delete_subject(subject_id: int):
    """Delete a subject, returning only an HTTP 200 OK if successful."""
    return await service.delete(subject_id)
