from typing import Any, Union
from .exceptions import ValidationError


class Field:
    def __init__(self) -> None:
        self.field_types: list = []

    def get_types(self, annotation: Any) -> None:
        """Recursively unpack the annotation and extend the accepted field types."""
        if hasattr(annotation, "__args__"):
            params = annotation.__args__
            self.get_types(params)
        else:
            self.field_types.extend(annotation)

    def validate(self) -> None:
        """Validate the provided field value is the appropriate type."""
        annotation = self.__annotations__["field_value"]

        if not hasattr(annotation, "__args__"):
            self.field_types.append(annotation)
        else:
            self.get_types(annotation)

        if not isinstance(self.field_value, tuple(self.field_types)):
            raise ValidationError(
                f"{self.field_value} is not of type {self.field_types}"
            )


class StrField(Field):

    field_value: Union[str, bytes] = None


class IntField(Field):

    field_value: int = None


class BytesField(Field):

    field_value: bytes = None