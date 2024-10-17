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

from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Type, Union
from xml.etree.ElementTree import Element  # nosec B405

import serializable
from serializable.helpers import BaseHelper
from sortedcontainers import SortedSet

from .._internal.compare import ComparableTuple as _ComparableTuple
from ..exception.serialization import CycloneDxDeserializationException
from ..serialization import BomRefHelper
from . import ExternalReference
from .bom_ref import BomRef

if TYPE_CHECKING:  # pragma: no cover
    from serializable import ObjectMetadataLibrary, ViewType


def bom_ref_or_str(bom_ref: Optional[Union[str, BomRef]]) -> BomRef:
    if isinstance(bom_ref, BomRef):
        return bom_ref
    else:
        return BomRef(value=str(bom_ref) if bom_ref else None)


@serializable.serializable_class(serialization_types=[
    serializable.SerializationType.JSON,
    serializable.SerializationType.XML]
)
class Standard:
    """
    A standard of regulations, industry or organizational-specific standards, maturity models, best practices,
    or any other requirements.
    """

    def __init__(
        self, *,
        bom_ref: Optional[Union[str, BomRef]] = None,
        name: Optional[str] = None,
        version: Optional[str] = None,
        description: Optional[str] = None,
        owner: Optional[str] = None,
        external_references: Optional[Iterable['ExternalReference']] = None
    ) -> None:
        self._bom_ref = bom_ref_or_str(bom_ref)
        self.name = name
        self.version = version
        self.description = description
        self.owner = owner
        self.external_references = external_references or []  # type:ignore[assignment]

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Standard):
            return (_ComparableTuple((self.bom_ref, self.name, self.version))
                    < _ComparableTuple((other.bom_ref, other.name, other.version)))
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Standard):
            return hash(other) == hash(self)
        return False

    def __hash__(self) -> int:
        return hash((
            self.bom_ref, self.name, self.version, self.description, self.owner, tuple(self.external_references)
        ))

    def __repr__(self) -> str:
        return f'<Standard bom-ref={self.bom_ref}, name={self.name}, version={self.version}, ' \
               f'description={self.description}, owner={self.owner}>'

    @property
    @serializable.json_name('bom-ref')
    @serializable.type_mapping(BomRefHelper)
    @serializable.xml_attribute()
    @serializable.xml_name('bom-ref')
    def bom_ref(self) -> BomRef:
        """
        An optional identifier which can be used to reference the standard elsewhere in the BOM. Every bom-ref MUST be
        unique within the BOM. If a value was not provided in the constructor, a UUIDv4 will have been assigned.
        Returns:
            `BomRef`
        """
        return self._bom_ref

    @property
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    @serializable.xml_sequence(2)
    def name(self) -> Optional[str]:
        """
        Returns:
            The name of the standard
        """
        return self._name

    @name.setter
    def name(self, name: Optional[str]) -> None:
        self._name = name

    @property
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    @serializable.xml_sequence(3)
    def version(self) -> Optional[str]:
        """
        Returns:
            The version of the standard
        """
        return self._version

    @version.setter
    def version(self, version: Optional[str]) -> None:
        self._version = version

    @property
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    @serializable.xml_sequence(4)
    def description(self) -> Optional[str]:
        """
        Returns:
            The description of the standard
        """
        return self._description

    @description.setter
    def description(self, description: Optional[str]) -> None:
        self._description = description

    @property
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    @serializable.xml_sequence(5)
    def owner(self) -> Optional[str]:
        """
        Returns:
            The owner of the standard, often the entity responsible for its release.
        """
        return self._owner

    @owner.setter
    def owner(self, owner: Optional[str]) -> None:
        self._owner = owner

    # @property
    # @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'requirement')
    # @serializable.xml_sequence(10)
    # def requirements(self) -> 'SortedSet[Requirement]':
    #     """
    #     Returns:
    #         A SortedSet of requirements comprising the standard.
    #     """
    #     return self._requirements
    #
    # @requirements.setter
    # def requirements(self, requirements: Iterable[Requirement]) -> None:
    #     self._requirements = SortedSet(requirements)
    #
    # @property
    # @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'level')
    # @serializable.xml_sequence(20)
    # def levels(self) -> 'SortedSet[Level]':
    #     """
    #     Returns:
    #         A SortedSet of levels associated with the standard. Some standards have different levels of compliance.
    #     """
    #     return self._levels
    #
    # @levels.setter
    # def levels(self, levels: Iterable[Level]) -> None:
    #     self._levels = SortedSet(levels)

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'reference')
    @serializable.xml_sequence(30)
    def external_references(self) -> 'SortedSet[ExternalReference]':
        """
        Returns:
            A SortedSet of external references associated with the standard.
        """
        return self._external_references

    @external_references.setter
    def external_references(self, external_references: Iterable[ExternalReference]) -> None:
        self._external_references = SortedSet(external_references)


