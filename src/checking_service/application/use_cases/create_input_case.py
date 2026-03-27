from uuid import uuid4

from checking_service.application.repositories.input_case import InputCaseRepository
from checking_service.application.mappers.input_case import InputCaseMapper
from checking_service.application.dto.input_case import CreateInputCaseDTO
from checking_service.domain.domain_errors import DomainError
from checking_service.application.application_errors import ValidationError


class CreateInputCaseUseCase:
    def __init__(self, repo: InputCaseRepository) -> None:
        self._repo = repo

    async def execute(self, dto: CreateInputCaseDTO) -> None:
        try:
            domain = InputCaseMapper.to_domain(dto=dto, id=uuid4())
        except DomainError as exc:
            raise ValidationError(
                "Invalid input data",
                context=exc.context,
            ) from exc

        # to do
        try:
            await self._repo.create(input_case=domain)
        except Exception:
            ...
