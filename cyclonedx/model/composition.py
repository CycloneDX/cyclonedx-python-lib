# This file is part of CycloneDX Python Library
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# Copyright (C) Siemens 2026. All Rights Reserved.

"""
    This set of classes represents the compositions in the CycloneDX standard.

.. note::
    Introduced in CycloneDX v1.3

.. note::
    See the CycloneDX Schema for compositions: https://cyclonedx.org/docs/1.7/xml/#type_compositionType
"""

from collections.abc import Iterable
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional, Union
from xml.etree.ElementTree import Element  # nosec B405

import py_serializable as serializable
from py_serializable.helpers import BaseHelper
from sortedcontainers import SortedSet

from .._internal.bom_ref import bom_ref_from_str as _bom_ref_from_str
from .._internal.compare import ComparableTuple as _ComparableTuple
from ..schema.schema import (
    SchemaVersion1Dot3,
    SchemaVersion1Dot4,
    SchemaVersion1Dot5,
    SchemaVersion1Dot6,
    SchemaVersion1Dot7,
)
from . import _BOM_LINK_PREFIX, XsUri
from .bom_ref import BomRef

if TYPE_CHECKING:  # pragma: no cover
    from py_serializable import ViewType


def _get_ref_attr(elem: Element) -> str:
    """Read the ``ref`` attribute, tolerating namespace-qualified attribute names."""
    for key, value in elem.attrib.items():
        if key == 'ref' or key.endswith('}ref'):
            return value
    return ''


@serializable.serializable_enum
class AggregateType(str, Enum):
    """
    Enum object that defines the permissible 'aggregate' types for a Composition according to the CycloneDX schema.

    Specifies an aggregate type that describes how complete a relationship is.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_aggregateType
    """
    COMPLETE = 'complete'
    INCOMPLETE = 'incomplete'
    INCOMPLETE_FIRST_PARTY_ONLY = 'incomplete_first_party_only'
    INCOMPLETE_FIRST_PARTY_PROPRIETARY_ONLY = 'incomplete_first_party_proprietary_only'
    INCOMPLETE_FIRST_PARTY_OPENSOURCE_ONLY = 'incomplete_first_party_opensource_only'
    INCOMPLETE_THIRD_PARTY_ONLY = 'incomplete_third_party_only'
    INCOMPLETE_THIRD_PARTY_PROPRIETARY_ONLY = 'incomplete_third_party_proprietary_only'
    INCOMPLETE_THIRD_PARTY_OPENSOURCE_ONLY = 'incomplete_third_party_opensource_only'
    UNKNOWN = 'unknown'
    NOT_SPECIFIED = 'not_specified'


class _AggregateTypeSerializationHelper(BaseHelper):
    """  THIS CLASS IS NON-PUBLIC API

    Down-maps `AggregateType` values that are not supported by a given schema version to a supported value.
    """

    __CASES: dict[type['ViewType'], frozenset[AggregateType]] = dict()
    __CASES[SchemaVersion1Dot3] = frozenset({
        AggregateType.COMPLETE,
        AggregateType.INCOMPLETE,
        AggregateType.INCOMPLETE_FIRST_PARTY_ONLY,
        AggregateType.INCOMPLETE_THIRD_PARTY_ONLY,
        AggregateType.UNKNOWN,
        AggregateType.NOT_SPECIFIED,
    })
    __CASES[SchemaVersion1Dot4] = __CASES[SchemaVersion1Dot3]
    __CASES[SchemaVersion1Dot5] = __CASES[SchemaVersion1Dot4] | {
        AggregateType.INCOMPLETE_FIRST_PARTY_PROPRIETARY_ONLY,
        AggregateType.INCOMPLETE_FIRST_PARTY_OPENSOURCE_ONLY,
        AggregateType.INCOMPLETE_THIRD_PARTY_PROPRIETARY_ONLY,
        AggregateType.INCOMPLETE_THIRD_PARTY_OPENSOURCE_ONLY,
    }
    __CASES[SchemaVersion1Dot6] = __CASES[SchemaVersion1Dot5]
    __CASES[SchemaVersion1Dot7] = __CASES[SchemaVersion1Dot6]

    @classmethod
    def __normalize(cls, aggregate: AggregateType, view: type['ViewType']) -> str:
        return (
            aggregate
            if aggregate in cls.__CASES.get(view, ())
            else AggregateType.INCOMPLETE
        ).value

    @classmethod
    def json_normalize(cls, o: Any, *,
                       view: Optional[type['ViewType']],
                       **__: Any) -> str:
        assert view is not None
        return cls.__normalize(o, view)

    @classmethod
    def xml_normalize(cls, o: Any, *,
                      view: Optional[type['ViewType']],
                      **__: Any) -> str:
        assert view is not None
        return cls.__normalize(o, view)

    @classmethod
    def json_denormalize(cls, o: Any, **__: Any) -> AggregateType:
        return AggregateType(o)

    @classmethod
    def xml_denormalize(cls, o: Any, **__: Any) -> AggregateType:
        return AggregateType(o.text if hasattr(o, 'text') else o)


