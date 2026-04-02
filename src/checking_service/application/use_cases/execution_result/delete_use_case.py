from uuid import UUID

from checking_service.application.ports.unit_of_work import UnitOfWork
from checking_service.application.application_errors import (
    ExternalServiceError,
    NotFoundError,
)
from checking_service.infrastructure.infrastructure_errors import InfrastructureError


class DeleteExecutionResultUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, id: UUID) -> None:
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

                await self._uow.execution_results.delete(id=id)
                await self._uow.commit()

        except InfrastructureError as exc:
            raise ExternalServiceError(
                "Infrastructure service failure",
                context=exc.context,
            ) from exc
