from pytest import raises

from factories import make_execution_result
from checking_service.domain.models.execution_result import ExecutionResult
from checking_service.domain.enums.status import Status
from checking_service.domain.domain_errors import InvariantViolationError


def test_valid_execution_result() -> None:
    execution_result: ExecutionResult = make_execution_result()
    assert execution_result.status == Status.passed
    assert execution_result.logs == "stdout"
    assert execution_result.execution_time_sec == 4.0


def test_execution_result_execution_time_is_negative() -> None:
    with raises(InvariantViolationError) as error:
        make_execution_result(execution_time_sec=-10.5)
    assert error.value.context.get("model") == "ExecutionResult"
    assert error.value.context.get("field") == "execution_time_sec"
    assert error.value.context.get("value") == -10.5
