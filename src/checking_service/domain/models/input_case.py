from dataclasses import dataclass
from uuid import UUID

from checking_service.domain.enums.language import Language
from checking_service.domain.errors.input_case_errors import (
    InputCaseEmptyInputDataAndExpectedOutputError,
)


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
        if not self.input_data and not self.expected_output:
            raise InputCaseEmptyInputDataAndExpectedOutputError(
                "InputCase.input_data and InputCase.expected_output are empty"
            )
