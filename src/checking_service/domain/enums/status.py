from checking_service.domain.enums.base_enum import BaseEnum


class Status(BaseEnum):
    passed = "passed"
    failed = "failed"
    error = "error"
    time_out = "time_out"
    memory_out = "memory_out"
