from uuid import UUID

from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from checking_service.domain.models import ExecutionResult
from checking_service.domain.enums.status import Status
from checking_service.application.ports.repositories.execution_result_repo import (
    ExecutionResultRepository,
)
from checking_service.infrastructure.db.models.execution_result import (
    ExecutionResultORM,
)
from checking_service.infrastructure.db.mappers.execution_result_mapper import (
    ExecutionResultMapper,
)
from checking_service.infrastructure.infrastructure_errors import (
    DatabaseError,
    IntegrityViolationError,
)


class ExecutionResultSQLAlchemyRepository(ExecutionResultRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.model = ExecutionResultORM

    async def create(self, execution_result: ExecutionResult) -> None:
        orm = ExecutionResultMapper.to_orm(domain=execution_result)
        query = insert(self.model).values(
            id=orm.id,
            submission_id=orm.submission_id,
            input_case_id=orm.input_case_id,
            status=orm.status,
            logs=orm.logs,
            execution_time_sec=orm.execution_time_sec,
            created_at=orm.created_at,
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
                "Failed to create ExecutionResult",
                context={"details": str(exc)},
            ) from exc

    async def get_by_id(self, id: UUID) -> ExecutionResult | None:
        query = select(self.model).where(self.model.id == id)

        try:
            result = await self.session.execute(query)

        except SQLAlchemyError as exc:
            raise DatabaseError(
                "Failed to fetch ExecutionResult", context={"details": str(exc)}
            ) from exc

        orm = result.scalar_one_or_none()

        if orm is None:
            return None

        return ExecutionResultMapper.to_domain(orm=orm)

    async def get_by_submission(self, submission_id: UUID) -> list[ExecutionResult]:
        query = select(self.model).where(self.model.submission_id == submission_id)

        try:
            result = await self.session.execute(query)

        except SQLAlchemyError as exc:
            raise DatabaseError(
                "Failed to fetch ExecutionResults", context={"details": str(exc)}
            ) from exc

        return [
            ExecutionResultMapper.to_domain(orm=orm) for orm in result.scalars().all()
        ]

    async def delete(self, id: UUID) -> None:
        query = delete(self.model).where(self.model.id == id)

        try:
            await self.session.execute(query)

        except SQLAlchemyError as exc:
            raise DatabaseError(
                "Failed to delete ExecutionResult", context={"details": str(exc)}
            )
