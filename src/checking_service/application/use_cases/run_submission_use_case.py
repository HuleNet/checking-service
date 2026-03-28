from uuid import uuid4
from datetime import datetime, timezone

from checking_service.domain.models import ExecutionResult
from checking_service.domain.enums.status import Status
from checking_service.domain.domain_errors import DomainError
from checking_service.application.dto.submission import SubmissionDTO
from checking_service.application.ports.runner import Runner, RunResult
from checking_service.application.ports.unit_of_work import UnitOfWork
from checking_service.application.mappers.submission_mapper import SubmissionMapper
from checking_service.application.application_errors import (
    ValidationError,
    ExternalServiceError,
    NotFoundError,
)


class RunSubmissionUseCase:
    def __init__(
        self,
        uow: UnitOfWork,
        runner: Runner,
    ) -> None:
        self._uow = uow
        self._runner = runner

    async def execute(self, dto: SubmissionDTO) -> None:
        try:
            submission = SubmissionMapper.to_domain(dto=dto)
        except DomainError as exc:
            raise ValidationError("Invalid Submission", context=exc.context) from exc

        async with self._uow:
            input_cases = await self._uow.input_cases.get_by_assignment_and_language(
                assignment_id=submission.assignment_id,
                language=submission.language,
            )
            
            if not input_cases:
                raise NotFoundError(
                    f"Input Cases with assignment_id={dto.assignment_id}, language={dto.language} not found"
                )

            for case in input_cases:
                try:
                    run_result = await self._runner.run(
                        code=submission.code,
                        language=submission.language,
                        input_data=case.input_data,
                    )
                # TO-DO: Exception -> InfrastructureError; context=exc.context
                except Exception as exc:
                    raise ExternalServiceError(
                        "Runner failed",
                        context={
                            "details": str(exc),
                        },
                    ) from exc

                status = self._determine_status(
                    result=run_result,
                    expected=case.expected_output,
                )
                result = ExecutionResult(
                    id=uuid4(),
                    submission_id=submission.id,
                    input_case_id=case.id,
                    status=status,
                    logs=run_result.stderr or run_result.stdout or "",
                    execution_time_sec=run_result.execution_time_sec,
                    created_at=datetime.now(timezone.utc),
                )

                await self._uow.execution_results.create(execution_result=result)

            await self._uow.commit()

    # TO-DO: More status, correct check
    def _determine_status(self, result: RunResult, expected: str) -> Status:
        if result.exit_code != 0:
            return Status.error

        if result.stdout.strip() == expected.strip():
            return Status.passed

        return Status.failed
