from uuid import UUID

from checking_service.application.ports.unit_of_work import UnitOfWork
from checking_service.application.mappers.execution_result_mapper import (
    ExecutionResultMapper,
)
from checking_service.application.dto.execution_result import ExecutionResultDTO
from checking_service.application.application_errors import ExternalServiceError
from checking_service.infrastructure.infrastructure_errors import InfrastructureError


class GetBySubmissionExecutionResultUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, submission_id: UUID) -> list[ExecutionResultDTO]:
        try:
            async with self._uow:
                domains = await self._uow.execution_results.get_by_submission(
                    submission_id=submission_id
                )

                return [
                    ExecutionResultMapper.to_dto(domain=domain) for domain in domains
                ]

        except InfrastructureError as exc:
            raise ExternalServiceError(
                "Infrastructure service failure", context=exc.context
            ) from exc
