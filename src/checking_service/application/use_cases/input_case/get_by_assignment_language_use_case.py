from uuid import UUID

from checking_service.domain.errors.domain_errors import DomainError
from checking_service.application.ports.unit_of_work import UnitOfWork
from checking_service.application.mappers.enum_mapper import map_str_to_language
from checking_service.application.mappers.input_case_mapper import InputCaseMapper
from checking_service.application.dto.input_case import GetInputCaseDTO, InputCaseDTO
from checking_service.application.application_errors import (
    ExternalServiceError,
    ValidationError,
)
from checking_service.infrastructure.infrastructure_errors import InfrastructureError


class GetByAssignmentAndLanguageUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, dto: GetInputCaseDTO) -> list[InputCaseDTO]:
        try:
            enum_language = map_str_to_language(dto.language)

        except DomainError as exc:
            raise ValidationError(
                "Invalid input data",
                context={
                    "code": exc.code,
                    "details": exc.context,
                },
            ) from exc

        try:
            async with self._uow:
                domains = await self._uow.input_cases.get_by_assignment_and_language(
                    assignment_id=dto.assignment_id,
                    language=enum_language,
                )
                return [InputCaseMapper.to_dto(domain=domain) for domain in domains]

        except InfrastructureError as exc:
            raise ExternalServiceError(
                "Infrastructure service failure",
                context=exc.context,
            ) from exc
