# encoding: utf-8

# This file is part of CycloneDX Python Lib
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
import warnings
from datetime import datetime
from typing import TYPE_CHECKING, Iterable, Optional, Set
from uuid import UUID, uuid4

import serializable
from sortedcontainers import SortedSet

from cyclonedx.serialization import UrnUuidHelper

from ..exception.model import UnknownComponentDependencyException
from ..parser import BaseParser
from ..schema.schema import (
    SchemaVersion1Dot0,
    SchemaVersion1Dot1,
    SchemaVersion1Dot2,
    SchemaVersion1Dot3,
    SchemaVersion1Dot4,
)
from . import (
    ExternalReference,
    LicenseChoice,
    OrganizationalContact,
    OrganizationalEntity,
    Property,
    ThisTool,
    Tool,
    get_now_utc,
)
from .bom_ref import BomRef
from .component import Component
from .dependency import Dependable, Dependency
from .service import Service
from .vulnerability import Vulnerability

if TYPE_CHECKING:
    from packageurl import PackageURL  # type:ignore[import]


@serializable.serializable_class
class BomMetaData:
    """
    This is our internal representation of the metadata complex type within the CycloneDX standard.

    .. note::
        See the CycloneDX Schema for Bom metadata: https://cyclonedx.org/docs/1.4/#type_metadata
    """

    def __init__(self, *, tools: Optional[Iterable[Tool]] = None,
                 authors: Optional[Iterable[OrganizationalContact]] = None, component: Optional[Component] = None,
                 manufacture: Optional[OrganizationalEntity] = None,
                 supplier: Optional[OrganizationalEntity] = None,
                 licenses: Optional[Iterable[LicenseChoice]] = None,
                 properties: Optional[Iterable[Property]] = None,
                 timestamp: Optional[datetime] = None) -> None:
        self.timestamp = timestamp or get_now_utc()
        self.tools = tools or []  # type: ignore
        self.authors = authors or []  # type: ignore
        self.component = component
        self.manufacture = manufacture
        self.supplier = supplier
        self.licenses = licenses or []  # type: ignore
        self.properties = properties or []  # type: ignore

        if not tools:
            self.tools.add(ThisTool)

    @property  # type: ignore[misc]
    @serializable.type_mapping(serializable.helpers.XsdDateTime)
    @serializable.xml_sequence(1)
    def timestamp(self) -> datetime:
        """
        The date and time (in UTC) when this BomMetaData was created.

        Returns:
            `datetime` instance in UTC timezone
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: datetime) -> None:
        self._timestamp = timestamp

    @property  # type: ignore[misc]
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'tool')
    @serializable.xml_sequence(2)
    def tools(self) -> "SortedSet[Tool]":
        """
        Tools used to create this BOM.

        Returns:
            `Set` of `Tool` objects.
        """
        return self._tools

    @tools.setter
    def tools(self, tools: Iterable[Tool]) -> None:
        self._tools = SortedSet(tools)

    @property  # type: ignore[misc]
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'author')
    @serializable.xml_sequence(3)
    def authors(self) -> "SortedSet[OrganizationalContact]":
        """
        The person(s) who created the BOM.

        Authors are common in BOMs created through manual processes.

        BOMs created through automated means may not have authors.

        Returns:
            Set of `OrganizationalContact`
        """
        return self._authors

    @authors.setter
    def authors(self, authors: Iterable[OrganizationalContact]) -> None:
        self._authors = SortedSet(authors)

    @property  # type: ignore[misc]
    @serializable.xml_sequence(4)
    def component(self) -> Optional[Component]:
        """
        The (optional) component that the BOM describes.

        Returns:
            `cyclonedx.model.component.Component` instance for this Bom Metadata.
        """
        return self._component

    @component.setter
    def component(self, component: Component) -> None:
        """
        The (optional) component that the BOM describes.

        Args:
            component
                `cyclonedx.model.component.Component` instance to add to this Bom Metadata.

        Returns:
            None
        """
        self._component = component

    @property  # type: ignore[misc]
    @serializable.xml_sequence(5)
    def manufacture(self) -> Optional[OrganizationalEntity]:
        """
        The organization that manufactured the component that the BOM describes.

        Returns:
            `OrganizationalEntity` if set else `None`
        """
        return self._manufacture

    @manufacture.setter
    def manufacture(self, manufacture: Optional[OrganizationalEntity]) -> None:
        self._manufacture = manufacture

    @property  # type: ignore[misc]
    @serializable.xml_sequence(6)
    def supplier(self) -> Optional[OrganizationalEntity]:
        """
        The organization that supplied the component that the BOM describes.

        The supplier may often be the manufacturer, but may also be a distributor or repackager.

        Returns:
            `OrganizationalEntity` if set else `None`
        """
        return self._supplier

    @supplier.setter
    def supplier(self, supplier: Optional[OrganizationalEntity]) -> None:
        self._supplier = supplier

    @property  # type: ignore[misc]
    @serializable.view(SchemaVersion1Dot3)
    @serializable.view(SchemaVersion1Dot4)
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'licenses')
    @serializable.xml_sequence(7)
    def licenses(self) -> "SortedSet[LicenseChoice]":
        """
        A optional list of statements about how this BOM is licensed.

        Returns:
            Set of `LicenseChoice`
        """
        return self._licenses

    @licenses.setter
    def licenses(self, licenses: Iterable[LicenseChoice]) -> None:
        self._licenses = SortedSet(licenses)

    @property  # type: ignore[misc]
    @serializable.view(SchemaVersion1Dot3)
    @serializable.view(SchemaVersion1Dot4)
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'property')
    @serializable.xml_sequence(8)
    def properties(self) -> "SortedSet[Property]":
        """
        Provides the ability to document properties in a key/value store. This provides flexibility to include data not
        officially supported in the standard without having to use additional namespaces or create extensions.

        Property names of interest to the general public are encouraged to be registered in the CycloneDX Property
        Taxonomy - https://github.com/CycloneDX/cyclonedx-property-taxonomy. Formal registration is OPTIONAL.

        Return:
            Set of `Property`
        """
        return self._properties

    @properties.setter
    def properties(self, properties: Iterable[Property]) -> None:
        self._properties = SortedSet(properties)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BomMetaData):
            return hash(other) == hash(self)
        return False

    def __hash__(self) -> int:
        return hash((
            tuple(self.authors), self.component, tuple(self.licenses), self.manufacture, tuple(self.properties),
            self.supplier, self.timestamp, tuple(self.tools)
        ))

    def __repr__(self) -> str:
        return f'<BomMetaData timestamp={self.timestamp}, component={self.component}>'


@serializable.serializable_class(
    ignore_during_deserialization=['$schema', 'bom_format', 'spec_version'])  # type: ignore[misc]
class Bom:
    """
    This is our internal representation of a bill-of-materials (BOM).

    You can either create a `cyclonedx.model.bom.Bom` yourself programmatically, or generate a `cyclonedx.model.bom.Bom`
    from a `cyclonedx.parser.BaseParser` implementation.

    Once you have an instance of `cyclonedx.model.bom.Bom`, you can pass this to an instance of
    `cyclonedx.output.BaseOutput` to produce a CycloneDX document according to a specific schema version and format.

    @todo: Handle different Spec Versions during (de-)serialization
    @todo: Support dependencies during (de-)serialization
    """

    @staticmethod
    def from_parser(parser: BaseParser) -> 'Bom':
        """
        Create a Bom instance from a Parser object.

        Args:
            parser (`cyclonedx.parser.BaseParser`): A valid parser instance.

        Returns:
            `cyclonedx.model.bom.Bom`: A Bom instance that represents the valid data held in the supplied parser.
        """
        bom = Bom()
        bom.components.update(parser.get_components())
        return bom

    def __init__(self, *, components: Optional[Iterable[Component]] = None,
                 services: Optional[Iterable[Service]] = None,
                 external_references: Optional[Iterable[ExternalReference]] = None,
                 serial_number: Optional[UUID] = None, version: int = 1,
                 metadata: Optional[BomMetaData] = None,
                 dependencies: Optional[Iterable[Dependency]] = None,
                 vulnerabilities: Optional[Iterable[Vulnerability]] = None) -> None:
        """
        Create a new Bom that you can manually/programmatically add data to later.

        Returns:
            New, empty `cyclonedx.model.bom.Bom` instance.
        """
        self.serial_number = serial_number or uuid4()
        self.metadata = metadata or BomMetaData()
        self.components = components or []  # type: ignore
        self.services = services or []  # type: ignore
        self.external_references = SortedSet(external_references) or SortedSet()
        self.vulnerabilities = SortedSet(vulnerabilities) or SortedSet()
        self.version = version
        self.dependencies = SortedSet(dependencies) or SortedSet()

    @property  # type: ignore[misc]
    @serializable.type_mapping(UrnUuidHelper)
    @serializable.view(SchemaVersion1Dot1)
    @serializable.view(SchemaVersion1Dot2)
    @serializable.view(SchemaVersion1Dot3)
    @serializable.view(SchemaVersion1Dot4)
    @serializable.xml_attribute()
    def serial_number(self) -> UUID:
        """
        Unique UUID for this BOM

        Returns:
            `UUID` instance
            `UUID` instance
        """
        return self._serial_number

    @serial_number.setter
    def serial_number(self, serial_number: UUID) -> None:
        self._serial_number = serial_number

    @property  # type: ignore[misc]
    @serializable.view(SchemaVersion1Dot2)
    @serializable.view(SchemaVersion1Dot3)
    @serializable.view(SchemaVersion1Dot4)
    @serializable.xml_sequence(1)
    def metadata(self) -> BomMetaData:
        """
        Get our internal metadata object for this Bom.

        Returns:
            Metadata object instance for this Bom.

        .. note::
            See the CycloneDX Schema for Bom metadata: https://cyclonedx.org/docs/1.3/#type_metadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: BomMetaData) -> None:
        self._metadata = metadata

    @property  # type: ignore[misc]
    @serializable.include_none(SchemaVersion1Dot0)
    @serializable.include_none(SchemaVersion1Dot1)
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'component')
    @serializable.xml_sequence(2)
    def components(self) -> "SortedSet[Component]":
        """
        Get all the Components currently in this Bom.

        Returns:
             Set of `Component` in this Bom
        """
        return self._components

    @components.setter
    def components(self, components: Iterable[Component]) -> None:
        self._components = SortedSet(components)

    def get_component_by_purl(self, purl: Optional["PackageURL"]) -> Optional[Component]:
        """
        Get a Component already in the Bom by its PURL

        Args:
             purl:
                An instance of `packageurl.PackageURL` to look and find `Component`.

        Returns:
            `Component` or `None`
        """
        if purl:
            found = [x for x in self.components if x.purl == purl]
            if len(found) == 1:
                return found[0]

        return None

    def get_urn_uuid(self) -> str:
        """
        Get the unique reference for this Bom.

        Returns:
            URN formatted UUID that uniquely identified this Bom instance.
        """
        return self.serial_number.urn

    def has_component(self, component: Component) -> bool:
        """
        Check whether this Bom contains the provided Component.

        Args:
            component:
                The instance of `cyclonedx.model.component.Component` to check if this Bom contains.

        Returns:
            `bool` - `True` if the supplied Component is part of this Bom, `False` otherwise.
        """
        return component in self.components

    @property  # type: ignore[misc]
    @serializable.view(SchemaVersion1Dot2)
    @serializable.view(SchemaVersion1Dot3)
    @serializable.view(SchemaVersion1Dot4)
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'service')
    @serializable.xml_sequence(3)
    def services(self) -> "SortedSet[Service]":
        """
        Get all the Services currently in this Bom.

        Returns:
             Set of `Service` in this BOM
        """
        return self._services

    @services.setter
    def services(self, services: Iterable[Service]) -> None:
        self._services = SortedSet(services)

    @property  # type: ignore[misc]
    @serializable.view(SchemaVersion1Dot1)
    @serializable.view(SchemaVersion1Dot2)
    @serializable.view(SchemaVersion1Dot3)
    @serializable.view(SchemaVersion1Dot4)
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'reference')
    @serializable.xml_sequence(4)
    def external_references(self) -> "SortedSet[ExternalReference]":
        """
        Provides the ability to document external references related to the BOM or to the project the BOM describes.

        Returns:
            Set of `ExternalReference`
        """
        return self._external_references

    @external_references.setter
    def external_references(self, external_references: Iterable[ExternalReference]) -> None:
        self._external_references = SortedSet(external_references)

    def _get_all_components(self) -> Set[Component]:
        components: Set[Component] = set()
        if self.metadata.component:
            components.update(self.metadata.component.get_all_nested_components(include_self=True))

        # Add Components and sub Components
        for c in self.components:
            components.update(c.get_all_nested_components(include_self=True))

        return components

    def get_vulnerabilities_for_bom_ref(self, bom_ref: BomRef) -> "SortedSet[Vulnerability]":
        """
        Get all known Vulnerabilities that affect the supplied bom_ref.

        Args:
            bom_ref: `BomRef`

        Returns:
            `SortedSet` of `Vulnerability`
        """

        vulnerabilities: SortedSet[Vulnerability] = SortedSet()
        for v in self.vulnerabilities:
            for target in v.affects:
                if target.ref == bom_ref.value:
                    vulnerabilities.add(v)
        return vulnerabilities

    def has_vulnerabilities(self) -> bool:
        """
        Check whether this Bom has any declared vulnerabilities.

        Returns:
            `bool` - `True` if this Bom has at least one Vulnerability, `False` otherwise.
        """
        return bool(self.vulnerabilities)

    @property  # type: ignore[misc]
    @serializable.view(SchemaVersion1Dot4)
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'vulnerability')
    @serializable.xml_sequence(8)
    def vulnerabilities(self) -> "SortedSet[Vulnerability]":
        """
        Get all the Vulnerabilities in this BOM.

        Returns:
             Set of `Vulnerability`
        """
        return self._vulnerabilities

    @vulnerabilities.setter
    def vulnerabilities(self, vulnerabilities: Iterable[Vulnerability]) -> None:
        self._vulnerabilities = SortedSet(vulnerabilities)

    @property  # type: ignore[misc]
    @serializable.xml_attribute()
    def version(self) -> int:
        return self._version

    @version.setter
    def version(self, version: int) -> None:
        self._version = version

    @property  # type: ignore[misc]
    @serializable.view(SchemaVersion1Dot2)
    @serializable.view(SchemaVersion1Dot3)
    @serializable.view(SchemaVersion1Dot4)
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'dependency')
    @serializable.xml_sequence(5)
    def dependencies(self) -> "SortedSet[Dependency]":
        return self._dependencies

    @dependencies.setter
    def dependencies(self, dependencies: Iterable[Dependency]) -> None:
        self._dependencies = SortedSet(dependencies)

    def register_dependency(self, target: Dependable, depends_on: Optional[Iterable[Dependable]] = None) -> None:
        _d = next(filter(lambda _d: _d.ref == target.bom_ref, self.dependencies), None)

        if _d and depends_on:
            # Dependency Target already registered - but it might have new dependencies to add
            _d.dependencies = _d.dependencies.union(  # type: ignore
                set(map(lambda _d: Dependency(ref=_d.bom_ref), depends_on)) if depends_on else []
            )
        elif not _d:
            # First time we are seeing this target as a Dependency
            self._dependencies.add(Dependency(
                ref=target.bom_ref,
                dependencies=list(map(lambda _dep: Dependency(ref=_dep.bom_ref), depends_on)) if depends_on else []
            ))

        # Ensure dependents are registered with no further dependents in the Dependency Graph as per CDX specification
        for _d2 in depends_on if depends_on else []:
            self.register_dependency(target=_d2, depends_on=None)

    def urn(self) -> str:
        return f'urn:cdx:{self.serial_number}/{self.version}'

    def validate(self) -> bool:
        """
        Perform data-model level validations to make sure we have some known data integrity prior to attempting output
        of this `Bom`

        Returns:
             `bool`
        """
        # 0. Make sure all Dependable have a Dependency entry
        if self.metadata.component:
            self.register_dependency(target=self.metadata.component)
        for _c in self.components:
            self.register_dependency(target=_c)
        for _s in self.services:
            self.register_dependency(target=_s)

        # 1. Make sure dependencies are all in this Bom.
        all_bom_refs = set(map(lambda c: c.bom_ref, self._get_all_components())) | set(
            map(lambda s: s.bom_ref, self.services))
        all_dependency_bom_refs = set().union(*(d.dependencies_as_bom_refs() for d in self.dependencies))

        dependency_diff = all_dependency_bom_refs - all_bom_refs
        if len(dependency_diff) > 0:
            raise UnknownComponentDependencyException(
                f'One or more Components have Dependency references to Components/Services that are not known in this '
                f'BOM. They are: {dependency_diff}')

        # 2. Dependencies should exist for the Component this BOM is describing, if one is set
        if self.metadata.component and filter(
            lambda _d: _d.ref == self.metadata.component.bom_ref, self.dependencies  # type: ignore[arg-type]
        ):
            warnings.warn(
                f'The Component this BOM is describing {self.metadata.component.purl} has no defined dependencies '
                f'which means the Dependency Graph is incomplete - you should add direct dependencies to this Component'
                f'to complete the Dependency Graph data.',
                UserWarning
            )

        return True

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Bom):
            return hash(other) == hash(self)
        return False

    def __hash__(self) -> int:
        return hash((
            self.serial_number, self.version, self.metadata, tuple(self.components), tuple(self.services),
            tuple(self.external_references), tuple(self.vulnerabilities), tuple(self.dependencies)
        ))

    def __repr__(self) -> str:
        return f'<Bom uuid={self.serial_number}, hash={hash(self)}>'
