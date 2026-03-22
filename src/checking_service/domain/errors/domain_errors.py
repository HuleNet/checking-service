class DomainError(Exception):
    pass


class SubmissionError(DomainError):
    pass


class InputCaseError(DomainError):
    pass


class AssignmentLimitsError(DomainError):
    pass


class ExecutionResultError(DomainError):
    pass
