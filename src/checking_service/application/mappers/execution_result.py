from uuid import UUID
from datetime import datetime

from checking_service.domain.models import ExecutionResult
from checking_service.domain.enums.status import Status
from checking_service.domain.domain_errors import UnsupportedTypeError
from checking_service.application.dto.execution_result import CreateExecutionResultDTO


class ExecutionResultMapper:
    @staticmethod
    def to_domain(
        dto: CreateExecutionResultDTO, id: UUID, created_at: datetime
    ) -> ExecutionResult:
        try:
            status = Status(dto.status)
        except ValueError:
            raise UnsupportedTypeError(
                "Unsupported status",
                field="status",
                value=dto.status,
                allowed=Status.values(),
            )
        return ExecutionResult(
            id=id,
            submission_id=dto.submission_id,
            input_case_id=dto.input_case_id,
            status=status,
            logs=dto.logs,
            execution_time_sec=dto.execution_time_sec,
            created_at=created_at,
        )
