from enum import StrEnum


class DispatchEnum(StrEnum):
    """
    A custom Enum class that extends StrEnum.

    This class inherits all functionality from StrEnum, including
    string representation and automatic value conversion to strings.

    Example:
        class Visibility(DispatchEnum):
            OPEN = "Open"
            RESTRICTED = "Restricted"

        assert str(Visibility.OPEN) == "Open"

    Note:
        In `3.12` we will get `__contains__` functionality:

        DeprecationWarning: in 3.12 __contains__ will no longer raise TypeError, but will return True or
        False depending on whether the value is a member or the value of a member
    """

    pass  # No additional implementation needed


class Visibility(DispatchEnum):
    open = "Open"
    restricted = "Restricted"


class SearchTypes(DispatchEnum):
    definition = "Definition"
    document = "Document"
    incident = "Incident"
    incident_priority = "IncidentPriority"
    incident_type = "IncidentType"
    individual_contact = "IndividualContact"
    plugin = "Plugin"
    query = "Query"
    search_filter = "SearchFilter"
    case = "Case"
    service = "Service"
    source = "Source"
    tag = "Tag"
    task = "Task"
    team_contact = "TeamContact"
    term = "Term"


class UserRoles(DispatchEnum):
    super_admin = "super_admin"
    admin = "admin"
    teacher = "teacher"
    student = "student"


class CourseType(DispatchEnum):
    ONLINE = "ONLINE"
    PHYSICAL = "PHYSICAL"


class GradeType(DispatchEnum):
    GRADE_5 = "GRADE_5"
    GRADE_6 = "GRADE_6"
    GRADE_7 = "GRADE_7"
    GRADE_8 = "GRADE_8"
    GRADE_9 = "GRADE_9"
    GRADE_10 = "GRADE_10"
    GRADE_11 = "GRADE_11"


class GenderType(DispatchEnum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class YMAEventType(DispatchEnum):
    COURSE = "COURSE"
    EXAM = "EXAM"


class YMAEventStatusType(DispatchEnum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class DocumentResourceTypes(DispatchEnum):
    case = "dispatch-case-document"
    executive = "dispatch-executive-report-document"
    incident = "dispatch-incident-document"
    review = "dispatch-incident-review-document"
    tracking = "dispatch-incident-sheet"


class DocumentResourceReferenceTypes(DispatchEnum):
    conversation = "dispatch-conversation-reference-document"
    faq = "dispatch-incident-reference-faq-document"


class DocumentResourceTemplateTypes(DispatchEnum):
    case = "dispatch-case-document-template"
    executive = "dispatch-executive-report-document-template"
    incident = "dispatch-incident-document-template"
    review = "dispatch-incident-review-document-template"
    tracking = "dispatch-incident-tracking-template"
    forms = "dispatch-forms-export-template"


class EventType(DispatchEnum):
    other = "Other"  # default and catch-all (x resource created/updated, etc.)
    # for fields like title, description, tags, type, etc.
    field_updated = "Field updated"
    # for priority, status, or severity changes
    assessment_updated = "Assessment updated"
    # for added/removed users and role changes
    participant_updated = "Participant updated"
    # for stopwatch-reacted messages from Slack
    imported_message = "Imported message"
    custom_event = "Custom event"  # for user-added events (new feature)


class SubjectNames(DispatchEnum):
    CASE = "Case"
    INCIDENT = "Incident"
    SIGNAL = "Signal"
