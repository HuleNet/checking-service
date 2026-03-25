from dataclasses import dataclass
from uuid import UUID

from checking_service.domain.enums.language import Language
from checking_service.domain.domain_errors import InvariantViolationError


@dataclass(frozen=True)
class Submission:
    id: UUID
    assignment_id: UUID
    language: Language
    code: str

    def __post_init__(self) -> None:
        self._check_invariants()

    def _check_invariants(self) -> None:
        if not self.code:
            raise InvariantViolationError(
                "Code is empty",
                model="Submission",
                field="code",
                value=self.code,
            )
