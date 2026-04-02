from uuid import UUID
from datetime import datetime

from sqlalchemy import (
    UUID as sqlalchemy_UUID,
    DateTime,
    Enum,
    Text,
    String,
    Float,
    ForeignKey,
    func,
)
from sqlalchemy.orm import mapped_column, Mapped, relationship

from checking_service.domain.enums.status import Status
from checking_service.infrastructure.db.models.base_orm import Base
from checking_service.infrastructure.db.models.input_case import InputCaseORM


class ExecutionResultORM(Base):
    __tablename__ = "execution_results"

    id: Mapped[UUID] = mapped_column(sqlalchemy_UUID(as_uuid=True), primary_key=True)
    submission_id: Mapped[UUID] = mapped_column(
        sqlalchemy_UUID(as_uuid=True), nullable=False, index=True
    )
    input_case_id: Mapped[UUID] = mapped_column(
        ForeignKey("input_cases.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[Status] = mapped_column(
        Enum(Status, native_enum=False), nullable=False
    )
    logs: Mapped[str] = mapped_column(Text(), nullable=False)
    execution_time_sec: Mapped[float] = mapped_column(Float(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    input_case: Mapped["InputCaseORM"] = relationship(
        back_populates="execution_results"
    )
