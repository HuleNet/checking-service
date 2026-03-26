from typing import Any

from checking_service.core.base_error import BaseError


class ApplicationError(BaseError):
    code: str = "application_error"


class ValidationError(ApplicationError):
    pass
