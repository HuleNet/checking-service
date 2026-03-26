from checking_service.application.repositories.execution_result import (
    ExecutionResultRepository,
)


class CreateExecutionResultUseCase:
    def __init__(self, repo: ExecutionResultRepository) -> None:
        self._repo = repo

    async def execute(self, dto) -> None: ...
