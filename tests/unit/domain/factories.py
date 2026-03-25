from uuid import UUID, uuid4

from checking_service.domain.enums.language import Language
from checking_service.domain.enums.status import Status
from checking_service.domain.models import (
    Submission,
    InputCase,
    ExecutionResult,
)


def make_submission(
    *,
    id: UUID | None = None,
    assignment_id: UUID | None = None,
    language: Language = Language.python,
    code: str = "valid_code",
) -> Submission:
    return Submission(
        id=id or uuid4(),
        assignment_id=assignment_id or uuid4(),
        language=language,
        code=code,
    )


def make_input_case(
    *,
    id: UUID | None = None,
    assignment_id: UUID | None = None,
    language: Language = Language.python,
    input_data: str = "input",
    expected_output: str = "output",
) -> InputCase:
    return InputCase(
        id=id or uuid4(),
        assignment_id=assignment_id or uuid4(),
        language=language,
        input_data=input_data,
        expected_output=expected_output,
    )


def make_execution_result(
    *,
    id: UUID | None = None,
    submission_id: UUID | None = None,
    input_case_id: UUID | None = None,
    status: Status = Status.passed,
    logs: str = "stdout",
    execution_time_sec: float = 4.0,
) -> ExecutionResult:
    return ExecutionResult(
        id=id or uuid4(),
        submission_id=submission_id or uuid4(),
        input_case_id=input_case_id or uuid4(),
        status=status,
        logs=logs,
        execution_time_sec=execution_time_sec,
    )
