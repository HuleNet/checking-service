from pytest import raises

from checking_service.application.mappers.execution_result_mapper import (
    ExecutionResultMapper,
)
from tests.unit.domain.domain_models_factories import make_execution_result


def test_successful_mapping() -> None:
    domain = make_execution_result()
    dto = ExecutionResultMapper.to_dto(domain=domain)
    assert dto.id == domain.id
    assert dto.status == domain.status
    assert dto.logs == domain.logs
    assert dto.created_at == domain.created_at
