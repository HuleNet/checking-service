from uuid import uuid4
from datetime import datetime, timezone

from pytest import raises

from checking_service.domain.models import ExecutionResult
from checking_service.domain.enums.status import Status
from checking_service.domain.domain_errors import UnsupportedTypeError
from checking_service.application.mappers.execution_result import ExecutionResultMapper
from checking_service.application.dto.execution_result import CreateExecutionResultDTO
from tests.unit.application.factories import ExecutionResultDTOFactory


def test_successful_mapping() -> None:
    dto: CreateExecutionResultDTO = ExecutionResultDTOFactory.make_create_dto()
    domain: ExecutionResult = ExecutionResultMapper.to_domain(
        dto=dto,
        id=uuid4(),
        created_at=datetime.now(timezone.utc),
    )
    assert domain.status == Status.passed


def test_unsupported_status_mapping() -> None:
    dto: CreateExecutionResultDTO = ExecutionResultDTOFactory.make_create_dto(
        status="unknown"
    )
    with raises(UnsupportedTypeError) as exc:
        ExecutionResultMapper.to_domain(
            dto=dto,
            id=uuid4(),
            created_at=datetime.now(timezone.utc),
        )
    assert exc.value.context == {
        "field": "status",
        "value": "unknown",
        "allowed": Status.values(),
    }