_Assembly = Union[BomRef, XsUri]
"""TypeAlias for a single assembly reference.

An assembly is either a plain ``bom-ref`` (:class:`BomRef`) or a BOM-Link element (:class:`XsUri`).
"""


if TYPE_CHECKING:  # pragma: no cover
    # workaround for https://github.com/python/mypy/issues/5264
    class _AssemblyRepository(SortedSet[_Assembly]):
        """Collection of assembly references.

        This is a `set`, not a `list`.  Order MUST NOT matter here.
        """

    class _BomRefRepository(SortedSet[BomRef]):
        """Collection of `BomRef`.

        This is a `set`, not a `list`.  Order MUST NOT matter here.
        """
else:
    class _AssemblyRepository(SortedSet):
        """Collection of assembly references.

        This is a `set`, not a `list`.  Order MUST NOT matter here.
        """

        def __init__(self, iterable: Any = None) -> None:
            # `BomRef` and `XsUri` are not mutually comparable; sort by string value.
            super().__init__(iterable, key=str)

    class _BomRefRepository(SortedSet):
        """Collection of `BomRef`.

        This is a `set`, not a `list`.  Order MUST NOT matter here.
        """


class _AssemblyRepositoryHelper(BaseHelper):
    @classmethod
    def json_normalize(cls, o: _AssemblyRepository, *,
                       view: Optional[type['ViewType']],
                       **__: Any) -> Any:
        if len(o) == 0:
            return None
        return [str(a) for a in o]

    @classmethod
    def json_denormalize(cls, o: list[Any],
                         **__: Any) -> _AssemblyRepository:
        repo = _AssemblyRepository()
        for a in o:
            s = str(a)
            if s.startswith(_BOM_LINK_PREFIX):
                repo.add(XsUri(s))
            else:
                repo.add(BomRef(value=s))
        return repo

    @classmethod
    def xml_normalize(cls, o: _AssemblyRepository, *,
                      element_name: str,
                      view: Optional[type['ViewType']],
                      xmlns: Optional[str],
                      **__: Any) -> Optional[Element]:
        if len(o) == 0:
            return None
        elem = Element(element_name)
        tag = f'{{{xmlns}}}assembly' if xmlns else 'assembly'
        for a in o:
            child = Element(tag)
            child.set(f'{{{xmlns}}}ref' if xmlns else 'ref', str(a))
            elem.append(child)
        return elem

    @classmethod
    def xml_denormalize(cls, o: Element,
                        default_ns: Optional[str],
                        **__: Any) -> _AssemblyRepository:
        repo = _AssemblyRepository()
        ns_map = {'bom': default_ns or ''}
        for a in o.iterfind('bom:assembly', ns_map):
            ref = _get_ref_attr(a)
            if ref.startswith(_BOM_LINK_PREFIX):
                repo.add(XsUri(ref))
            else:
                repo.add(BomRef(value=ref))
        return repo


class _BomRefRepositoryHelper(BaseHelper):
    """Serialize a `SortedSet` of `BomRef` as a nested XML wrapper / JSON list of strings."""

    _element_item_name = 'item'

    @classmethod
    def json_normalize(cls, o: _BomRefRepository, *,
                       view: Optional[type['ViewType']],
                       **__: Any) -> Any:
        if len(o) == 0:
            return None
        return [str(r) for r in o]

    @classmethod
    def json_denormalize(cls, o: list[Any],
                         **__: Any) -> _BomRefRepository:
        repo = _BomRefRepository()
        for r in o:
            repo.add(BomRef(value=str(r)))
        return repo

    @classmethod
    def xml_normalize(cls, o: _BomRefRepository, *,
                      element_name: str,
                      view: Optional[type['ViewType']],
                      xmlns: Optional[str],
                      **__: Any) -> Optional[Element]:
        if len(o) == 0:
            return None
        elem = Element(element_name)
        tag = f'{{{xmlns}}}{cls._element_item_name}' if xmlns else cls._element_item_name
        for r in o:
            child = Element(tag)
            child.set(f'{{{xmlns}}}ref' if xmlns else 'ref', str(r))
            elem.append(child)
        return elem

    @classmethod
    def xml_denormalize(cls, o: Element,
                        default_ns: Optional[str],
                        **__: Any) -> _BomRefRepository:
        repo = _BomRefRepository()
        ns_map = {'bom': default_ns or ''}
        for r in o.iterfind(f'bom:{cls._element_item_name}', ns_map):
            repo.add(BomRef(value=_get_ref_attr(r)))
        return repo


