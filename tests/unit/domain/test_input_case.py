from pytest import raises

from factories import make_input_case
from checking_service.domain.models.input_case import InputCase
from checking_service.domain.enums.language import Language
from checking_service.domain.domain_errors import InvariantViolationError


def test_valid_input_case() -> None:
    input_case: InputCase = make_input_case()
    assert input_case.language == Language.python
    assert input_case.input_data == "input"
    assert input_case.expected_output == "output"


def test_input_case_input_data_is_empty() -> None:
    with raises(InvariantViolationError) as error:
        make_input_case(input_data="")
    assert error.value.context.get("model") == "InputCase"
    assert error.value.context.get("field") == "input_data"
    assert error.value.context.get("value") == ""


def test_input_case_expected_output_is_empty() -> None:
    with raises(InvariantViolationError) as error:
        make_input_case(expected_output="")
    assert error.value.context.get("model") == "InputCase"
    assert error.value.context.get("field") == "expected_output"
    assert error.value.context.get("value") == ""
