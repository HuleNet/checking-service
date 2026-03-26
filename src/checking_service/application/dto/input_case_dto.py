from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreateInputCaseDTO:
    assignment_id: UUID
    language: str
    input_data: str
    expected_output: str
