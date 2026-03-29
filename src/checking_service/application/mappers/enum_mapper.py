from checking_service.domain.enums.language import Language
from checking_service.domain.domain_errors import UnsupportedTypeError


def map_str_to_language(value: str) -> Language:
    try:
        return Language(value)
    except ValueError:
        raise UnsupportedTypeError(
            "Unsupported language",
            field="language",
            value=value,
            allowed=Language.values(),
        )
