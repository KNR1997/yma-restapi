from enum import StrEnum


class UserRole(StrEnum):
    super_admin = "super_admin"
    admin = "admin"
    teacher = "teacher"
    student = "student"


class CourseType(StrEnum):
    ONLINE = "ONLINE"
    PHYSICAL = "PHYSICAL"


class GradeType(StrEnum):
    GRADE_6 = "GRADE_6"
    GRADE_7 = "GRADE_7"
    GRADE_8 = "GRADE_8"
    GRADE_9 = "GRADE_9"
    GRADE_10 = "GRADE_10"
    GRADE_11 = "GRADE_11"


class EventType(StrEnum):
    COURSE = "COURSE"
    EXAM = "EXAM"


class EventStatusType(StrEnum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class EnrollmentStatusType(StrEnum):
    ACTIVE = "ACTIVE"
    LOCKED = "LOCKED"
    # DROPPED = "DROPPED"


class GenderType(StrEnum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class MethodType(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class PayerType(StrEnum):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"
    MANAGER = "MANAGER"
    INSTITUTE = "INSTITUTE"


class PaymentMethodType(StrEnum):
    CASH = "CASH"
    CARD = "CARD"


class PaymentType(StrEnum):
    ADMISSION_FEE = "ADMISSION_FEE"
    COURSE_FEE = "COURSE_FEE"
    EXAM_FEE = "EXAM_FEE"
    SALARY = "SALARY"
