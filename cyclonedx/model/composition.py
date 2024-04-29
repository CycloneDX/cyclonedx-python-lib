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
# Copyright (c) OWASP Foundation. All Rights Reserved.
from enum import Enum
from typing import Any, Dict, FrozenSet, Iterable, Optional, Type

import serializable
from sortedcontainers import SortedSet

from .._internal.compare import ComparableTuple as _ComparableTuple
from ..exception.serialization import SerializationOfUnsupportedAggregateTypeException
from ..schema.schema import (
    SchemaVersion1Dot0,
    SchemaVersion1Dot1,
    SchemaVersion1Dot2,
    SchemaVersion1Dot3,
    SchemaVersion1Dot4,
    SchemaVersion1Dot5,
    SchemaVersion1Dot6,
)
from ..serialization import BomRefHelper
from .bom_ref import BomRef


@serializable.serializable_enum
class AggregateType(str, Enum):
    """
    This is our internal representation of the composition.aggregate ENUM type within the CycloneDX standard.

    .. note::
        Introduced in CycloneDX v1.4

    .. note::
        See the CycloneDX Schema for hashType: https://cyclonedx.org/docs/1.4/xml/#type_aggregateType
    """

    # See `_AggregateTypeSerializationHelper.__CASES` for view/case map

    """
    The relationship is complete. No further relationships including constituent components, services, or dependencies
    are known to exist.
    """
    COMPLETE = 'complete'

    """
    The relationship is incomplete. Additional relationships exist and may include constituent components, services, or
    dependencies.
    """
    INCOMPLETE = 'incomplete'

    """
    The relationship is incomplete. Only relationships for first-party components, services, or their dependencies are
    represented.
    """
    INCOMPLETE_FIRST_PARTY_ONLY = 'incomplete_first_party_only'

    """
    The relationship is incomplete. Only relationships for first-party components, services, or their dependencies are
    represented, limited specifically to those that are proprietary.
    """
    INCOMPLETE_FIRST_PARTY_PROPRIETARY_ONLY = 'incomplete_first_party_proprietary_only'

    """
    The relationship is incomplete. Only relationships for first-party components, services, or their dependencies are
    represented, limited specifically to those that are opensource.
    """
    INCOMPLETE_FIRST_PARTY_OPENSOURCE_ONLY = 'incomplete_first_party_opensource_only'

    """
    The relationship is incomplete. Only relationships for third-party components, services, or their dependencies are
    represented.
    """
    INCOMPLETE_THIRD_PARTY_ONLY = 'incomplete_third_party_only'

    """
    The relationship is incomplete. Only relationships for third-party components, services, or their dependencies are
    represented, limited specifically to those that are proprietary.
    """
    INCOMPLETE_THIRD_PARTY_PROPRIETARY_ONLY = 'incomplete_third_party_proprietary_only'

    """
    The relationship is incomplete. Only relationships for third-party components, services, or their dependencies are
    represented, limited specifically to those that are opensource.
    """
    INCOMPLETE_THIRD_PARTY_OPENSOURCE_ONLY = 'incomplete_third_party_opensource_only'

    """
    The relationship may be complete or incomplete. This usually signifies a 'best-effort' to obtain constituent
    components, services, or dependencies but the completeness is inconclusive.
    """
    UNKNOWN = 'unknown'

    """
    The relationship completeness is not specified.
    """
    NOT_SPECIFIED = 'not_specified'


class _AggregateTypeSerializationHelper(serializable.helpers.BaseHelper):
    """  THIS CLASS IS NON-PUBLIC API  """

    __CASES: Dict[Type[serializable.ViewType], FrozenSet[AggregateType]] = dict()
    __CASES[SchemaVersion1Dot0] = frozenset({})
    __CASES[SchemaVersion1Dot1] = __CASES[SchemaVersion1Dot0]
    __CASES[SchemaVersion1Dot2] = __CASES[SchemaVersion1Dot1]
    __CASES[SchemaVersion1Dot3] = __CASES[SchemaVersion1Dot2] | {
        AggregateType.COMPLETE,
        AggregateType.INCOMPLETE,
        AggregateType.INCOMPLETE_FIRST_PARTY_ONLY,
        AggregateType.INCOMPLETE_THIRD_PARTY_ONLY,
        AggregateType.UNKNOWN,
        AggregateType.NOT_SPECIFIED
    }
    __CASES[SchemaVersion1Dot4] = __CASES[SchemaVersion1Dot3]
    __CASES[SchemaVersion1Dot5] = __CASES[SchemaVersion1Dot4] | {
        AggregateType.INCOMPLETE_FIRST_PARTY_PROPRIETARY_ONLY,
        AggregateType.INCOMPLETE_FIRST_PARTY_OPENSOURCE_ONLY,
        AggregateType.INCOMPLETE_THIRD_PARTY_PROPRIETARY_ONLY,
        AggregateType.INCOMPLETE_THIRD_PARTY_OPENSOURCE_ONLY
    }
    __CASES[SchemaVersion1Dot6] = __CASES[SchemaVersion1Dot5]

    @classmethod
    def __normalize(cls, at: AggregateType, view: Type[serializable.ViewType]) -> Optional[str]:
        print(f'Normalising {at!r} for {view!r}')
        if at in cls.__CASES.get(view, ()):
            return at.value
        raise SerializationOfUnsupportedAggregateTypeException(f'unsupported {at!r} for view {view!r}')

    @classmethod
    def json_normalize(cls, o: Any, *,
                       view: Optional[Type[serializable.ViewType]],
                       **__: Any) -> Optional[str]:
        assert view is not None
        return cls.__normalize(o, view)

    @classmethod
    def xml_normalize(cls, o: Any, *,
                      view: Optional[Type[serializable.ViewType]],
                      **__: Any) -> Optional[str]:
        assert view is not None
        return cls.__normalize(o, view)

    @classmethod
    def deserialize(cls, o: Any) -> AggregateType:
        return AggregateType(o)


