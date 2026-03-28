from typing import Protocol, Self
from types import TracebackType

from checking_service.application.ports.repositories.input_case_repo import (
    InputCaseRepository,
)
from checking_service.application.ports.repositories.execution_result_repo import (
    ExecutionResultRepository,
)


class UnitOfWork(Protocol):
    input_cases: InputCaseRepository
    execution_results: ExecutionResultRepository

    async def __aenter__(self) -> Self: ...
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> bool | None: ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
