from uuid import UUID

from checking_service.domain.models import InputCase
from checking_service.domain.domain_errors import DomainError
from checking_service.application.ports.unit_of_work import UnitOfWork
from checking_service.application.mappers.input_case_mapper import InputCaseMapper
from checking_service.application.dto.input_case import UpdateInputCaseDTO
from checking_service.application.application_errors import (
    ValidationError,
    NotFoundError,
)


class UpdateInputCaseUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, id: UUID, dto: UpdateInputCaseDTO) -> None:
        async with self._uow:
            domain = await self._uow.input_cases.get_by_id(id=id)

            if domain is None:
                raise NotFoundError(f"Input Case with id={id} not found")

            try:
                domain = InputCaseMapper.apply_update(domain=domain, dto=dto)
            except DomainError as exc:
                raise ValidationError(
                    "Invalid update data",
                    context=exc.context,
                ) from exc

            await self._uow.input_cases.update(input_case=domain)
            await self._uow.commit()
