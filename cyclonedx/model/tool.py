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


from collections.abc import Iterable
from itertools import chain
from typing import TYPE_CHECKING, Any, Optional
from warnings import warn

import attrs
from sortedcontainers import SortedSet

from ..serialization import METADATA_KEY_VERSIONS, METADATA_KEY_XML_SEQUENCE, VERSIONS_1_4_AND_LATER
from . import ExternalReference, HashType

if TYPE_CHECKING:  # pragma: no cover
    from .component import Component
    from .service import Service


def _sortedset_factory() -> SortedSet:
    return SortedSet()


def _sortedset_converter(value: Any) -> SortedSet:
    """Convert a value to SortedSet."""
    if value is None:
        return SortedSet()
    if isinstance(value, SortedSet):
        return value
    if isinstance(value, (list, tuple, set, frozenset)):
        return SortedSet(value)
    return SortedSet([value])


@attrs.define
class Tool:
    """
    This is our internal representation of the `toolType` complex type within the CycloneDX standard.

    Tool(s) are the things used in the creation of the CycloneDX document.

    Tool might be deprecated since CycloneDX 1.5, but it is not deprecated in this library.
    In fact, this library will try to provide a compatibility layer if needed.

    .. note::
        See the CycloneDX Schema for toolType: https://cyclonedx.org/docs/1.7/xml/#type_toolType
    """
    vendor: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 1}
    )
    name: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 2}
    )
    version: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 3}
    )
    hashes: 'SortedSet[HashType]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={METADATA_KEY_XML_SEQUENCE: 4}
    )
    external_references: 'SortedSet[ExternalReference]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_4_AND_LATER,
            METADATA_KEY_XML_SEQUENCE: 5,
        }
    )

    @staticmethod
    def _cmp(val: Any) -> tuple:
        """Wrap value for None-safe comparison (None sorts last)."""
        return (0, val) if val is not None else (1, '')

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Tool):
            c = self._cmp
            return (
                c(self.vendor), c(self.name), c(self.version),
                tuple(self.hashes), tuple(self.external_references)
            ) < (
                c(other.vendor), c(other.name), c(other.version),
                tuple(other.hashes), tuple(other.external_references)
            )
        return NotImplemented

    def __hash__(self) -> int:
        return hash((
            self.vendor, self.name, self.version,
            tuple(self.hashes), tuple(self.external_references)
        ))

    def __repr__(self) -> str:
        return f'<Tool name={self.name}, version={self.version}, vendor={self.vendor}>'

    @classmethod
    def from_component(cls: type['Tool'], component: 'Component') -> 'Tool':
        return cls(
            vendor=component.group,
            name=component.name,
            version=component.version,
            hashes=component.hashes,
            external_references=component.external_references,
        )

    @classmethod
    def from_service(cls: type['Tool'], service: 'Service') -> 'Tool':
        return cls(
            vendor=service.group,
            name=service.name,
            version=service.version,
            external_references=service.external_references,
        )


class ToolRepository:
    """
    The repository of tool formats
    """

    def __init__(
        self, *,
        components: Optional[Iterable['Component']] = None,
        services: Optional[Iterable['Service']] = None,
        # Deprecated since v1.5
        tools: Optional[Iterable[Tool]] = None
    ) -> None:
        self._components: SortedSet = SortedSet(components or ())
        self._services: SortedSet = SortedSet(services or ())
        self._tools: SortedSet = SortedSet()
        if tools:
            warn('`@.tools` is deprecated from CycloneDX v1.5 onwards. '
                 'Please use `@.components` and `@.services` instead.',
                 DeprecationWarning)
            self._tools = SortedSet(tools)

    @property
    def components(self) -> 'SortedSet[Component]':
        """
        Returns:
            A SortedSet of Components
        """
        return self._components

    @components.setter
    def components(self, components: Iterable['Component']) -> None:
        self._components = SortedSet(components)

    @property
    def services(self) -> 'SortedSet[Service]':
        """
        Returns:
            A SortedSet of Services
        """
        return self._services

    @services.setter
    def services(self, services: Iterable['Service']) -> None:
        self._services = SortedSet(services)

    @property
    def tools(self) -> 'SortedSet[Tool]':
        return self._tools

    @tools.setter
    def tools(self, tools: Iterable[Tool]) -> None:
        if tools:
            warn('`@.tools` is deprecated from CycloneDX v1.5 onwards. '
                 'Please use `@.components` and `@.services` instead.',
                 DeprecationWarning)
        self._tools = SortedSet(tools)

    def __len__(self) -> int:
        return len(self._tools) + len(self._components) + len(self._services)

    def __bool__(self) -> bool:
        return len(self._tools) > 0 or len(self._components) > 0 or len(self._services) > 0

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ToolRepository):
            return (
                tuple(self._tools), tuple(self._components), tuple(self._services)
            ) == (
                tuple(other._tools), tuple(other._components), tuple(other._services)
            )
        return False

    def __lt__(self, other: object) -> bool:
        if isinstance(other, ToolRepository):
            return (
                tuple(self._tools), tuple(self._components), tuple(self._services)
            ) < (
                tuple(other._tools), tuple(other._components), tuple(other._services)
            )
        return NotImplemented

    def __hash__(self) -> int:
        return hash((tuple(self._tools), tuple(self._components), tuple(self._services)))

    def all_as_tools(self) -> 'SortedSet[Tool]':
        """Get all tools, components, and services as Tool objects."""
        # Import here to avoid circular imports
        from .component import Component
        from .service import Service

        return SortedSet(chain(
            self.tools,
            map(Tool.from_component, self.components),
            map(Tool.from_service, self.services),
        ))
