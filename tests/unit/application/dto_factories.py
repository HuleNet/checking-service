from uuid import UUID, uuid4
from datetime import datetime, timezone

from checking_service.application.dto.submission import SubmissionDTO
from checking_service.application.dto.input_case import (
    CreateInputCaseDTO,
    UpdateInputCaseDTO,
    GetInputCaseDTO,
    InputCaseDTO,
)
from checking_service.application.dto.execution_result import ExecutionResultDTO


class SubmissionDTOFactory:
    @staticmethod
    def make_dto(
        *,
        id: UUID | None = None,
        assignment_id: UUID | None = None,
        language: str = "python",
        code: str = "code",
    ) -> SubmissionDTO:
        return SubmissionDTO(
            id=id or uuid4(),
            assignment_id=assignment_id or uuid4(),
            language=language,
            code=code,
        )


class InputCaseDTOFactory:
    @staticmethod
    def make_create_dto(
        *,
        assignment_id: UUID | None = None,
        language: str = "python",
        input_data: str = "input",
        expected_output: str = "expected",
    ) -> CreateInputCaseDTO:
        return CreateInputCaseDTO(
            assignment_id=assignment_id or uuid4(),
            language=language,
            input_data=input_data,
            expected_output=expected_output,
        )

    @staticmethod
    def make_update_dto(
        *,
        input_data: str = "updated_input",
        expected_output: str = "updated_output",
    ) -> UpdateInputCaseDTO:
        return UpdateInputCaseDTO(
            input_data=input_data,
            expected_output=expected_output,
        )

    @staticmethod
    def make_get_dto(
        *,
        assignment_id: UUID | None = None,
        language: str = "python",
    ) -> GetInputCaseDTO:
        return GetInputCaseDTO(
            assignment_id=assignment_id or uuid4(),
            language=language,
        )

    @staticmethod
    def make_dto(
        *,
        id: UUID | None = None,
        assignment_id: UUID | None = None,
        language: str = "python",
        input_data: str = "input",
        expected_output: str = "expected",
    ) -> InputCaseDTO:
        return InputCaseDTO(
            id=id or uuid4(),
            assignment_id=assignment_id or uuid4(),
            language=language,
            input_data=input_data,
            expected_output=expected_output,
        )


class ExecutionResultDTOFactory:
    @staticmethod
    def make_dto(
        *,
        id: UUID | None = None,
        submission_id: UUID | None = None,
        input_case_id: UUID | None = None,
        status: str = "passed",
        logs: str = "4",
        execution_time_sec: float = 0.5,
        created_at: datetime | None = None,
    ) -> ExecutionResultDTO:
        return ExecutionResultDTO(
            id=id or uuid4(),
            submission_id=submission_id or uuid4(),
            input_case_id=input_case_id or uuid4(),
            status=status,
            logs=logs,
            execution_time_sec=execution_time_sec,
            created_at=created_at or datetime.now(timezone.utc),
        )
