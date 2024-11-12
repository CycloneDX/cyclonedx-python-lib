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

from typing import TYPE_CHECKING, Any, Iterable, Optional, Union

import serializable
from sortedcontainers import SortedSet

from .._internal.bom_ref import bom_ref_from_str
from .._internal.compare import ComparableTuple as _ComparableTuple
from ..serialization import BomRefHelper
from . import ExternalReference
from .bom_ref import BomRef

if TYPE_CHECKING:  # pragma: no cover
    pass


@serializable.serializable_class
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
        self._bom_ref = bom_ref_from_str(bom_ref)
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
        unique within the BOM.

        Returns:
            `BomRef`
        """
        return self._bom_ref

    @property
    @serializable.xml_sequence(1)
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
    @serializable.xml_sequence(2)
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
    @serializable.xml_sequence(3)
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
    @serializable.xml_sequence(4)
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
    # @serializable.xml_sequence(5)
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
    # @serializable.xml_sequence(6)
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
    @serializable.xml_sequence(7)
    def external_references(self) -> 'SortedSet[ExternalReference]':
        """
        Returns:
            A SortedSet of external references associated with the standard.
        """
        return self._external_references

    @external_references.setter
    def external_references(self, external_references: Iterable[ExternalReference]) -> None:
        self._external_references = SortedSet(external_references)


@serializable.serializable_class(name='definitions')
class Definitions:
    """
    The repository for definitions
    """

    def __init__(
        self, *,
        standards: Optional[Iterable[Standard]] = None
    ) -> None:
        self.standards = standards or ()  # type:ignore[assignment]

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'standard')
    @serializable.xml_sequence(1)
    def standards(self) -> 'SortedSet[Standard]':
        """
        Returns:
            A SortedSet of Standards
        """
        return self._standards

    @standards.setter
    def standards(self, standards: Iterable[Standard]) -> None:
        self._standards = SortedSet(standards)

    def __bool__(self) -> bool:
        return len(self._standards) > 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Definitions):
            return False

        return self._standards == other._standards

    def __hash__(self) -> int:
        return hash((tuple(self._standards)))

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Definitions):
            return (_ComparableTuple(self._standards)
                    < _ComparableTuple(other.standards))
        return NotImplemented

    def __repr__(self) -> str:
        return '<Definitions>'
