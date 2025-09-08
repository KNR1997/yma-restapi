from .models import Subject, SubjectCreate, SubjectUpdate
from fastapi import HTTPException, status
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError


def get(*, db_session, subject_id: int) -> Subject | None:
    """Gets a subject by id."""
    return db_session.query(Subject).filter(Subject.id == subject_id).one_or_none()


def create(*, db_session, subject_in: SubjectCreate) -> Subject:
    """Creates a new subject."""
    subject = Subject(
        **subject_in.model_dump(),
    )

    db_session.add(subject)
    db_session.commit()
    return subject


def update(
    *, db_session, subject: Subject, subject_in: SubjectUpdate
) -> Subject:
    """Updates a subject."""
    try:
        print('updating subject 2 -------', getattr(subject_in, "name", None))

        # Pydantic model_dump might raise ValidationError or AttributeError
        try:
            update_data = subject_in.model_dump(exclude_unset=True)
        except ValidationError as ve:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid input data: {ve.errors()}",
            )
        except AttributeError as ae:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Bad input object: {ae}",
            )

        print('updating subject 3 -------: ',
              getattr(subject_in, "name", None))

        subject_data = subject.dict()
        print('herrrrrrrrrrrrrrrrrrrr----------')
        for field in subject_data:
            if field in update_data:
                setattr(subject, field, update_data[field])

        db_session.commit()
        db_session.refresh(subject)  # ensure updated values
        return subject

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while updating the subject.",
        )
    except Exception as e:
        db_session.rollback()
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )


def delete(*, db_session, subject_id: int):
    """Deletes a subject."""
    subject = (
        db_session.query(Subject).filter(
            Subject.id == subject_id).one_or_none()
    )
    db_session.delete(subject)
    db_session.commit()
