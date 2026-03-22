from pytest import raises

from tests.unit.domain.factories import make_assignment_limits
from checking_service.domain.errors.assignment_limits_errors import (
    AssignmentLimitsNegativeMemoryLimitError,
    AssignmentLimitsNegativeTimeLimitError,
)


def test_valid_assignment_limits() -> None:
    assignment_limits = make_assignment_limits()
    assert assignment_limits.time_limit_sec == 8.0
    assert assignment_limits.memory_limit_mb == 12


def test_assignment_limits_time_limit_is_negative() -> None:
    with raises(AssignmentLimitsNegativeTimeLimitError):
        make_assignment_limits(time_limit_sec=-10.5)


def test_assignment_limits_memory_limit_is_negative() -> None:
    with raises(AssignmentLimitsNegativeMemoryLimitError):
        make_assignment_limits(memory_limit_mb=-10)
