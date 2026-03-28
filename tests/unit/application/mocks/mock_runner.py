from checking_service.domain.enums.language import Language
from checking_service.application.ports.runner import Runner, RunResult


class MockRunner(Runner):
    def __init__(self, results: dict[str, RunResult]) -> None:
        self._results = results

    async def run(self, code: str, language: Language, input_data: str) -> RunResult:
        return self._results[input_data]
