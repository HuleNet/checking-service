from pytest import raises

from factories import make_submission
from checking_service.domain.models.submission import Submission
from checking_service.domain.enums.language import Language
from checking_service.domain.domain_errors import InvariantViolationError


def test_valid_submission() -> None:
    submission: Submission = make_submission()
    assert submission.language == Language.python
    assert submission.code == "valid_code"


def test_submission_code_is_empty() -> None:
    with raises(InvariantViolationError) as error:
        make_submission(code="")
    assert error.value.context.get("model") == "Submission"
    assert error.value.context.get("field") == "code"
    assert error.value.context.get("value") == ""
