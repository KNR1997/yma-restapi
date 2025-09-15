from typing import Optional
from fastapi import APIRouter, Query, Depends
from tortoise.expressions import Q
from tortoise.transactions import atomic

from yma.course.repos import CourseRepository
from yma.auth.repository import UserRepository
from yma.student.repository import StudentRepository
from yma.payments.repository import PaymentRepository
from yma.enrollment.repos import EnrollmentPaymentRepository, EnrollmentRepository
from yma.course.service import CourseService
from yma.student.service import StudentService
from yma.payments.service import PaymentService
from yma.enrollment.services import EnrollmentPaymentService, EnrollmentService
from yma.auth.services import UserService
from yma.course.models import CoursePagination
from yma.enrollment.models import EnrollmentPaymentCreate, EnrollmentUpdate
from yma.student.models import StudentCreate, StudentPagination, StudentRead, StudentUpdate, AdmissionPaymentCreate, StudentPartialUpdate, CoursePaymentCreate
from yma.payments.models import PaymentCreate
from yma.auth.permissions import AdminPermission, PermissionsDependency
from yma.exceptions import ResourceNotFoundException, ConflictException


router = APIRouter()
service = StudentService(StudentRepository())
user_service = UserService(UserRepository())
course_service = CourseService(CourseRepository())
payment_service = PaymentService(PaymentRepository())
enrollment_service = EnrollmentService(EnrollmentRepository())
enrollment_payment_service = EnrollmentPaymentService(EnrollmentPaymentRepository())


@router.get("", response_model=StudentPagination)
async def paginated_students(
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
    return StudentPagination(
        data=data,
        itemsPerPage=10,
        page=page,
        page_size=page_size,
        total=total,
    )


@router.get("/{student_id}", response_model=StudentRead)
async def get_student(student_id: int):
    """Get a student by its id."""
    student = await service.get(student_id)
    return student


@atomic()
@router.post("", response_model=StudentRead)
async def create_student(student_in: StudentCreate):
    """Create a new student."""
    user = await user_service.create(student_in.user)
    student_in.user_id = user.id
    return await service.create(student_in)


@atomic()
@router.put("/{student_id}", response_model=StudentRead)
async def update_student(
    student_id: int,
    student_in: StudentUpdate
):
    """Update a student by its id."""
    student = await service.get(student_id=student_id)
    if not student:
        raise ResourceNotFoundException(
            "A student with this id does not exist.")
    user = await user_service.get(user_id=student.user.id)
    if not user:
        raise ResourceNotFoundException(
            "A user for student does not exist.")
    await user_service.update(user=user, user_in=student_in.user)
    return await service.update(student=student, student_in=student_in)


@router.delete("/{student_id}", response_model=None)
async def delete_student(student_id: int):
    """Delete a student, returning only an HTTP 200 OK if successful."""
    return await service.delete(student_id)


@router.get("/{student_id}/available-courses", response_model=CoursePagination)
async def get_available_courses(
    student_id: int,
    page: int = Query(1, description="Page Number"),
    page_size: int = Query(10, description="Items Per Page"),
):
    """Get available courses for student to enroll."""
    student = await service.get(student_id=student_id)
    if not student:
        raise ResourceNotFoundException(
            "A student with this id does not exist.")
    q = Q(grade=student.grade)
    total, data = await course_service.paginated(page=page, page_size=page_size, search=q)
    return CoursePagination(
        data=data,
        itemsPerPage=10,
        page=page,
        page_size=page_size,
        total=total,
    )


@router.get("/{student_id}/enrolled-courses", response_model=CoursePagination)
async def get_enrolled_courses(
    student_id: int,
    page: int = Query(1, description="Page Number"),
    page_size: int = Query(10, description="Items Per Page"),
):
    """Get available courses for student to enroll."""
    student = await service.get(student_id=student_id)
    if not student:
        raise ResourceNotFoundException(
            "A student with this id does not exist.")
    q = Q(grade=student.grade)
    total, data = await course_service.get_student_enrolled_paginated(student_id=student_id, page=page, page_size=page_size, search=q)
    return CoursePagination(
        data=data,
        itemsPerPage=10,
        page=page,
        page_size=page_size,
        total=total,
    )


@atomic()
@router.post(
    "/{student_id}/payments/admission",
    dependencies=[Depends(PermissionsDependency([AdminPermission]))],
    response_model=StudentRead)
async def create_admission_payment(
    student_id: int,
    data_in: AdmissionPaymentCreate
):
    """Create a new admission payment."""
    student = await service.get(student_id)
    if not student:
        raise ResourceNotFoundException(
            "A student with this id does not exist.")
    if student.is_admission_payed:
        raise ConflictException("Admission already paid")

    await payment_service.create_admission_payment(
        PaymentCreate(
            payer_user_id=student.user.id,
            amount=data_in.admission,
        )
    )
    return await service.mark_admission_paid(student)


@atomic()
@router.post(
    "/{student_id}/payments/course",
    dependencies=[Depends(PermissionsDependency([AdminPermission]))],
    response_model=StudentRead)
async def create_course_payment(
    student_id: int,
    data_in: CoursePaymentCreate
):
    """Create a course payment."""
    student = await service.get(student_id)
    if not student:
        raise ResourceNotFoundException(
            "A student with this id does not exist.")
    if student.is_admission_payed:
        raise ConflictException("Admission already paid")

    enrollment = await enrollment_service.get_by_student_and_course(student_id=student_id, course_id=data_in.course_id)
    if not enrollment:
        raise ResourceNotFoundException(
            "A enrollment for this payment does not exist.")

    # Check if already paid for this specific month/year
    already_paid = (enrollment.last_payment_month == data_in.month and
                    enrollment.last_payment_year == data_in.year)

    if already_paid:
        raise ConflictException(
            "Already paid for this month", field="month")

    await enrollment_payment_service.create(
        EnrollmentPaymentCreate(
            enrollment_id=enrollment.id,
            payment_month=data_in.month,
            payment_year=data_in.year,
            amount=data_in.amount,
        )
    )

    await payment_service.create_course_payment(
        PaymentCreate(
            payer_user_id=student.user.id,
            amount=data_in.amount,
        )
    )

    return await enrollment_service.update(
        EnrollmentUpdate(
            status=EnrollmentStatusType.ACTIVE,
            last_payment_month=data_in.month,
            last_payment_year=data_in.year,
            is_active=True,
        )
    )
