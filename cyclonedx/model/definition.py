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
# Copyright (c) OWASP Foundation. All Rights Reserved.

import re
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any, Optional, Union

from attrs import define, field
from sortedcontainers import SortedSet

from .._internal.bom_ref import bom_ref_from_str as _bom_ref_from_str
from .._internal.compare import ComparableTuple as _ComparableTuple
from ..exception.model import InvalidCreIdException
from ..exception.serialization import SerializationOfUnexpectedValueException
from . import ExternalReference, Property
from .bom_ref import BomRef

if TYPE_CHECKING:  # pragma: no cover
    from typing import TypeVar

    _T_CreId = TypeVar('_T_CreId', bound='CreId')


def _sortedset_converter(value: Any) -> SortedSet:
    """Convert a value to SortedSet."""
    if value is None:
        return SortedSet()
    if isinstance(value, SortedSet):
        return value
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes, dict)):
        return SortedSet(value)
    return SortedSet([value])


class CreId:
    """
    Helper class that allows us to perform validation on data strings that must conform to
    Common Requirements Enumeration (CRE) identifier(s).
    """

    _VALID_CRE_REGEX = re.compile(r'^CRE:[0-9]+-[0-9]+$')

    def __init__(self, id: str) -> None:
        if CreId._VALID_CRE_REGEX.match(id) is None:
            raise InvalidCreIdException(
                f'Supplied value "{id} does not meet format specification.'
            )
        self._id = id

    @property
    def id(self) -> str:
        return self._id

    @classmethod
    def serialize(cls, o: Any) -> str:
        if isinstance(o, cls):
            return str(o)
        raise SerializationOfUnexpectedValueException(
            f'Attempt to serialize a non-CreId: {o!r}')

    @classmethod
    def deserialize(cls: 'type[_T_CreId]', o: Any) -> '_T_CreId':
        return cls(id=str(o))

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, CreId):
            return self._id == other._id
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, CreId):
            return self._id < other._id
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._id)

    def __repr__(self) -> str:
        return f'<CreId {self._id}>'

    def __str__(self) -> str:
        return self._id


