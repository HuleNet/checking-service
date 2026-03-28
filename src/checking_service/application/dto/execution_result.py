from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass(frozen=True)
class ExecutionResultDTO:
    id: UUID
    submission_id: UUID
    input_case_id: UUID
    status: str
    logs: str
    execution_time_sec: float
    created_at: datetime
