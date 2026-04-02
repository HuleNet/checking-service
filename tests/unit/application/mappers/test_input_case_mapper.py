from uuid import uuid4

from pytest import raises

from checking_service.domain.enums.language import Language
from checking_service.domain.errors.domain_errors import (
    UnsupportedTypeError,
    InvariantViolationError,
)
from checking_service.application.mappers.input_case_mapper import InputCaseMapper
from tests.unit.domain.domain_models_factories import make_input_case
from tests.unit.application.dto_factories import InputCaseDTOFactory


def test_successful_to_domain_mapping() -> None:
    id = uuid4()
    dto = InputCaseDTOFactory.make_create_dto(language="lua")

    with raises(UnsupportedTypeError) as exc:
        InputCaseMapper.to_domain(dto=dto, id=id)

    assert exc.value.context == {
        "field": "language",
        "value": "lua",
        "allowed": Language.values(),
    }


def test_invalid_to_domain_mapping() -> None:
    id = uuid4()
    dto = InputCaseDTOFactory.make_create_dto()
    domain = InputCaseMapper.to_domain(dto=dto, id=id)

    assert domain.id == id
    assert domain.assignment_id == dto.assignment_id
    assert domain.language.value == dto.language
    assert domain.input_data == dto.input_data
    assert domain.expected_output == dto.expected_output


def test_successful_to_dto_mapping() -> None:
    domain = make_input_case()
    dto = InputCaseMapper.to_dto(domain=domain)

    assert domain.id == dto.id
    assert domain.assignment_id == dto.assignment_id
    assert domain.language.value == dto.language
    assert domain.input_data == dto.input_data
    assert domain.expected_output == dto.expected_output


def test_successful_update_mapping() -> None:
    updating_dto = InputCaseDTOFactory.make_update_dto()
    updated_domain = make_input_case()
    new_domain = InputCaseMapper.apply_update(domain=updated_domain, dto=updating_dto)

    assert new_domain.id == updated_domain.id
    assert new_domain.assignment_id == updated_domain.assignment_id
    assert new_domain.language == updated_domain.language
    assert new_domain.input_data == updating_dto.input_data
    assert new_domain.expected_output == updating_dto.expected_output


def test_invalid_update_mapping() -> None:
    updating_dto = InputCaseDTOFactory.make_update_dto(input_data="")
    updated_domain = make_input_case()

    with raises(InvariantViolationError) as exc:
        InputCaseMapper.apply_update(domain=updated_domain, dto=updating_dto)

    assert exc.value.context == {
        "model": "InputCase",
        "field": "input_data",
        "value": "",
    }
