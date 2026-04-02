from pytest import raises

from checking_service.domain.models.execution_result import ExecutionResult
from checking_service.domain.enums.status import Status
from checking_service.domain.errors.domain_errors import InvariantViolationError
from tests.unit.domain.domain_models_factories import make_execution_result


def test_valid_execution_result() -> None:
    execution_result: ExecutionResult = make_execution_result()

    assert execution_result.status == Status.passed
    assert execution_result.logs == "stdout"
    assert execution_result.execution_time_sec == 4.0


def test_execution_result_execution_time_is_negative() -> None:
    with raises(InvariantViolationError) as exc:
        make_execution_result(execution_time_sec=-10.5)

    assert exc.value.context == {
        "model": "ExecutionResult",
        "field": "execution_time_sec",
        "value": -10.5,
    }
