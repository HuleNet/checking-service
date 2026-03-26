from typing import Any

from checking_service.core.base_error import BaseError


class DomainError(BaseError):
    code: str = "domain_error"


class InvariantViolationError(DomainError):
    def __init__(self, message: str, *, model: str, field: str, value: Any) -> None:
        super().__init__(
            message,
            context={
                "model": model,
                "field": field,
                "value": value,
            },
        )


class UnsupportedTypeError(DomainError):
    def __init__(
        self,
        message: str,
        *,
        field: str,
        value: Any,
        allowed: list[str],
    ) -> None:
        super().__init__(
            message,
            context={
                "field": field,
                "value": value,
                "allowed": allowed,
            },
        )
