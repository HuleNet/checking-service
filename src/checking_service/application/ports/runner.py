from typing import Protocol
from dataclasses import dataclass

from checking_service.domain.enums.language import Language


@dataclass(frozen=True)
class RunResult:
    stdout: str
    stderr: str
    exit_code: int
    execution_time_sec: float


class Runner(Protocol):
    async def run(
        self, code: str, language: Language, input_data: str
    ) -> RunResult: ...
