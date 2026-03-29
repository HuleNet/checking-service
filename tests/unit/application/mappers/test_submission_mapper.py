from pytest import raises

from checking_service.domain.domain_errors import UnsupportedTypeError
from checking_service.domain.enums.language import Language
from checking_service.application.mappers.submission_mapper import SubmissionMapper
from tests.unit.application.dto_factories import SubmissionDTOFactory


def test_successful_mapping() -> None:
    dto = SubmissionDTOFactory.make_dto()
    domain = SubmissionMapper.to_domain(dto=dto)
    assert domain.id == dto.id
    assert domain.language.value == dto.language
    assert domain.code == dto.code
    assert domain.assignment_id == dto.assignment_id


def test_unsupported_language() -> None:
    dto = SubmissionDTOFactory.make_dto(language="lua")
    with raises(UnsupportedTypeError) as exc:
        SubmissionMapper.to_domain(dto=dto)
    assert exc.value.context == {
        "field": "language",
        "value": "lua",
        "allowed": Language.values(),
    }