class _DependencyRefRepositoryHelper(_BomRefRepositoryHelper):
    _element_item_name = 'dependency'


class _VulnerabilityRefRepositoryHelper(_BomRefRepositoryHelper):
    _element_item_name = 'vulnerability'


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class Composition:
    """
    Models a Composition within a BOM.

    .. note::
        See https://cyclonedx.org/docs/1.7/xml/#type_compositionType
    """

    def __init__(
        self, *,
        aggregate: AggregateType = AggregateType.NOT_SPECIFIED,
        assemblies: Optional[Iterable[_Assembly]] = None,
        dependencies: Optional[Iterable[BomRef]] = None,
        vulnerabilities: Optional[Iterable[BomRef]] = None,
        bom_ref: Optional[Union[str, BomRef]] = None,
    ) -> None:
        self._bom_ref = _bom_ref_from_str(bom_ref, optional=True)
        self.aggregate = aggregate
        self.assemblies = assemblies or []  # type:ignore[assignment]
        self.dependencies = dependencies or []
        self.vulnerabilities = vulnerabilities or []

    @property
    @serializable.json_name('bom-ref')
    @serializable.type_mapping(BomRef)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_attribute()
    @serializable.xml_name('bom-ref')
    def bom_ref(self) -> Optional[BomRef]:
        """
        An optional identifier which can be used to reference the composition elsewhere in the BOM.
        Every bom-ref MUST be unique within the BOM.

        Returns:
            `BomRef`
        """
        return self._bom_ref

    @property
    @serializable.type_mapping(_AggregateTypeSerializationHelper)
    @serializable.view(SchemaVersion1Dot3)
    @serializable.view(SchemaVersion1Dot4)
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(1)
    def aggregate(self) -> AggregateType:
        """
        Specifies an aggregate type that describes how complete a relationship is.

        Returns:
            `AggregateType`
        """
        return self._aggregate

    @aggregate.setter
    def aggregate(self, aggregate: AggregateType) -> None:
        self._aggregate = aggregate

    @property
    @serializable.type_mapping(_AssemblyRepositoryHelper)
    @serializable.view(SchemaVersion1Dot3)
    @serializable.view(SchemaVersion1Dot4)
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(2)
    def assemblies(self) -> _AssemblyRepository:
        """
        The bom-ref identifiers of the components or services being described. Assemblies refer to nested
        relationships whereby a constituent part may include other constituent parts.

        Returns:
            Set of `BomRef`/`XsUri`
        """
        return self._assemblies

    @assemblies.setter
    def assemblies(self, assemblies: Iterable[_Assembly]) -> None:
        self._assemblies = _AssemblyRepository(assemblies)

    @property
    @serializable.type_mapping(_DependencyRefRepositoryHelper)
    @serializable.view(SchemaVersion1Dot3)
    @serializable.view(SchemaVersion1Dot4)
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(3)
    def dependencies(self) -> _BomRefRepository:
        """
        The bom-ref identifiers of the components or services being described. Dependencies refer to a relationship
        whereby an independent constituent part requires another independent constituent part.

        Returns:
            Set of `BomRef`
        """
        return self._dependencies

    @dependencies.setter
    def dependencies(self, dependencies: Iterable[BomRef]) -> None:
        self._dependencies = _BomRefRepository(dependencies)

    @property
    @serializable.type_mapping(_VulnerabilityRefRepositoryHelper)
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(4)
    def vulnerabilities(self) -> _BomRefRepository:
        """
        The bom-ref identifiers of the vulnerabilities being described.

        Returns:
            Set of `BomRef`
        """
        return self._vulnerabilities

    @vulnerabilities.setter
    def vulnerabilities(self, vulnerabilities: Iterable[BomRef]) -> None:
        self._vulnerabilities = _BomRefRepository(vulnerabilities)

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((
            self._aggregate,
            _ComparableTuple(self._assemblies),
            _ComparableTuple(self._dependencies),
            _ComparableTuple(self._vulnerabilities),
        ))

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Composition):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Composition):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __repr__(self) -> str:
        return f'<Composition bom-ref={self._bom_ref!r}, aggregate={self._aggregate}>'
