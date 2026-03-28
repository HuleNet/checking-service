from uuid import uuid4

from checking_service.domain.domain_errors import DomainError
from checking_service.application.ports.unit_of_work import UnitOfWork
from checking_service.application.mappers.input_case_mapper import InputCaseMapper
from checking_service.application.dto.input_case import CreateInputCaseDTO
from checking_service.application.application_errors import ValidationError


class CreateInputCaseUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, dto: CreateInputCaseDTO) -> None:
        try:
            domain = InputCaseMapper.to_domain(
                dto=dto,
                id=uuid4(),
            )
        except DomainError as exc:
            raise ValidationError(
                "Invalid Input Case",
                context=exc.context,
            ) from exc

        async with self._uow:
            await self._uow.input_cases.create(domain)
            await self._uow.commit()
