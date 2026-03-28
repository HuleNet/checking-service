from uuid import UUID

from checking_service.domain.models import InputCase
from checking_service.application.mappers.enum_mapper import map_str_to_language
from checking_service.application.dto.input_case import (
    CreateInputCaseDTO,
    UpdateInputCaseDTO,
    InputCaseDTO,
)


class InputCaseMapper:
    @staticmethod
    def to_domain(dto: CreateInputCaseDTO, id: UUID) -> InputCase:
        language = map_str_to_language(value=dto.language)
        return InputCase(
            id=id,
            assignment_id=dto.assignment_id,
            language=language,
            input_data=dto.input_data,
            expected_output=dto.expected_output,
        )

    @staticmethod
    def to_dto(domain: InputCase) -> InputCaseDTO:
        return InputCaseDTO(
            id=domain.id,
            assignment_id=domain.assignment_id,
            language=domain.language.value,
            input_data=domain.input_data,
            expected_output=domain.expected_output,
        )

    @staticmethod
    def apply_update(domain: InputCase, dto: UpdateInputCaseDTO) -> InputCase:
        return InputCase(
            id=domain.id,
            assignment_id=domain.assignment_id,
            language=domain.language,
            input_data=dto.input_data,
            expected_output=dto.expected_output,
        )
