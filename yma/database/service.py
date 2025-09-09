from fastapi import Depends, Query

from typing import Annotated, Optional

from pydantic import StringConstraints
from sqlalchemy import asc, desc
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Session
from starlette.requests import Request

from yma.database.logging import SessionTracker

# allows only printable characters
QueryStr = Annotated[str, StringConstraints(pattern=r"^[ -~]+$", min_length=1)]


def search_filter_sort_paginate(
    db_session: Session,
    model,
    page: int = 1,
    items_per_page: int | None = 10,
    query_str: str | None = None,
    search: str | None = None,
    search_join: str | None = None,
    sort_by: list[str] | None = None,
    descending: list[bool] | None = None,
):
    query = db_session.query(model)

    if search:
        # Format: "field:value"
        if ":" in search:
            field, value = search.split(":", 1)
            column = getattr(model, field, None)
            if column is not None:
                query = query.filter(column.ilike(f"%{value}%"))

    # TODO: add search logic here if needed
    if query_str:
        # Example: simple case-insensitive LIKE search on a "name" column
        if hasattr(model, "name"):
            query = query.filter(model.name.ilike(f"%{query_str}%"))

    # Sorting
    if sort_by:
        for i, field in enumerate(sort_by):
            column = getattr(model, field, None)
            if column is not None:
                order = desc(
                    column) if descending and descending[i] else asc(column)
                query = query.order_by(order)

    # Pagination
    if items_per_page == -1:
        items_per_page = None

    try:
        total = query.count()
        if items_per_page:
            query = query.offset(
                (page - 1) * items_per_page).limit(items_per_page)
    except ProgrammingError:
        return {"items": [], "itemsPerPage": items_per_page, "page": page, "total": 0}

    return {
        "data": query.all(),
        "itemsPerPage": items_per_page,
        "page_size": items_per_page,
        "page": page,
        "total": total,
    }


def get_db(request: Request) -> Session:
    """Get database session from request state."""
    session = request.state.db
    if not hasattr(session, "_dispatch_session_id"):
        session._dispatch_session_id = SessionTracker.track_session(
            session, context="fastapi_request"
        )
    return session


DbSession = Annotated[Session, Depends(get_db)]


def common_parameters(
    db_session: DbSession,  # however you inject your session
    page: int = Query(1, gt=0),
    items_per_page: int = Query(10, alias="itemsPerPage", gt=0),
    query_str: str | None = Query(None, alias="q"),
    search: str | None = None,
    search_join: str | None = None,
    sort_by: list[str] = Query([], alias="sortBy[]"),
    descending: list[bool] = Query([], alias="descending[]"),
):
    return {
        "db_session": db_session,
        "page": page,
        "items_per_page": items_per_page,
        "query_str": query_str,
        "search": search,
        "search_join": search_join,
        "sort_by": sort_by,
        "descending": descending,
    }


CommonParameters = Annotated[dict, Depends(common_parameters)]