@define
class Requirement:
    """
    A requirement comprising a standard.

    .. note::
        See the CycloneDX Schema for hashType:
        https://cyclonedx.org/docs/1.7/json/#definitions_standards_items_requirements
    """

    _bom_ref: BomRef = field(
        factory=BomRef,
        converter=_bom_ref_from_str,
        metadata={'json_name': 'bom-ref', 'xml_name': 'bom-ref', 'xml_attribute': True}
    )
    """An optional identifier which can be used to reference the requirement elsewhere in the BOM."""

    identifier: Optional[str] = field(
        default=None,
        metadata={'json_name': 'identifier', 'xml_name': 'identifier', 'xml_sequence': 1}
    )
    """The identifier of the requirement."""

    title: Optional[str] = field(
        default=None,
        metadata={'json_name': 'title', 'xml_name': 'title', 'xml_sequence': 2}
    )
    """The title of the requirement."""

    text: Optional[str] = field(
        default=None,
        metadata={'json_name': 'text', 'xml_name': 'text', 'xml_sequence': 3}
    )
    """The text of the requirement."""

    _descriptions: 'SortedSet[str]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'descriptions', 'xml_name': 'descriptions', 'xml_item_name': 'description',
                  'xml_sequence': 4}
    )
    """A SortedSet of descriptions of the requirement."""

    _open_cre: 'SortedSet[CreId]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'openCre', 'xml_name': 'openCre', 'xml_sequence': 5}
    )
    """The Common Requirements Enumeration (CRE) identifier(s)."""

    _parent: Optional[BomRef] = field(
        default=None,
        metadata={'json_name': 'parent', 'xml_name': 'parent', 'xml_sequence': 6}
    )
    """The optional bom-ref to a parent requirement."""

    _properties: 'SortedSet[Property]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'properties', 'xml_name': 'properties', 'xml_item_name': 'property', 'xml_sequence': 7}
    )
    """Properties in a key/value store."""

    _external_references: 'SortedSet[ExternalReference]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'externalReferences', 'xml_name': 'externalReferences', 'xml_item_name': 'reference',
                  'xml_sequence': 8}
    )
    """External references related to the component."""

    @property
    def bom_ref(self) -> BomRef:
        """An optional identifier which can be used to reference the requirement elsewhere in the BOM."""
        return self._bom_ref

    @property
    def descriptions(self) -> 'SortedSet[str]':
        """A SortedSet of descriptions of the requirement."""
        return self._descriptions

    @descriptions.setter
    def descriptions(self, descriptions: Iterable[str]) -> None:
        self._descriptions = SortedSet(descriptions)

    @property
    def open_cre(self) -> 'SortedSet[CreId]':
        """The Common Requirements Enumeration (CRE) identifier(s)."""
        return self._open_cre

    @open_cre.setter
    def open_cre(self, open_cre: Iterable[CreId]) -> None:
        self._open_cre = SortedSet(open_cre)

    @property
    def parent(self) -> Optional[BomRef]:
        """The optional bom-ref to a parent requirement."""
        return self._parent

    @parent.setter
    def parent(self, parent: Optional[Union[str, BomRef]]) -> None:
        self._parent = _bom_ref_from_str(parent, optional=True)

    @property
    def properties(self) -> 'SortedSet[Property]':
        """Properties in a key/value store."""
        return self._properties

    @properties.setter
    def properties(self, properties: Iterable[Property]) -> None:
        self._properties = SortedSet(properties)

    @property
    def external_references(self) -> 'SortedSet[ExternalReference]':
        """External references related to the component."""
        return self._external_references

    @external_references.setter
    def external_references(self, external_references: Iterable[ExternalReference]) -> None:
        self._external_references = SortedSet(external_references)

    def __hash__(self) -> int:
        return hash((self.identifier, self.bom_ref.value, self.title, self.text))

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Requirement):
            return (self.identifier or '', self.bom_ref.value or '') < (other.identifier or '', other.bom_ref.value or '')
        return NotImplemented


@define
class Level:
    """
    Level of compliance for a standard.

    .. note::
        See the CycloneDX Schema for hashType: https://cyclonedx.org/docs/1.7/json/#definitions_standards_items_levels
    """

    _bom_ref: BomRef = field(
        factory=BomRef,
        converter=_bom_ref_from_str,
        metadata={'json_name': 'bom-ref', 'xml_name': 'bom-ref', 'xml_attribute': True}
    )
    """An optional identifier which can be used to reference the level elsewhere in the BOM."""

    identifier: Optional[str] = field(
        default=None,
        metadata={'json_name': 'identifier', 'xml_name': 'identifier', 'xml_sequence': 1}
    )
    """The identifier of the level."""

    title: Optional[str] = field(
        default=None,
        metadata={'json_name': 'title', 'xml_name': 'title', 'xml_sequence': 2}
    )
    """The title of the level."""

    description: Optional[str] = field(
        default=None,
        metadata={'json_name': 'description', 'xml_name': 'description', 'xml_sequence': 3}
    )
    """The description of the level."""

    _requirements: 'SortedSet[BomRef]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'requirements', 'xml_name': 'requirements', 'xml_item_name': 'requirement',
                  'xml_sequence': 4}
    )
    """A SortedSet of requirements associated with the level."""

    @property
    def bom_ref(self) -> BomRef:
        """An optional identifier which can be used to reference the level elsewhere in the BOM."""
        return self._bom_ref

    @property
    def requirements(self) -> 'SortedSet[BomRef]':
        """A SortedSet of requirements associated with the level."""
        return self._requirements

    @requirements.setter
    def requirements(self, requirements: Iterable[Union[str, BomRef]]) -> None:
        self._requirements = SortedSet(map(_bom_ref_from_str,  # type:ignore[arg-type]
                                           requirements))

    def __hash__(self) -> int:
        return hash((self.identifier, self.bom_ref.value, self.title, self.description))

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Level):
            return (self.identifier or '', self.bom_ref.value or '') < (other.identifier or '', other.bom_ref.value or '')
        return NotImplemented


