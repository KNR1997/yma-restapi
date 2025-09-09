from fastapi import Depends
from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy.inspection import inspect
from starlette.requests import Request
from typing import Annotated

from yma.database.logging import SessionTracker


def get_db(request: Request) -> Session:
    """Get database session from request state."""
    session = request.state.db
    if not hasattr(session, "_dispatch_session_id"):
        session._dispatch_session_id = SessionTracker.track_session(
            session, context="fastapi_request"
        )
    return session


DbSession = Annotated[Session, Depends(get_db)]


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    def dict(self):
        """Returns a dict representation of a model."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        """Readable representation for debugging."""
        ids = inspect(self).identity
        id_str = ("#" + str(ids[0])) if ids else ""
        return f"<{self.__class__.__name__} {id_str}>"
