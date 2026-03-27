from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreateSubmissionDTO:
    assignment_id: UUID
    language: str
    code: str
