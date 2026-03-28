from pytest import raises, mark

from checking_service.application.use_cases.run_submission_use_case import (
    RunSubmissionUseCase,
)
from checking_service.application.ports.runner import RunResult
from tests.unit.domain.domain_models_factories import make_input_case
from tests.unit.application.mocks.mock_uow import MockUnitOfWork
from tests.unit.application.mocks.mock_runner import MockRunner
from tests.unit.application.dto_factories import SubmissionDTOFactory


@mark.asyncio
async def test_successful_use_case() -> None:
    submission = SubmissionDTOFactory.make_dto()

    uow = MockUnitOfWork()
    
    await uow.input_cases.create(
        input_case=make_input_case(
            assignment_id=submission.assignment_id,
            input_data="2 2",
            expected_output="4",
        )
    )
    await uow.input_cases.create(
        input_case=make_input_case(
            assignment_id=submission.assignment_id,
            input_data="3 1",
            expected_output="4",
        )
    )
    await uow.input_cases.create(
        input_case=make_input_case(
            assignment_id=submission.assignment_id,
            input_data="4 4",
            expected_output="8",
        )
    )

    runner = MockRunner(
        {
            "2 2": RunResult(
                stdout="4", stderr="", exit_code=0, execution_time_sec=0.5
            ),
            "3 1": RunResult(
                stdout="5", stderr="", exit_code=0, execution_time_sec=0.5
            ),
            "4 4": RunResult(
                stdout="", stderr="error", exit_code=-1, execution_time_sec=0.5
            ),
        }
    )

    use_case = RunSubmissionUseCase(uow=uow, runner=runner)

    await use_case.execute(dto=submission)
    
    result = await uow.execution_results.get_by_submission(submission_id=submission.id)
    statuses = [r.status for r in result]
    
    assert len(result) == 3
    assert statuses == ["passed", "failed", "error"]

