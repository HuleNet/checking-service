from uuid import UUID, uuid4

from checking_service.application.dto.input_case import CreateInputCaseDTO
from checking_service.application.dto.submission import CreateSubmissionDTO
from checking_service.application.dto.execution_result import CreateExecutionResultDTO


class InputCaseDTOFactory:
    @staticmethod
    def make_create_dto(
        *,
        assignment_id: UUID | None = None,
        language: str = "python",
        input_data: str = "input",
        expected_output: str = "output",
    ) -> CreateInputCaseDTO:
        return CreateInputCaseDTO(
            assignment_id=assignment_id or uuid4(),
            language=language,
            input_data=input_data,
            expected_output=expected_output,
        )


class SubmissionDTOFactory:
    @staticmethod
    def make_create_dto(
        *,
        assignment_id: UUID | None = None,
        language: str = "python",
        code: str = "code",
    ) -> CreateSubmissionDTO:
        return CreateSubmissionDTO(
            assignment_id=assignment_id or uuid4(),
            language=language,
            code=code,
        )


class ExecutionResultDTOFactory:
    @staticmethod
    def make_create_dto(
        *,
        submission_id: UUID | None = None,
        input_case_id: UUID | None = None,
        status: str = "passed",
        logs: str = "4",
        execution_time_sec: float = 0.4,
    ) -> CreateExecutionResultDTO:
        return CreateExecutionResultDTO(
            submission_id=submission_id or uuid4(),
            input_case_id=input_case_id or uuid4(),
            status=status,
            logs=logs,
            execution_time_sec=execution_time_sec,
        )
