from uuid import uuid4

from pytest import raises, mark

from checking_service.domain.enums.language import Language
from checking_service.application.use_cases.input_case.update_use_case import (
    UpdateInputCaseUseCase,
)
from checking_service.application.application_errors import (
    NotFoundError,
    ValidationError,
)
from tests.unit.application.mocks.mock_uow import MockUnitOfWork
from tests.unit.application.dto_factories import InputCaseDTOFactory
from tests.unit.domain.domain_models_factories import make_input_case


@mark.asyncio
async def test_successful_mapping() -> None:
    uow = MockUnitOfWork()
    updated_domain = make_input_case()
    updating_dto = InputCaseDTOFactory.make_update_dto()
    await uow.input_cases.create(input_case=updated_domain)
    use_case = UpdateInputCaseUseCase(uow=uow)
    await use_case.execute(id=updated_domain.id, dto=updating_dto)
    new_domain = await uow.input_cases.get_by_id(id=updated_domain.id)
    assert new_domain is not None
    assert new_domain.id == updated_domain.id
    assert new_domain.assignment_id == updated_domain.assignment_id
    assert new_domain.language == updated_domain.language
    assert new_domain.input_data == updating_dto.input_data
    assert new_domain.expected_output == updating_dto.expected_output


@mark.asyncio
async def test_not_found_use_case() -> None:
    uow = MockUnitOfWork()
    updated_domain = make_input_case()
    updating_dto = InputCaseDTOFactory.make_update_dto()
    await uow.input_cases.create(input_case=updated_domain)
    use_case = UpdateInputCaseUseCase(uow=uow)
    with raises(NotFoundError):
        await use_case.execute(id=uuid4(), dto=updating_dto)


@mark.asyncio
async def test_validation_error_mapping() -> None:
    uow = MockUnitOfWork()
    updated_domain = make_input_case()
    updating_dto = InputCaseDTOFactory.make_update_dto(input_data="")
    await uow.input_cases.create(input_case=updated_domain)
    use_case = UpdateInputCaseUseCase(uow=uow)
    with raises(ValidationError) as exc:
        await use_case.execute(id=updated_domain.id, dto=updating_dto)
    assert exc.value.context == {
        "model": "InputCase",
        "field": "input_data",
        "value": "",
    }
