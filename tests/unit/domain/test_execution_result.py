from pytest import raises

from tests.unit.domain.factories import make_execution_result
from checking_service.domain.enums.status import Status
from checking_service.domain.models.execution_result import (
    ExecutionResultNegativeExecutionMemoryError,
    ExecutionResultNegativeExecutionTimeError,
)


def test_valid_execution_result() -> None:
    execution_result = make_execution_result()
    assert execution_result.status == Status.passed
    assert execution_result.logs == "stdout"
    assert execution_result.execution_time_sec == 4.0
    assert execution_result.execution_memory_mb == 8


def test_execution_result_execution_time_is_negative() -> None:
    with raises(ExecutionResultNegativeExecutionTimeError):
        make_execution_result(execution_time_sec=-10.5)


def test_execution_result_execution_memory_is_negative() -> None:
    with raises(ExecutionResultNegativeExecutionMemoryError):
        make_execution_result(execution_memory_mb=-10)
