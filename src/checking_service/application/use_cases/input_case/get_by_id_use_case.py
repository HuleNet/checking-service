from uuid import UUID

from checking_service.application.ports.unit_of_work import UnitOfWork
from checking_service.application.mappers.input_case_mapper import InputCaseMapper
from checking_service.application.dto.input_case import InputCaseDTO
from checking_service.application.application_errors import (
    ExternalServiceError,
    NotFoundError,
)
from checking_service.infrastructure.infrastructure_errors import InfrastructureError


class GetByIdInputCaseUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, id: UUID) -> InputCaseDTO:
        try:
            async with self._uow:
                domain = await self._uow.input_cases.get_by_id(id=id)

                if domain is None:
                    raise NotFoundError(
                        "InputCase not found",
                        context={
                            "id": str(id),
                        },
                    )

                return InputCaseMapper.to_dto(domain=domain)

        except InfrastructureError as exc:
            raise ExternalServiceError(
                "Infrastructure service failure",
                context=exc.context,
            ) from exc
