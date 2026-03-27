from uuid import uuid4

from pytest import raises

from checking_service.domain.models import Submission
from checking_service.domain.enums.language import Language
from checking_service.domain.domain_errors import UnsupportedTypeError
from checking_service.application.mappers.submission import SubmissionMapper
from checking_service.application.dto.submission import CreateSubmissionDTO
from tests.unit.application.factories import SubmissionDTOFactory


def test_successful_mapping() -> None:
    dto: CreateSubmissionDTO = SubmissionDTOFactory.make_create_dto()
    domain: Submission = SubmissionMapper.to_domain(dto=dto, id=uuid4())
    assert domain.language == Language.python


def test_unsupported_language_mapping() -> None:
    dto: CreateSubmissionDTO = SubmissionDTOFactory.make_create_dto(language="lua")
    with raises(UnsupportedTypeError) as exc:
        SubmissionMapper.to_domain(dto=dto, id=uuid4())
    assert exc.value.context == {
        "field": "language",
        "value": "lua",
        "allowed": Language.values(),
    }