class DefinitionRepository:
    """
    The repository for definitions
    """

    def __init__(
        self, *,
        standards: Optional[Iterable[Standard]] = None
    ) -> None:
        self.standards = standards or ()  # type:ignore[assignment]

    @property
    def standards(self) -> 'SortedSet[Standard]':
        """
        Returns:
            A SortedSet of Standards
        """
        return self._standards

    @standards.setter
    def standards(self, standards: Iterable[Standard]) -> None:
        self._standards = SortedSet(standards)

    def __len__(self) -> int:
        return len(self._standards)

    def __bool__(self) -> bool:
        return len(self._standards) > 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DefinitionRepository):
            return False

        return self._standards == other._standards

    def __hash__(self) -> int:
        return hash((tuple(self._standards)))

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, DefinitionRepository):
            return (_ComparableTuple(self._standards)
                    < _ComparableTuple(other.standards))
        return NotImplemented

    def __repr__(self) -> str:
        return '<Definitions>'


class _DefinitionRepositoryHelper(BaseHelper):
    """
    Helper class for serializing and deserializing a Definitions.
    """

    @classmethod
    def json_normalize(cls, o: DefinitionRepository, *,
                       view: Optional[Type['ViewType']],
                       **__: Any) -> Any:
        elem: Dict[str, Any] = {}
        if o.standards:
            elem['standards'] = tuple(o.standards)
        return elem or None

    @classmethod
    def json_denormalize(cls, o: Union[List[Dict[str, Any]], Dict[str, Any]],
                         **__: Any) -> DefinitionRepository:
        standards = None
        if isinstance(o, Dict):
            standards = map(lambda c: Standard.from_json(c),  # type:ignore[attr-defined]
                            o.get('standards', ()))
        return DefinitionRepository(standards=standards)

    @classmethod
    def xml_normalize(cls, o: DefinitionRepository, *,
                      element_name: str,
                      view: Optional[Type['ViewType']],
                      xmlns: Optional[str],
                      **__: Any) -> Optional[Element]:
        elem = Element(element_name)
        if o.standards:
            elem_s = Element(f'{{{xmlns}}}standards' if xmlns else 'standards')
            elem_s.extend(
                si.as_xml(  # type:ignore[attr-defined]
                    view_=view, as_string=False, element_name='standard', xmlns=xmlns)
                for si in o.standards)
            elem.append(elem_s)
        return elem \
            if len(elem) > 0 \
            else None

    @classmethod
    def xml_denormalize(cls, o: Element, *,
                        default_ns: Optional[str],
                        prop_info: 'ObjectMetadataLibrary.SerializableProperty',
                        ctx: Type[Any],
                        **kwargs: Any) -> DefinitionRepository:
        standards = None
        for e in o:
            tag = e.tag if default_ns is None else e.tag.replace(f'{{{default_ns}}}', '')
            if tag == 'standards':
                standards = map(lambda s: Standard.from_xml(  # type:ignore[attr-defined]
                    s, default_ns), e)
            else:
                raise CycloneDxDeserializationException(f'unexpected: {e!r}')
        return DefinitionRepository(standards=standards)
