from typing import Protocol
from uuid import UUID

from checking_service.domain.models.execution_result import ExecutionResult


class ExecutionResultRepository(Protocol):
    async def create(self, execution_result: ExecutionResult) -> None: ...
    async def get_by_id(self, id: UUID) -> ExecutionResult | None: ...
    async def get_by_submission_id(
        self, submission_id: UUID
    ) -> list[ExecutionResult]: ...
