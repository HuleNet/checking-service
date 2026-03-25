from dataclasses import dataclass
from uuid import UUID

from checking_service.domain.enums.status import Status
from checking_service.domain.domain_errors import InvariantViolationError


@dataclass(frozen=True)
class ExecutionResult:
    id: UUID
    submission_id: UUID
    input_case_id: UUID
    status: Status
    logs: str
    execution_time_sec: float

    def __post_init__(self) -> None:
        self._check_invariants()

    def _check_invariants(self) -> None:
        if self.execution_time_sec < 0:
            raise InvariantViolationError(
                "Execution time is negative number",
                model="ExecutionResult",
                field="execution_time_sec",
                value=self.execution_time_sec,
            )
