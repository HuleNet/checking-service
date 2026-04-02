from typing import Any

from checking_service.domain.errors.base_error import BaseError


class DomainError(BaseError):
    code = "domain_error"


class InvariantViolationError(DomainError):
    code = "invariant_violation"


class UnsupportedTypeError(DomainError):
    code = "unsupported_type"
