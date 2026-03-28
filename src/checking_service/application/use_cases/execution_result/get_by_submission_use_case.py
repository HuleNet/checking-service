from uuid import UUID

from checking_service.application.ports.unit_of_work import UnitOfWork
from checking_service.application.mappers.execution_result_mapper import (
    ExecutionResultMapper,
)
from checking_service.application.dto.execution_result import ExecutionResultDTO


class GetBySubmissionExecutionResultUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, submission_id: UUID) -> list[ExecutionResultDTO]:
        async with self._uow:
            domains = await self._uow.execution_results.get_by_submission(
                submission_id=submission_id
            )

            return [ExecutionResultMapper.to_dto(domain=domain) for domain in domains]
