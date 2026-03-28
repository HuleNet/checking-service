from checking_service.domain.models import Submission
from checking_service.application.mappers.enum_mapper import map_str_to_language
from checking_service.application.dto.submission import SubmissionDTO


class SubmissionMapper:
    @staticmethod
    def to_domain(dto: SubmissionDTO) -> Submission:
        language = map_str_to_language(value=dto.language)
        return Submission(
            id=dto.id,
            assignment_id=dto.assignment_id,
            language=language,
            code=dto.code,
        )
