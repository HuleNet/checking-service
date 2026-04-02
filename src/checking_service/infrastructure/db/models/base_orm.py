from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def __repr__(self) -> str:
        fields = []

        for key in self.__mapper__.c.keys():
            value = getattr(self, key, None)
            fields.append(f"{key}={value!r}")

        return f"{self.__class__.__name__}({', '.join(fields)})"
