from checking_service.domain.models.execution_result import ExecutionResult
from checking_service.domain.enums.status import Status
from checking_service.infrastructure.db.models.execution_result import (
    ExecutionResultORM,
)


class ExecutionResultMapper:
    @staticmethod
    def to_orm(domain: ExecutionResult) -> ExecutionResultORM:
        return ExecutionResultORM(
            id=domain.id,
            submission_id=domain.submission_id,
            input_case_id=domain.input_case_id,
            status=domain.status,
            logs=domain.logs,
            execution_time_sec=domain.execution_time_sec,
            created_at=domain.created_at,
        )

    @staticmethod
    def to_domain(orm: ExecutionResultORM) -> ExecutionResult:
        return ExecutionResult(
            id=orm.id,
            submission_id=orm.submission_id,
            input_case_id=orm.input_case_id,
            status=ExecutionResultMapper._map_status_to_domain(status=orm.status),
            logs=orm.logs,
            execution_time_sec=orm.execution_time_sec,
            created_at=orm.created_at,
        )

    @staticmethod
    def _map_status_to_domain(status: Status | str) -> Status:
        if isinstance(status, Status):
            return status
        return Status(status)
