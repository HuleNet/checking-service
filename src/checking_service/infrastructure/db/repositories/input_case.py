from uuid import UUID

from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from checking_service.domain.models import InputCase
from checking_service.domain.enums.language import Language
from checking_service.application.ports.repositories.input_case_repo import (
    InputCaseRepository,
)
from checking_service.infrastructure.db.models.input_case import InputCaseORM
from checking_service.infrastructure.db.mappers.input_case_mapper import InputCaseMapper
from checking_service.infrastructure.infrastructure_errors import (
    DatabaseError,
    IntegrityViolationError,
)


class InputCaseSQLALchemyRepository(InputCaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.model = InputCaseORM

    async def create(self, input_case: InputCase) -> None:
        orm = InputCaseMapper.to_orm(domain=input_case)
        query = insert(self.model).values(
            id=orm.id,
            assignment_id=orm.assignment_id,
            language=orm.language,
            input_data=orm.input_data,
            expected_output=orm.expected_output,
        )

        try:
            await self.session.execute(query)

        except IntegrityError as exc:
            raise IntegrityViolationError(
                "Constraint violation",
                context={"details": str(exc)},
            ) from exc

        except SQLAlchemyError as exc:
            raise DatabaseError(
                "Failed to create InputCase",
                context={"details": str(exc)},
            ) from exc

    async def get_by_id(self, id: UUID) -> InputCase | None:
        query = select(self.model).where(self.model.id == id)

        try:
            result = await self.session.execute(query)

        except SQLAlchemyError as exc:
            raise DatabaseError(
                "Failed to fetch InputCase", context={"details": str(exc)}
            ) from exc

        orm = result.scalar_one_or_none()

        if orm is None:
            return None

        return InputCaseMapper.to_domain(orm=orm)

    async def get_by_assignment_and_language(
        self, assignment_id: UUID, language: Language
    ) -> list[InputCase]:
        query = select(self.model).where(
            self.model.assignment_id == assignment_id,
            self.model.language == language,
        )

        try:
            result = await self.session.execute(query)

        except SQLAlchemyError as exc:
            raise DatabaseError(
                "Failed to fetch InputCases", context={"details": str(exc)}
            ) from exc

        return [InputCaseMapper.to_domain(orm=orm) for orm in result.scalars().all()]

    async def update(self, input_case: InputCase) -> None:
        query = (
            update(self.model)
            .where(self.model.id == input_case.id)
            .values(
                input_data=input_case.input_data,
                expected_output=input_case.expected_output,
            )
        )

        try:
            await self.session.execute(query)

        except IntegrityError as exc:
            raise IntegrityViolationError(
                "Constraint violation", context={"details": str(exc)}
            ) from exc

        except SQLAlchemyError as exc:
            raise DatabaseError(
                "Failed to update InputCase", context={"details": str(exc)}
            ) from exc

    async def delete(self, id: UUID) -> None:
        query = delete(self.model).where(self.model.id == id)

        try:
            await self.session.execute(query)

        except SQLAlchemyError as exc:
            raise DatabaseError(
                "Failed to delete InputCase", context={"details": str(exc)}
            ) from exc
