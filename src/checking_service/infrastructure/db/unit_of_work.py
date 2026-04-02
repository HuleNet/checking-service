from typing import Self

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from checking_service.application.ports.unit_of_work import UnitOfWork
from checking_service.infrastructure.db.session import SessionLocal
from checking_service.infrastructure.db.repositories.input_case import (
    InputCaseSQLALchemyRepository,
)
from checking_service.infrastructure.db.repositories.execution_result import (
    ExecutionResultSQLAlchemyRepository,
)


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(
        self, session_maker: async_sessionmaker[AsyncSession] = SessionLocal
    ) -> None:
        self._session_maker = session_maker
        self.session: AsyncSession | None = None

    async def __aenter__(self) -> Self:
        if self.session is not None:
            raise RuntimeError("Session already started")

        self.session = self._session_maker()
        self.input_cases = InputCaseSQLALchemyRepository(session=self.session)
        self.execution_results = ExecutionResultSQLAlchemyRepository(
            session=self.session
        )
        return self

    async def __aexit__(self, exc_type: type[BaseException] | None, *args) -> None:
        try:
            if exc_type:
                await self.rollback()
            else:
                await self.commit()
        finally:
            if self.session:
                await self.session.close()
                self.session = None

    async def commit(self) -> None:
        if not self.session:
            raise RuntimeError("Session is not initialized")

        await self.session.commit()

    async def rollback(self) -> None:
        if not self.session:
            raise RuntimeError("Session is not initialized")

        await self.session.rollback()
