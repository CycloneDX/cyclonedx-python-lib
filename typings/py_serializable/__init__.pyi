from typing import Any, Callable, Iterable, Optional, TypeVar, overload
from typing_extensions import dataclass_transform

from . import helpers

_ClassT = TypeVar("_ClassT", bound=type[Any])
_DecoratedT = TypeVar("_DecoratedT")


class ViewType: ...


class SerializationType: ...


class XmlStringSerializationType:
    NORMALIZED_STRING: Any
    TOKEN: Any


class XmlArraySerializationType:
    FLAT: Any
    NESTED: Any


class ObjectMetadataLibrary:
    class SerializableProperty: ...


@dataclass_transform()
@overload
def serializable_class(
    cls: _ClassT,
    /,
    *,
    name: Optional[str] = ...,
    serialization_types: Optional[Iterable[SerializationType]] = ...,
    ignore_during_deserialization: Optional[Iterable[str]] = ...,
    ignore_unknown_during_deserialization: bool = ...,
) -> _ClassT: ...


@dataclass_transform()
@overload
def serializable_class(
    cls: None = None,
    /,
    *,
    name: Optional[str] = ...,
    serialization_types: Optional[Iterable[SerializationType]] = ...,
    ignore_during_deserialization: Optional[Iterable[str]] = ...,
    ignore_unknown_during_deserialization: bool = ...,
) -> Callable[[_ClassT], _ClassT]: ...


def serializable_enum(cls: _ClassT, /) -> _ClassT: ...


def include_none(*args: Any, **kwargs: Any) -> Callable[[_DecoratedT], _DecoratedT]: ...
def json_name(*args: Any, **kwargs: Any) -> Callable[[_DecoratedT], _DecoratedT]: ...
def string_format(*args: Any, **kwargs: Any) -> Callable[[_DecoratedT], _DecoratedT]: ...
def type_mapping(*args: Any, **kwargs: Any) -> Callable[[_DecoratedT], _DecoratedT]: ...
def view(*args: Any, **kwargs: Any) -> Callable[[_DecoratedT], _DecoratedT]: ...
def xml_array(*args: Any, **kwargs: Any) -> Callable[[_DecoratedT], _DecoratedT]: ...
def xml_attribute(*args: Any, **kwargs: Any) -> Callable[[_DecoratedT], _DecoratedT]: ...
def xml_name(*args: Any, **kwargs: Any) -> Callable[[_DecoratedT], _DecoratedT]: ...
def xml_sequence(*args: Any, **kwargs: Any) -> Callable[[_DecoratedT], _DecoratedT]: ...
def xml_string(*args: Any, **kwargs: Any) -> Callable[[_DecoratedT], _DecoratedT]: ...
