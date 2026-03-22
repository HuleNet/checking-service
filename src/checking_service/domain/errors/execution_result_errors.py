from checking_service.domain.errors.domain_errors import ExecutionResultError


class ExecutionResultNegativeExecutionTimeError(ExecutionResultError):
    pass


class ExecutionResultNegativeExecutionMemoryError(ExecutionResultError):
    pass
