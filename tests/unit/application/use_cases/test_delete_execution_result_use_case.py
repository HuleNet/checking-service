from uuid import uuid4

from pytest import raises, mark

from checking_service.application.use_cases.execution_result.delete_use_case import (
    DeleteExecutionResultUseCase,
)
from checking_service.application.application_errors import NotFoundError
from tests.unit.application.mocks.mock_uow import MockUnitOfWork
from tests.unit.domain.domain_models_factories import make_execution_result


@mark.asyncio
async def test_successful_use_case() -> None:
    uow = MockUnitOfWork()
    domain = make_execution_result()
    await uow.execution_results.create(execution_result=domain)
    use_case = DeleteExecutionResultUseCase(uow=uow)
    await use_case.execute(id=domain.id)
    execution_result = await uow.execution_results.get_by_id(id=domain.id)
    assert execution_result is None


@mark.asyncio
async def test_not_found_use_case() -> None:
    uow = MockUnitOfWork()
    id = uuid4()
    use_case = DeleteExecutionResultUseCase(uow=uow)
    with raises(NotFoundError):
        await use_case.execute(id=id)
