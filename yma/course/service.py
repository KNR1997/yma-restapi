from .models import Course, CourseCreate, CourseUpdate


def get(*, db_session, course_id: int) -> Course | None:
    """Gets a course by id."""
    return db_session.query(Course).filter(Course.id == course_id).one_or_none()


def create(*, db_session, course_in: CourseCreate) -> Course:
    """Creates a new course."""
    course = Course(
        **course_in.model_dump(),
    )

    db_session.add(course)
    db_session.commit()
    return course


def update(
    *, db_session, course: Course, course_in: CourseUpdate
) -> Course:
    """Updates a course."""
    course_data = course.dict()
    update_data = course_in.model_dump(exclude_unset=True)

    for field in course_data:
        if field in update_data:
            setattr(Course, field, update_data[field])

    db_session.commit()
    return course


def delete(*, db_session, course_id: int):
    """Deletes a course."""
    course = (
        db_session.query(Course).filter(
            Course.id == course_id).one_or_none()
    )
    db_session.delete(course)
    db_session.commit()
