from uuid import UUID

from checking_service.application.ports.unit_of_work import UnitOfWork
from checking_service.application.application_errors import NotFoundError


class DeleteExecutionResultUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, id: UUID) -> None:
        async with self._uow:
            domain = await self._uow.execution_results.get_by_id(id=id)

            if domain is None:
                raise NotFoundError(f"Execution Result with id={id} not found")

            await self._uow.execution_results.delete(id=id)
            await self._uow.commit()
