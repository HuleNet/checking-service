from pytest import raises

from tests.unit.domain.factories import make_submission
from checking_service.domain.enums.language import Language
from checking_service.domain.errors.submission_errors import SubmissionEmptyCodeError


def test_valid_submission() -> None:
    submission = make_submission()
    assert submission.language == Language.python
    assert submission.code == "valid_code"


def test_submission_code_is_empty() -> None:
    with raises(SubmissionEmptyCodeError):
        make_submission(code="")
