from dataclasses import dataclass
from uuid import UUID

from checking_service.domain.enums.status import Status
from checking_service.domain.errors.execution_result_errors import (
    ExecutionResultNegativeExecutionMemoryError,
    ExecutionResultNegativeExecutionTimeError,
)


@dataclass(frozen=True)
class ExecutionResult:
    id: UUID
    submission_id: UUID
    input_case_id: UUID
    status: Status
    logs: str
    execution_time_sec: float
    execution_memory_mb: int

    def __post_init__(self) -> None:
        self._check_invariants()

    def _check_invariants(self) -> None:
        if self.execution_time_sec < 0:
            raise ExecutionResultNegativeExecutionTimeError(
                "ExecutionResult.execution_time_sec is negative"
            )

        if self.execution_memory_mb < 0:
            raise ExecutionResultNegativeExecutionMemoryError(
                "ExecutionResult.execution_memory_mb is negative"
            )
