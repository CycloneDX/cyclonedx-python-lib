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


from typing import Any, Iterable, Optional, Type
from warnings import warn

import serializable
from sortedcontainers import SortedSet

from .._internal.compare import ComparableTuple as _ComparableTuple
from ..schema.schema import SchemaVersion1Dot4, SchemaVersion1Dot5, SchemaVersion1Dot6
from . import ExternalReference, HashType, _HashTypeRepositorySerializationHelper
from .component import Component
from .service import Service


@serializable.serializable_class
class Tool:
    """
    This is our internal representation of the `toolType` complex type within the CycloneDX standard.

    Tool(s) are the things used in the creation of the CycloneDX document.

    Tool might be deprecated since CycloneDX 1.5, but it is not deprecated in this library.
    In fact, this library will try to provide a compatibility layer if needed.

    .. note::
        See the CycloneDX Schema for toolType: https://cyclonedx.org/docs/1.3/#type_toolType
    """

    def __init__(
        self, *,
        vendor: Optional[str] = None,
        name: Optional[str] = None,
        version: Optional[str] = None,
        hashes: Optional[Iterable[HashType]] = None,
        external_references: Optional[Iterable[ExternalReference]] = None,
    ) -> None:
        self.vendor = vendor
        self.name = name
        self.version = version
        self.hashes = hashes or []  # type:ignore[assignment]
        self.external_references = external_references or []  # type:ignore[assignment]

    @property
    @serializable.xml_sequence(1)
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def vendor(self) -> Optional[str]:
        """
        The name of the vendor who created the tool.

        Returns:
            `str` if set else `None`
        """
        return self._vendor

    @vendor.setter
    def vendor(self, vendor: Optional[str]) -> None:
        self._vendor = vendor

    @property
    @serializable.xml_sequence(2)
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def name(self) -> Optional[str]:
        """
        The name of the tool.

        Returns:
             `str` if set else `None`
        """
        return self._name

    @name.setter
    def name(self, name: Optional[str]) -> None:
        self._name = name

    @property
    @serializable.xml_sequence(3)
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def version(self) -> Optional[str]:
        """
        The version of the tool.

        Returns:
             `str` if set else `None`
        """
        return self._version

    @version.setter
    def version(self, version: Optional[str]) -> None:
        self._version = version

    @property
    @serializable.type_mapping(_HashTypeRepositorySerializationHelper)
    @serializable.xml_sequence(4)
    def hashes(self) -> 'SortedSet[HashType]':
        """
        The hashes of the tool (if applicable).

        Returns:
            Set of `HashType`
        """
        return self._hashes

    @hashes.setter
    def hashes(self, hashes: Iterable[HashType]) -> None:
        self._hashes = SortedSet(hashes)

    @property
    @serializable.view(SchemaVersion1Dot4)
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'reference')
    @serializable.xml_sequence(5)
    def external_references(self) -> 'SortedSet[ExternalReference]':
        """
        External References provides a way to document systems, sites, and information that may be relevant but which
        are not included with the BOM.

        Returns:
            Set of `ExternalReference`
        """
        return self._external_references

    @external_references.setter
    def external_references(self, external_references: Iterable[ExternalReference]) -> None:
        self._external_references = SortedSet(external_references)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Tool):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Tool):
            return _ComparableTuple((
                self.vendor, self.name, self.version
            )) < _ComparableTuple((
                other.vendor, other.name, other.version
            ))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.vendor, self.name, self.version, tuple(self.hashes), tuple(self.external_references)))

    def __repr__(self) -> str:
        return f'<Tool name={self.name}, version={self.version}, vendor={self.vendor}>'

    @classmethod
    def from_component(cls: Type['Tool'], component: 'Component') -> 'Tool':
        return cls(
            vendor=component.group,
            name=component.name,
            version=component.version,
            hashes=component.hashes,
            external_references=component.external_references,
        )

    @classmethod
    def from_service(cls: Type['Tool'], service: 'Service') -> 'Tool':
        return cls(
            vendor=service.group,
            name=service.name,
            version=service.version,
            external_references=service.external_references,
        )


class ToolsRepository:
    """
    The repository of tool formats
    """

    def __init__(
        self, *,
        components: Optional[Iterable[Component]] = None,
        services: Optional[Iterable[Service]] = None,
        # Deprecated since v1.5
        tools: Optional[Iterable[Tool]] = None
    ) -> None:
        if tools:
            warn('Using Tool is deprecated as of CycloneDX v1.5. Components and Services should be used now. '
                 'See https://cyclonedx.org/docs/1.5/', DeprecationWarning)
        self._components = SortedSet(components or [])
        self._services = SortedSet(services or [])
        self._tools = SortedSet(tools or [])

    @property
    def components(self) -> 'SortedSet[Component]':
        """
        Returns:
            A SortedSet of Components
        """
        return self._components

    @components.setter
    def components(self, components: Iterable[Component]) -> None:
        self._components = SortedSet(components)

    @property
    def services(self) -> 'SortedSet[Service]':
        """
        Returns:
            A SortedSet of Services
        """
        return self._services

    @services.setter
    def services(self, services: Iterable[Service]) -> None:
        self._services = SortedSet(services)

    @property
    def tools(self) -> 'SortedSet[Tool]':
        return self._tools

    @tools.setter
    def tools(self, tools: Iterable[Tool]) -> None:
        self._tools = SortedSet(tools)

    def __len__(self) -> int:
        return len(self._tools) \
            + len(self._components) \
            + len(self._services)

    def __bool__(self) -> bool:
        return len(self._tools) > 0 \
            or len(self._components) > 0 \
            or len(self._services) > 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ToolsRepository):
            return False

        return self._tools == other._tools \
            and self._components == other._components \
            and self._services == other._services

    def __hash__(self) -> int:
        return hash((tuple(self._tools), tuple(self._components), tuple(self._services)))
