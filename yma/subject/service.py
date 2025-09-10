from .models import Subject, SubjectCreate, SubjectUpdate


def get(*, db_session, subject_id: int) -> Subject | None:
    """Gets a subject by id."""
    return db_session.query(Subject).filter(Subject.id == subject_id).one_or_none()


def get_by_name(*, db_session, name: str) -> Subject | None:
    """Gets an organization by its name."""
    return db_session.query(Subject).filter(Subject.name == name).one_or_none()


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
    subject_data = subject.dict()
    update_data = subject_in.model_dump(exclude_unset=True)

    for field in subject_data:
        if field in update_data:
            setattr(subject, field, update_data[field])

    db_session.commit()
    return subject


def delete(*, db_session, subject_id: int):
    """Deletes a subject."""
    subject = (
        db_session.query(Subject).filter(
            Subject.id == subject_id).one_or_none()
    )
    db_session.delete(subject)
    db_session.commit()
