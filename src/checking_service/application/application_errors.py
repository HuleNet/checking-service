from checking_service.domain.errors.base_error import BaseError


class ApplicationError(BaseError):
    code = "application_error"


class ValidationError(ApplicationError):
    code = "validation_error"


class NotFoundError(ApplicationError):
    code = "not_found"


class ExternalServiceError(ApplicationError):
    code = "external_service_error"
