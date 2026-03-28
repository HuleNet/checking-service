from uuid import UUID

from checking_service.domain.models import InputCase, ExecutionResult
from checking_service.domain.enums.language import Language
from checking_service.application.ports.repositories.input_case_repo import (
    InputCaseRepository,
)
from checking_service.application.ports.repositories.execution_result_repo import (
    ExecutionResultRepository,
)


class MockInputCaseRepository(InputCaseRepository):
    def __init__(self) -> None:
        self._storage: dict[UUID, InputCase] = {}

    async def create(self, input_case: InputCase) -> None:
        self._storage[input_case.id] = input_case

    async def get_by_id(self, id: UUID) -> InputCase | None:
        return self._storage.get(id)

    async def get_by_assignment_and_language(
        self, assignment_id: UUID, language: Language
    ) -> list[InputCase]:
        return [
            input_case
            for input_case in self._storage.values()
            if input_case.assignment_id == assignment_id
            and input_case.language == language
        ]

    async def update(self, input_case: InputCase) -> None:
        if input_case.id not in self._storage:
            return
        self._storage[input_case.id] = input_case

    async def delete(self, id: UUID) -> None:
        if id not in self._storage:
            return
        self._storage.pop(id, None)


class MockExecutionResultRepository(ExecutionResultRepository):
    def __init__(self) -> None:
        self._storage: dict[UUID, ExecutionResult] = {}

    async def create(self, execution_result: ExecutionResult) -> None:
        self._storage[execution_result.id] = execution_result

    async def get_by_id(self, id: UUID) -> ExecutionResult | None:
        return self._storage.get(id)

    async def get_by_submission(self, submission_id: UUID) -> list[ExecutionResult]:
        return [
            execution_result
            for execution_result in self._storage.values()
            if execution_result.submission_id == submission_id
        ]

    async def delete(self, id: UUID) -> None:
        if id not in self._storage:
            return
        self._storage.pop(id, None)
