from typing import Self

from checking_service.application.ports.unit_of_work import UnitOfWork
from tests.unit.application.mocks.mock_repos import (
    MockExecutionResultRepository,
    MockInputCaseRepository,
)


class MockUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self.input_cases = MockInputCaseRepository()
        self.execution_results = MockExecutionResultRepository()
        self._committed = False

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        *args,
    ) -> None:
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self) -> None:
        self._committed = True

    async def rollback(self) -> None:
        self._committed = False
