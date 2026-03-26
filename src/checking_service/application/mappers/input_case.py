from uuid import UUID

from checking_service.domain.models import InputCase
from checking_service.domain.enums.language import Language
from checking_service.application.dto.input_case_dto import CreateInputCaseDTO
from checking_service.domain.domain_errors import UnsupportedTypeError


class InputCaseMapper:
    @staticmethod
    def to_domain(dto: CreateInputCaseDTO, id: UUID) -> InputCase:
        try:
            language = Language(dto.language)
        except ValueError:
            raise UnsupportedTypeError(
                "Unsupported language",
                field="language",
                value=dto.language,
                allowed=Language.values(),
            )
        return InputCase(
            id=id,
            assignment_id=dto.assignment_id,
            language=language,
            input_data=dto.input_data,
            expected_output=dto.expected_output,
        )
