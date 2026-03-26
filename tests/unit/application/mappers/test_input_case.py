from uuid import uuid4

from pytest import raises

from checking_service.domain.enums.language import Language
from checking_service.domain.domain_errors import UnsupportedTypeError
from checking_service.application.mappers.input_case import InputCaseMapper
from checking_service.application.dto.input_case_dto import CreateInputCaseDTO
from tests.unit.application.factories import InputCaseDTOFactory


def test_successful_mapping() -> None:
    dto: CreateInputCaseDTO = InputCaseDTOFactory.make_create_dto()
    domain = InputCaseMapper.to_domain(dto=dto, id=uuid4())
    assert domain.language == Language.python


def test_unsupported_language_mapping() -> None:
    dto: CreateInputCaseDTO = InputCaseDTOFactory.make_create_dto(language="lua")
    with raises(UnsupportedTypeError) as exc:
        InputCaseMapper.to_domain(dto=dto, id=uuid4())
    assert exc.value.context == {
        "field": "language",
        "value": "lua",
        "allowed": Language.values(),
    }
