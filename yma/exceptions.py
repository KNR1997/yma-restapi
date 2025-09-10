from typing import Any, List


class AppException(Exception):
    """Base application exception with consistent response format."""

    status_code: int = 400
    detail: Any = {"detail": [{"msg": "An error occurred."}]}

    def __init__(self, detail: Any = None):
        if detail:
            self.detail = detail


class NotFoundError(AppException):
    status_code = 404

    def __init__(self, msg: str = "Resource not found."):
        super().__init__([{"msg": msg}])


class DuplicateNameError(AppException):
    status_code = 400

    def __init__(self, field: str = "name"):
        super().__init__([{"msg": f"{field} already exists.", "loc": [field]}])


class BadRequestError(AppException):
    status_code = 400

    def __init__(self, msg: str):
        super().__init__([{"msg": msg}])
