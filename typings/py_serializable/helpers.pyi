from typing import Any


class BaseHelper: ...


class XsdDateTime:
    @classmethod
    def deserialize(cls, value: Any) -> Any: ...
    @classmethod
    def serialize(cls, value: Any) -> Any: ...
