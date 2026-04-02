from dataclasses import dataclass
from uuid import UUID

from checking_service.domain.enums.language import Language
from checking_service.domain.errors.domain_errors import InvariantViolationError


@dataclass(frozen=True)
class InputCase:
    id: UUID
    assignment_id: UUID
    language: Language
    input_data: str
    expected_output: str

    def __post_init__(self) -> None:
        self._check_invariants()

    def _check_invariants(self) -> None:
        if not self.input_data:
            raise InvariantViolationError(
                "Input data is empty",
                context={
                    "model": "InputCase",
                    "field": "input_data",
                    "value": self.input_data,
                },
            )

        if not self.expected_output:
            raise InvariantViolationError(
                "Expected output is empty",
                context={
                    "model": "InputCase",
                    "field": "expected_output",
                    "value": self.expected_output,
                },
            )
