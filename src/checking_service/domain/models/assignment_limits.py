from dataclasses import dataclass
from uuid import UUID

from checking_service.domain.errors.assignment_limits_errors import (
    AssignmentLimitsNegativeMemoryLimitError,
    AssignmentLimitsNegativeTimeLimitError,
)


@dataclass(frozen=True)
class AssignmentLimits:
    assignment_id: UUID
    time_limit_sec: float
    memory_limit_mb: int

    def __post_init__(self) -> None:
        self._check_invariants()

    def _check_invariants(self) -> None:
        if self.time_limit_sec < 0:
            raise AssignmentLimitsNegativeTimeLimitError(
                "AssignmentLimits.time_limit_sec is negative"
            )

        if self.memory_limit_mb < 0:
            raise AssignmentLimitsNegativeMemoryLimitError(
                "AssignmentLimits.memory_limit_mb is negative"
            )
