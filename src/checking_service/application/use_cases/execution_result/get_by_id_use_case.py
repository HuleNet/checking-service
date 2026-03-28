from uuid import UUID

from checking_service.application.ports.unit_of_work import UnitOfWork
from checking_service.application.mappers.execution_result_mapper import (
    ExecutionResultMapper,
)
from checking_service.application.dto.execution_result import ExecutionResultDTO
from checking_service.application.application_errors import NotFoundError


class GetByIdExecutionResultUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, id: UUID) -> ExecutionResultDTO:
        async with self._uow:
            domain = await self._uow.execution_results.get_by_id(id=id)

            if domain is None:
                raise NotFoundError(f"Execution Result with id={id} not found")

            return ExecutionResultMapper.to_dto(domain=domain)
