from .models import Hall, HallCreate, HallUpdate


def get(*, db_session, hall_id: int) -> Hall | None:
    """Gets a hall by id."""
    return db_session.query(Hall).filter(Hall.id == hall_id).one_or_none()


def create(*, db_session, hall_in: HallCreate) -> Hall:
    """Creates a new hall."""
    hall = Hall(
        **hall_in.model_dump(),
    )

    db_session.add(hall)
    db_session.commit()
    return hall


def update(
    *, db_session, hall: Hall, hall_in: HallUpdate
) -> Hall:
    """Updates a hall."""
    hall_data = hall.dict()
    update_data = hall_in.model_dump(exclude_unset=True)

    for field in hall_data:
        if field in update_data:
            setattr(hall, field, update_data[field])

    db_session.commit()
    return hall


def delete(*, db_session, hall_id: int):
    """Deletes a hall."""
    hall = (
        db_session.query(Hall).filter(
            Hall.id == hall_id).one_or_none()
    )
    db_session.delete(hall)
    db_session.commit()
