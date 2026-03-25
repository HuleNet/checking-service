from typing import Any, Tuple, Dict


class DomainError(Exception):
    code: str = "domain_error"

    def __init__(self, message: str, **context: Any) -> None:
        super().__init__(message)
        self.message = message
        self.context = context


class InvariantViolationError(DomainError):
    def __init__(self, message: str, *, model: str, field: str, value: Any) -> None:
        super().__init__(message, model=model, field=field, value=value)
