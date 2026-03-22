from checking_service.domain.errors.domain_errors import AssignmentLimitsError


class AssignmentLimitsNegativeTimeLimitError(AssignmentLimitsError):
    pass


class AssignmentLimitsNegativeMemoryLimitError(AssignmentLimitsError):
    pass
