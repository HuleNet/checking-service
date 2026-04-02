from uuid import UUID

from checking_service.application.ports.unit_of_work import UnitOfWork
from checking_service.application.mappers.execution_result_mapper import (
    ExecutionResultMapper,
)
from checking_service.application.dto.execution_result import ExecutionResultDTO
from checking_service.application.application_errors import (
    ExternalServiceError,
    NotFoundError,
)
from checking_service.infrastructure.infrastructure_errors import InfrastructureError


class GetByIdExecutionResultUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, id: UUID) -> ExecutionResultDTO:
        try:
            async with self._uow:
                domain = await self._uow.execution_results.get_by_id(id=id)

                if domain is None:
                    raise NotFoundError(
                        "ExecutionResult not found",
                        context={
                            "id": str(id),
                        },
                    )

                return ExecutionResultMapper.to_dto(domain=domain)

        except InfrastructureError as exc:
            raise ExternalServiceError(
                "Infrastructure service failure",
                context=exc.context,
            ) from exc
