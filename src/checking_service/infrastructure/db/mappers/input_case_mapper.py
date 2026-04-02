from checking_service.domain.models import InputCase
from checking_service.domain.enums.language import Language
from checking_service.infrastructure.db.models.input_case import InputCaseORM


class InputCaseMapper:
    @staticmethod
    def to_orm(domain: InputCase) -> InputCaseORM:
        return InputCaseORM(
            id=domain.id,
            assignment_id=domain.assignment_id,
            language=domain.language,
            input_data=domain.input_data,
            expected_output=domain.expected_output,
        )

    @staticmethod
    def to_domain(orm: InputCaseORM) -> InputCase:
        return InputCase(
            id=orm.id,
            assignment_id=orm.assignment_id,
            language=InputCaseMapper._map_language_to_domain(language=orm.language),
            input_data=orm.input_data,
            expected_output=orm.expected_output,
        )

    @staticmethod
    def _map_language_to_domain(language: Language | str) -> Language:
        if isinstance(language, Language):
            return language
        return Language(language)
