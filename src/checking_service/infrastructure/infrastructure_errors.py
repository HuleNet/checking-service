from checking_service.domain.errors.base_error import BaseError


class InfrastructureError(BaseError):
    code = "infrastructure_error"


class DatabaseError(InfrastructureError):
    code = "database_error"


class IntegrityViolationError(DatabaseError):
    code = "integrity_violation"


class TransactionError(DatabaseError):
    code = "transaction_error"


class RunnerError(InfrastructureError):
    code = "runner_error"


class RunnerTimeoutError(RunnerError):
    code = "runner_timeout"


class RunnerMemoryOutError(RunnerError):
    code = "runner_memory_out"


class RunnerExecutionError(RunnerError):
    code = "runner_execution_error"
