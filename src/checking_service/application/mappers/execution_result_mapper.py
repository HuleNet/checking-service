from checking_service.domain.models import ExecutionResult
from checking_service.application.dto.execution_result import ExecutionResultDTO


class ExecutionResultMapper:
    @staticmethod
    def to_dto(domain: ExecutionResult) -> ExecutionResultDTO:
        return ExecutionResultDTO(
            id=domain.id,
            submission_id=domain.submission_id,
            input_case_id=domain.input_case_id,
            status=domain.status.value,
            logs=domain.logs,
            execution_time_sec=domain.execution_time_sec,
            created_at=domain.created_at,
        )
