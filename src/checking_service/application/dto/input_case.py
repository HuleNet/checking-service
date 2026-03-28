from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreateInputCaseDTO:
    assignment_id: UUID
    language: str
    input_data: str
    expected_output: str


@dataclass(frozen=True)
class UpdateInputCaseDTO:
    input_data: str
    expected_output: str


@dataclass(frozen=True)
class GetInputCaseDTO:
    assignment_id: UUID
    language: str


@dataclass(frozen=True)
class InputCaseDTO:
    id: UUID
    assignment_id: UUID
    language: str
    input_data: str
    expected_output: str
