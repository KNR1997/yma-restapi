from .models import Guardian, GuardianCreate, GuardianUpdate


def get(*, db_session, guardian_id: int) -> Guardian | None:
    """Gets a guardian by id."""
    return db_session.query(Guardian).filter(Guardian.id == guardian_id).one_or_none()


def create(*, db_session, guardian_in: GuardianCreate) -> Guardian:
    """Creates a new guardian."""
    guardian = Guardian(
        **guardian_in.model_dump(),
    )

    db_session.add(guardian)
    db_session.commit()
    return guardian


def update(
    *, db_session, guardian: Guardian, guardian_in: GuardianUpdate
) -> Guardian:
    """Updates a guardian."""
    guardian_data = guardian.dict()
    update_data = guardian_in.model_dump(exclude_unset=True)

    for field in guardian_data:
        if field in update_data:
            setattr(guardian, field, update_data[field])

    db_session.commit()
    return guardian


def delete(*, db_session, guardian_id: int):
    """Deletes a guardian."""
    guardian = (
        db_session.query(Guardian).filter(
            Guardian.id == guardian_id).one_or_none()
    )
    db_session.delete(guardian)
    db_session.commit()
