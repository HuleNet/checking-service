from uuid import UUID

from checking_service.domain.models import Submission
from checking_service.domain.enums.language import Language
from checking_service.domain.domain_errors import UnsupportedTypeError
from checking_service.application.dto.submission import CreateSubmissionDTO


class SubmissionMapper:
    @staticmethod
    def to_domain(dto: CreateSubmissionDTO, id: UUID) -> Submission:
        try:
            language = Language(dto.language)
        except ValueError:
            raise UnsupportedTypeError(
                "Unsupported language",
                field="language",
                value=dto.language,
                allowed=Language.values(),
            )
        return Submission(
            id=id,
            assignment_id=dto.assignment_id,
            language=language,
            code=dto.code,
        )
