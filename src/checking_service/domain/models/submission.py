from dataclasses import dataclass
from uuid import UUID

from checking_service.domain.enums.language import Language
from checking_service.domain.errors.submission_errors import (
    SubmissionEmptyCodeError,
)


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
            raise SubmissionEmptyCodeError("Submission.code is empty")
