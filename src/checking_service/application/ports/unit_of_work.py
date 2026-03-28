from typing import Protocol

from checking_service.application.ports.repositories.input_case_repo import (
    InputCaseRepository,
)
from checking_service.application.ports.repositories.execution_result_repo import (
    ExecutionResultRepository,
)


class UnitOfWork(Protocol):
    input_cases: InputCaseRepository
    execution_results: ExecutionResultRepository

    async def __aenter__(self): ...
    async def __aexit__(self, *args): ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
