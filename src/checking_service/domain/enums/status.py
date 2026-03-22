from enum import Enum


class Status(str, Enum):
    passed = "passed"
    failed = "failed"
    error = "error"
    time_out = "time_out"
    memory_out = "memory_out"