@define
class Standard:
    """
    A standard of regulations, industry or organizational-specific standards, maturity models, best practices,
    or any other requirements.

    .. note::
        See the CycloneDX Schema for hashType: https://cyclonedx.org/docs/1.7/xml/#type_standard
    """

    _bom_ref: BomRef = field(
        factory=BomRef,
        converter=_bom_ref_from_str,
        metadata={'json_name': 'bom-ref', 'xml_name': 'bom-ref', 'xml_attribute': True}
    )
    """An optional identifier which can be used to reference the standard elsewhere in the BOM."""

    name: Optional[str] = field(
        default=None,
        metadata={'json_name': 'name', 'xml_name': 'name', 'xml_sequence': 1}
    )
    """The name of the standard."""

    version: Optional[str] = field(
        default=None,
        metadata={'json_name': 'version', 'xml_name': 'version', 'xml_sequence': 2}
    )
    """The version of the standard."""

    description: Optional[str] = field(
        default=None,
        metadata={'json_name': 'description', 'xml_name': 'description', 'xml_sequence': 3}
    )
    """The description of the standard."""

    owner: Optional[str] = field(
        default=None,
        metadata={'json_name': 'owner', 'xml_name': 'owner', 'xml_sequence': 4}
    )
    """The owner of the standard."""

    _requirements: 'SortedSet[Requirement]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'requirements', 'xml_name': 'requirements', 'xml_item_name': 'requirement',
                  'xml_sequence': 5}
    )
    """A SortedSet of requirements comprising the standard."""

    _levels: 'SortedSet[Level]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'levels', 'xml_name': 'levels', 'xml_item_name': 'level', 'xml_sequence': 6}
    )
    """A SortedSet of levels associated with the standard."""

    _external_references: 'SortedSet[ExternalReference]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'externalReferences', 'xml_name': 'externalReferences', 'xml_item_name': 'reference',
                  'xml_sequence': 7}
    )
    """A SortedSet of external references associated with the standard."""

    @property
    def bom_ref(self) -> BomRef:
        """An optional identifier which can be used to reference the standard elsewhere in the BOM."""
        return self._bom_ref

    @property
    def requirements(self) -> 'SortedSet[Requirement]':
        """A SortedSet of requirements comprising the standard."""
        return self._requirements

    @requirements.setter
    def requirements(self, requirements: Iterable[Requirement]) -> None:
        self._requirements = SortedSet(requirements)

    @property
    def levels(self) -> 'SortedSet[Level]':
        """A SortedSet of levels associated with the standard."""
        return self._levels

    @levels.setter
    def levels(self, levels: Iterable[Level]) -> None:
        self._levels = SortedSet(levels)

    @property
    def external_references(self) -> 'SortedSet[ExternalReference]':
        """A SortedSet of external references associated with the standard."""
        return self._external_references

    @external_references.setter
    def external_references(self, external_references: Iterable[ExternalReference]) -> None:
        self._external_references = SortedSet(external_references)

    def __hash__(self) -> int:
        return hash((self.name, self.version, self.bom_ref.value))

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Standard):
            return (self.name or '', self.version or '') < (other.name or '', other.version or '')
        return NotImplemented


@define
class Definitions:
    """
    The repository for definitions

    .. note::
        See the CycloneDX Schema for hashType: https://cyclonedx.org/docs/1.7/xml/#type_definitionsType
    """

    _standards: 'SortedSet[Standard]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'standards', 'xml_name': 'standards', 'xml_item_name': 'standard', 'xml_sequence': 1}
    )
    """A SortedSet of Standards."""

    @property
    def standards(self) -> 'SortedSet[Standard]':
        """A SortedSet of Standards."""
        return self._standards

    @standards.setter
    def standards(self, standards: Iterable[Standard]) -> None:
        self._standards = SortedSet(standards)

    def __bool__(self) -> bool:
        return len(self._standards) > 0

    def __len__(self) -> int:
        return len(self._standards)

    def __hash__(self) -> int:
        return hash(tuple(self._standards))
