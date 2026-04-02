from checking_service.domain.enums.base_enum import BaseEnum


class Status(BaseEnum):
    passed = "passed"
    failed = "failed"
    error = "error"
    timeout = "timeout"
    memory_out = "memory_out"
