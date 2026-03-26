from typing import Protocol
from uuid import UUID

from checking_service.domain.models.input_case import InputCase
from checking_service.domain.enums.language import Language


class InputCaseRepository(Protocol):
    async def create(self, input_case: InputCase) -> None: ...
    async def get_by_id(self, id: UUID) -> InputCase | None: ...
    async def get_by_assignment_id_and_language(
        self, assignment_id: UUID, language: Language
    ) -> list[InputCase]: ...
    async def delete(self, id: UUID) -> None: ...
