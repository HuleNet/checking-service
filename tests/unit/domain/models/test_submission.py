from pytest import raises

from checking_service.domain.models.submission import Submission
from checking_service.domain.enums.language import Language
from checking_service.domain.domain_errors import InvariantViolationError
from tests.unit.domain.domain_models_factories import make_submission


def test_valid_submission() -> None:
    submission: Submission = make_submission()
    assert submission.language == Language.python
    assert submission.code == "valid_code"


def test_submission_code_is_empty() -> None:
    with raises(InvariantViolationError) as exc:
        make_submission(code="")
    assert exc.value.context == {
        "model": "Submission",
        "field": "code",
        "value": "",
    }