@serializable.serializable_class
class CompositionReference:
    """
    Models a reference for an assembly or dependency in a Composition.

    .. note::
        See https://cyclonedx.org/docs/1.4/xml/#type_compositionType
    """

    def __init__(self, *, ref: BomRef) -> None:
        self.ref = ref

    @property
    @serializable.json_name('.')
    @serializable.type_mapping(BomRefHelper)
    @serializable.xml_attribute()
    def ref(self) -> BomRef:
        """
        References a component or service by its bom-ref attribute.

        Returns:
            `BomRef`
        """
        return self._ref

    @ref.setter
    def ref(self, ref: BomRef) -> None:
        self._ref = ref

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CompositionReference):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, CompositionReference):
            return self.ref < other.ref
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.ref)

    def __repr__(self) -> str:
        return f'<CompositionReference ref={self.ref!r}>'


@serializable.serializable_class
class Composition:
    """
    This is our internal representation of the `compositionType` type within the CycloneDX standard.

    .. note::
        Introduced in CycloneDX v1.4

    .. note::
        See the CycloneDX Schema for hashType: https://cyclonedx.org/docs/1.4/xml/#type_compositionType
    """

    def __init__(self, *, aggregate: AggregateType, assemblies: Optional[Iterable[CompositionReference]] = None,
                 dependencies: Optional[Iterable[CompositionReference]] = None) -> None:
        self.aggregate = aggregate
        self.assemblies = assemblies or []  # type:ignore[assignment]
        self.dependencies = dependencies or []  # type:ignore[assignment]

    @property
    @serializable.type_mapping(_AggregateTypeSerializationHelper)
    @serializable.xml_sequence(10)
    def aggregate(self) -> AggregateType:
        """
        Specifies an aggregate type that describe how complete a relationship is.

        Returns:
            `AggregateType`
        """
        return self._aggregate

    @aggregate.setter
    def aggregate(self, aggregate: AggregateType) -> None:
        self._aggregate = aggregate

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'assembly')
    @serializable.xml_sequence(20)
    def assemblies(self) -> 'SortedSet[CompositionReference]':
        """
        The bom-ref identifiers of the components or services being described. Assemblies refer to nested relationships
        whereby a constituent part may include other constituent parts. References do not cascade to child parts.
        References are explicit for the specified constituent part only.

        Returns:
            'SortedSet[CompositionReference]`
        """
        return self._assemblies

    @assemblies.setter
    def assemblies(self, assemblies: Optional[Iterable[CompositionReference]]) -> None:
        self._assemblies = SortedSet(assemblies)

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'dependency')
    @serializable.xml_sequence(30)
    def dependencies(self) -> 'SortedSet[CompositionReference]':
        """
        The bom-ref identifiers of the components or services being described. Dependencies refer to a relationship
        whereby an independent constituent part requires another independent constituent part. References do not
        cascade to transitive dependencies. References are explicit for the specified dependency only.

        Returns:
            'SortedSet[CompositionReference]`
        """
        return self._dependencies

    @dependencies.setter
    def dependencies(self, dependencies: Optional[Iterable[CompositionReference]]) -> None:
        self._dependencies = SortedSet(dependencies)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Composition):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Composition):
            return _ComparableTuple((
                self.aggregate, _ComparableTuple(self.assemblies), _ComparableTuple(self.dependencies)
            )) < _ComparableTuple((
                other.aggregate, _ComparableTuple(other.assemblies), _ComparableTuple(other.dependencies)
            ))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.aggregate, tuple(self.assemblies), tuple(self.dependencies)))

    def __repr__(self) -> str:
        return f'<Composition aggregate={self.aggregate!r}>'
