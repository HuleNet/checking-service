from uuid import UUID

from sqlalchemy import UUID as sqlalchemy_UUID, Enum, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from checking_service.domain.enums.language import Language
from checking_service.infrastructure.db.models.base_orm import Base
from checking_service.infrastructure.db.models.execution_result import (
    ExecutionResultORM,
)


class InputCaseORM(Base):
    __tablename__ = "input_cases"

    id: Mapped[UUID] = mapped_column(sqlalchemy_UUID(as_uuid=True), primary_key=True)
    assignment_id: Mapped[UUID] = mapped_column(
        sqlalchemy_UUID(as_uuid=True), nullable=False, index=True
    )
    language: Mapped[Language] = mapped_column(
        Enum(Language, native_enum=False), nullable=False
    )
    input_data: Mapped[str] = mapped_column(String(2048), nullable=False)
    expected_output: Mapped[str] = mapped_column(String(2048), nullable=False)

    execution_results: Mapped[list["ExecutionResultORM"]] = relationship(
        back_populates="input_case", cascade="all, delete-orphan"
    )
