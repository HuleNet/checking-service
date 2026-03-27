from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreateExecutionResultDTO:
    submission_id: UUID
    input_case_id: UUID
    status: str
    logs: str
    execution_time_sec: float
