from uuid import UUID, uuid4

from checking_service.application.dto.input_case_dto import CreateInputCaseDTO


class InputCaseDTOFactory:
    @staticmethod
    def make_create_dto(
        *,
        assignment_id: UUID | None = None,
        language: str = "python",
        input_data: str = "input",
        expected_output: str = "output",
    ) -> CreateInputCaseDTO:
        return CreateInputCaseDTO(
            assignment_id=assignment_id or uuid4(),
            language=language,
            input_data=input_data,
            expected_output=expected_output,
        )
