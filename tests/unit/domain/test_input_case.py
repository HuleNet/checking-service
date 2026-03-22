from pytest import raises

from tests.unit.domain.factories import make_input_case
from checking_service.domain.enums.language import Language
from checking_service.domain.errors.input_case_errors import (
    InputCaseEmptyInputDataAndExpectedOutputError,
)


def test_valid_input_case() -> None:
    input_case = make_input_case()
    assert input_case.language == Language.python
    assert input_case.input_data == "input"
    assert input_case.expected_output == "output"


def test_input_case_input_data_and_expected_output_are_empty() -> None:
    with raises(InputCaseEmptyInputDataAndExpectedOutputError):
        make_input_case(input_data="", expected_output="")
