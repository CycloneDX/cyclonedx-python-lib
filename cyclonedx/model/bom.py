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


from collections.abc import Generator, Iterable
from datetime import datetime
from enum import Enum
from itertools import chain
from typing import TYPE_CHECKING, Any, Optional, Union
from uuid import UUID, uuid4
from warnings import warn

from attrs import Factory, define, field
from sortedcontainers import SortedSet

from .._internal.compare import ComparableTuple as _ComparableTuple
from .._internal.time import get_now_utc as _get_now_utc
from ..exception.model import LicenseExpressionAlongWithOthersException, UnknownComponentDependencyException
from ..schema import SchemaVersion
from . import _BOM_LINK_PREFIX, ExternalReference, Property
from .bom_ref import BomRef
from .component import Component
from .contact import OrganizationalContact, OrganizationalEntity
from .definition import Definitions
from .dependency import Dependable, Dependency
from .license import License, LicenseExpression, LicenseRepository
from .lifecycle import Lifecycle, LifecycleRepository
from .service import Service
from .tool import Tool, ToolRepository
from .vulnerability import Vulnerability

if TYPE_CHECKING:  # pragma: no cover
    from packageurl import PackageURL


def _sortedset_converter(value: Any) -> SortedSet:
    if value is None:
        return SortedSet()
    if isinstance(value, SortedSet):
        return value
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes, dict)):
        return SortedSet(value)
    return SortedSet([value])


def _license_repository_converter(value: Any) -> 'LicenseRepository':
    if value is None:
        return LicenseRepository()
    if isinstance(value, LicenseRepository):
        return value
    # Convert generators, lists, etc. to LicenseRepository
    return LicenseRepository(value)


def _lifecycle_repository_converter(value: Any) -> 'LifecycleRepository':
    if value is None:
        return LifecycleRepository()
    if isinstance(value, LifecycleRepository):
        return value
    # Convert generators, lists, etc. to LifecycleRepository
    return LifecycleRepository(value)


class TlpClassification(str, Enum):
    """
    Enum object that defines the Traffic Light Protocol (TLP) classification that controls the sharing and distribution
    of the data that the BOM describes.

    .. note::
        Introduced in CycloneDX v1.7

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_tlpClassificationType
    """

    CLEAR = 'CLEAR'
    GREEN = 'GREEN'
    AMBER = 'AMBER'
    AMBER_AND_STRICT = 'AMBER_AND_STRICT'
    RED = 'RED'


@define
class DistributionConstraints:
    """
    Our internal representation of the `distributionConstraints` complex type.
    Conditions and constraints governing the sharing and distribution of the data or components described by this BOM.

    .. note::
        Introduced in CycloneDX v1.7

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_metadata
    """

    tlp: TlpClassification = field(
        default=TlpClassification.CLEAR,
        metadata={'json_name': 'tlp', 'xml_name': 'tlp', 'xml_sequence': 0,
                  'min_schema_version': SchemaVersion.V1_7}
    )
    """
    The Traffic Light Protocol (TLP) classification that controls the sharing and distribution of the data that the
    BOM describes.
    """

    def __hash__(self) -> int:
        return hash(self.tlp)

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, DistributionConstraints):
            return self.tlp < other.tlp
        return NotImplemented


@define
class BomMetaData:
    """
    This is our internal representation of the metadata complex type within the CycloneDX standard.

    .. note::
        See the CycloneDX Schema for Bom metadata: https://cyclonedx.org/docs/1.7/xml/#type_metadata
    """

    timestamp: datetime = field(
        factory=_get_now_utc,
        metadata={'json_name': 'timestamp', 'xml_name': 'timestamp', 'xml_sequence': 1}
    )
    """The date and time (in UTC) when this BomMetaData was created."""

    _lifecycles: LifecycleRepository = field(
        factory=LifecycleRepository,
        converter=_lifecycle_repository_converter,
        metadata={'json_name': 'lifecycles', 'xml_name': 'lifecycles', 'xml_sequence': 2,
                  'min_schema_version': SchemaVersion.V1_5}
    )
    """An optional list of BOM lifecycle stages."""

    _tools: ToolRepository = field(
        factory=ToolRepository,
        converter=lambda v: v if isinstance(v, ToolRepository) else ToolRepository(tools=v) if v else ToolRepository(),
        metadata={'json_name': 'tools', 'xml_name': 'tools', 'xml_sequence': 3}
    )
    """Tools used to create this BOM."""

    _authors: 'SortedSet[OrganizationalContact]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'authors', 'xml_name': 'authors', 'xml_item_name': 'author', 'xml_sequence': 4}
    )
    """The person(s) who created the BOM."""

    component: Optional[Component] = field(
        default=None,
        metadata={'json_name': 'component', 'xml_name': 'component', 'xml_sequence': 5}
    )
    """The (optional) component that the BOM describes."""

    _manufacture: Optional[OrganizationalEntity] = field(
        default=None,
        metadata={'json_name': 'manufacture', 'xml_name': 'manufacture', 'xml_sequence': 6,
                  'min_schema_version': SchemaVersion.V1_2, 'max_schema_version': SchemaVersion.V1_7}
    )
    """The organization that manufactured the component that the BOM describes."""

    manufacturer: Optional[OrganizationalEntity] = field(
        default=None,
        metadata={'json_name': 'manufacturer', 'xml_name': 'manufacturer', 'xml_sequence': 7,
                  'min_schema_version': SchemaVersion.V1_6}
    )
    """The organization that created the BOM."""

    supplier: Optional[OrganizationalEntity] = field(
        default=None,
        metadata={'json_name': 'supplier', 'xml_name': 'supplier', 'xml_sequence': 8}
    )
    """The organization that supplied the component that the BOM describes."""

    _licenses: LicenseRepository = field(
        factory=LicenseRepository,
        converter=_license_repository_converter,
        metadata={'json_name': 'licenses', 'xml_name': 'licenses', 'xml_sequence': 9,
                  'min_schema_version': SchemaVersion.V1_3}
    )
    """A optional list of statements about how this BOM is licensed."""

    _properties: 'SortedSet[Property]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'properties', 'xml_name': 'properties', 'xml_item_name': 'property', 'xml_sequence': 10,
                  'min_schema_version': SchemaVersion.V1_3}
    )
    """Provides the ability to document properties in a key/value store."""

    distribution_constraints: Optional[DistributionConstraints] = field(
        default=None,
        metadata={'json_name': 'distributionConstraints', 'xml_name': 'distributionConstraints', 'xml_sequence': 11,
                  'min_schema_version': SchemaVersion.V1_7}
    )
    """Conditions and constraints governing the sharing and distribution of the data."""

    @property
    def lifecycles(self) -> LifecycleRepository:
        """An optional list of BOM lifecycle stages."""
        return self._lifecycles

    @lifecycles.setter
    def lifecycles(self, lifecycles: Iterable[Lifecycle]) -> None:
        self._lifecycles = LifecycleRepository(lifecycles)

    @property
    def tools(self) -> ToolRepository:
        """Tools used to create this BOM."""
        return self._tools

    @tools.setter
    def tools(self, tools: Union[Iterable[Tool], ToolRepository]) -> None:
        self._tools = tools if isinstance(tools, ToolRepository) else ToolRepository(tools=tools)

    @property
    def authors(self) -> 'SortedSet[OrganizationalContact]':
        """The person(s) who created the BOM."""
        return self._authors

    @authors.setter
    def authors(self, authors: Iterable[OrganizationalContact]) -> None:
        self._authors = SortedSet(authors)

    @property
    def manufacture(self) -> Optional[OrganizationalEntity]:
        """The organization that manufactured the component that the BOM describes (deprecated)."""
        return self._manufacture

    @manufacture.setter
    def manufacture(self, manufacture: Optional[OrganizationalEntity]) -> None:
        if manufacture is not None:
            warn(
                '`bom.metadata.manufacture` is deprecated from CycloneDX v1.6 onwards. '
                'Please use `bom.metadata.component.manufacturer` instead.',
                DeprecationWarning)
        self._manufacture = manufacture

    @property
    def licenses(self) -> LicenseRepository:
        """A optional list of statements about how this BOM is licensed."""
        return self._licenses

    @licenses.setter
    def licenses(self, licenses: Iterable[License]) -> None:
        self._licenses = LicenseRepository(licenses)

    @property
    def properties(self) -> 'SortedSet[Property]':
        """Provides the ability to document properties in a key/value store."""
        return self._properties

    @properties.setter
    def properties(self, properties: Iterable[Property]) -> None:
        self._properties = SortedSet(properties)

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((
            _ComparableTuple(self.authors), self.component, _ComparableTuple(self.licenses), self.manufacture,
            _ComparableTuple(self.properties), self.distribution_constraints,
            _ComparableTuple(self.lifecycles), self.supplier, self.timestamp, self.tools, self.manufacturer
        ))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BomMetaData):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: object) -> bool:
        if isinstance(other, BomMetaData):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())


@define
class Bom:
    """
    This is our internal representation of a bill-of-materials (BOM).

    Once you have an instance of `cyclonedx.model.bom.Bom`, you can pass this to an instance of
    `cyclonedx.output.BaseOutput` to produce a CycloneDX document according to a specific schema version and format.
    """

    serial_number: UUID = field(
        factory=uuid4,
        metadata={'json_name': 'serialNumber', 'xml_name': 'serialNumber', 'xml_attribute': True,
                  'min_schema_version': SchemaVersion.V1_1}
    )
    """Unique UUID for this BOM."""

    version: int = field(
        default=1,
        metadata={'json_name': 'version', 'xml_name': 'version', 'xml_attribute': True}
    )
    """The version of this BOM."""

    metadata: BomMetaData = field(
        factory=BomMetaData,
        metadata={'json_name': 'metadata', 'xml_name': 'metadata', 'xml_sequence': 10,
                  'min_schema_version': SchemaVersion.V1_2}
    )
    """Metadata for this BOM."""

    _components: 'SortedSet[Component]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'components', 'xml_name': 'components', 'xml_item_name': 'component',
                  'xml_sequence': 20}
    )
    """Components in this BOM."""

    _services: 'SortedSet[Service]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'services', 'xml_name': 'services', 'xml_item_name': 'service',
                  'xml_sequence': 30, 'min_schema_version': SchemaVersion.V1_2}
    )
    """Services in this BOM."""

    _external_references: 'SortedSet[ExternalReference]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'externalReferences', 'xml_name': 'externalReferences', 'xml_item_name': 'reference',
                  'xml_sequence': 40, 'min_schema_version': SchemaVersion.V1_1}
    )
    """External references related to the BOM."""

    _dependencies: 'SortedSet[Dependency]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'dependencies', 'xml_name': 'dependencies', 'xml_item_name': 'dependency',
                  'xml_sequence': 50, 'min_schema_version': SchemaVersion.V1_2}
    )
    """Dependencies in this BOM."""

    _properties: 'SortedSet[Property]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'properties', 'xml_name': 'properties', 'xml_item_name': 'property',
                  'xml_sequence': 70, 'min_schema_version': SchemaVersion.V1_5}
    )
    """Properties for this BOM."""

    _vulnerabilities: 'SortedSet[Vulnerability]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'vulnerabilities', 'xml_name': 'vulnerabilities', 'xml_item_name': 'vulnerability',
                  'xml_sequence': 80, 'min_schema_version': SchemaVersion.V1_4}
    )
    """Vulnerabilities in this BOM."""

    definitions: Optional[Definitions] = field(
        default=None,
        metadata={'json_name': 'definitions', 'xml_name': 'definitions', 'xml_sequence': 110,
                  'min_schema_version': SchemaVersion.V1_6}
    )
    """Definitions for this BOM."""

    @property
    def components(self) -> 'SortedSet[Component]':
        """Get all the Components currently in this Bom."""
        return self._components

    @components.setter
    def components(self, components: Iterable[Component]) -> None:
        self._components = SortedSet(components)

    @property
    def services(self) -> 'SortedSet[Service]':
        """Get all the Services currently in this Bom."""
        return self._services

    @services.setter
    def services(self, services: Iterable[Service]) -> None:
        self._services = SortedSet(services)

    @property
    def external_references(self) -> 'SortedSet[ExternalReference]':
        """Provides the ability to document external references related to the BOM."""
        return self._external_references

    @external_references.setter
    def external_references(self, external_references: Iterable[ExternalReference]) -> None:
        self._external_references = SortedSet(external_references)

    @property
    def dependencies(self) -> 'SortedSet[Dependency]':
        """Dependencies in this BOM."""
        return self._dependencies

    @dependencies.setter
    def dependencies(self, dependencies: Iterable[Dependency]) -> None:
        self._dependencies = SortedSet(dependencies)

    @property
    def properties(self) -> 'SortedSet[Property]':
        """Properties for this BOM."""
        return self._properties

    @properties.setter
    def properties(self, properties: Iterable[Property]) -> None:
        self._properties = SortedSet(properties)

    @property
    def vulnerabilities(self) -> 'SortedSet[Vulnerability]':
        """Get all the Vulnerabilities in this BOM."""
        return self._vulnerabilities

    @vulnerabilities.setter
    def vulnerabilities(self, vulnerabilities: Iterable[Vulnerability]) -> None:
        self._vulnerabilities = SortedSet(vulnerabilities)

    def get_component_by_purl(self, purl: Optional['PackageURL']) -> Optional[Component]:
        """
        Get a Component already in the Bom by its PURL

        Args:
             purl:
                An instance of `packageurl.PackageURL` to look and find `Component`.

        Returns:
            `Component` or `None`

        .. deprecated:: next
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

        .. deprecated:: next
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

        .. deprecated:: next
        """
        return component in self.components

    def _get_all_components(self) -> Generator[Component, None, None]:
        if self.metadata.component:
            yield from self.metadata.component.get_all_nested_components(include_self=True)
        for c in self.components:
            yield from c.get_all_nested_components(include_self=True)

    def get_vulnerabilities_for_bom_ref(self, bom_ref: BomRef) -> 'SortedSet[Vulnerability]':
        """
        Get all known Vulnerabilities that affect the supplied bom_ref.

        Args:
            bom_ref: `BomRef`

        Returns:
            `SortedSet` of `Vulnerability`

        .. deprecated:: next
            Deprecated without any replacement.
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

        .. deprecated:: next
            Deprecated without any replacement.
        """
        return bool(self.vulnerabilities)

    def register_dependency(self, target: Dependable, depends_on: Optional[Iterable[Dependable]] = None) -> None:
        _d = next(filter(lambda _d: _d.ref == target.bom_ref, self.dependencies), None)
        if _d:
            # Dependency Target already registered - but it might have new dependencies to add
            if depends_on:
                _d.dependencies.update([Dependency(ref=_d.bom_ref) for _d in depends_on])
        else:
            # First time we are seeing this target as a Dependency
            self._dependencies.add(Dependency(
                ref=target.bom_ref,
                dependencies=[Dependency(ref=_dep.bom_ref) for _dep in depends_on] if depends_on else []
            ))

        if depends_on:
            # Ensure dependents are registered with no further dependents in the DependencyGraph
            for _d2 in depends_on:
                self.register_dependency(target=_d2, depends_on=None)

    def urn(self) -> str:
        """
        .. deprecated:: next
            Deprecated without any replacement.
        """
        # idea: have 'serial_number' be a string, and use it instead of this method
        return f'{_BOM_LINK_PREFIX}{self.serial_number}/{self.version}'

    def validate(self) -> bool:
        """
        Perform data-model level validations to make sure we have some known data integrity prior to attempting output
        of this `Bom`

        Returns:
             `bool`

        .. deprecated:: next
            Deprecated without any replacement.
        """
        # !! deprecated function. have this as an part of the normalization process, like the BomRefDiscrimator
        # 0. Make sure all Dependable have a Dependency entry
        if self.metadata.component:
            self.register_dependency(target=self.metadata.component)
        for _c in self.components:
            self.register_dependency(target=_c)
        for _s in self.services:
            self.register_dependency(target=_s)

        # 1. Make sure dependencies are all in this Bom.
        component_bom_refs = set(map(lambda c: c.bom_ref, self._get_all_components())) | set(
            map(lambda s: s.bom_ref, self.services))
        dependency_bom_refs = set(chain(
            (d.ref for d in self.dependencies),
            chain.from_iterable(d.dependencies_as_bom_refs() for d in self.dependencies)
        ))
        dependency_diff = dependency_bom_refs - component_bom_refs
        if len(dependency_diff) > 0:
            raise UnknownComponentDependencyException(
                'One or more Components have Dependency references to Components/Services that are not known in this '
                f'BOM. They are: {dependency_diff}')

        # 2. if root component is set and there are other components: dependencies should exist for the Component
        # this BOM is describing
        if self.metadata.component and len(self.components) > 0 and not any(map(
            lambda d: d.ref == self.metadata.component.bom_ref and len(d.dependencies) > 0,  # type:ignore[union-attr]
            self.dependencies
        )):
            warn(
                f'The Component this BOM is describing {self.metadata.component.purl} has no defined dependencies '
                'which means the Dependency Graph is incomplete - you should add direct dependencies to this '
                '"root" Component to complete the Dependency Graph data.',
                category=UserWarning, stacklevel=1
            )

        # 3. If a LicenseExpression is set, then there must be no other license.
        # see https://github.com/CycloneDX/specification/pull/205
        elem: Union[BomMetaData, Component, Service]
        for elem in chain(  # type:ignore[assignment]
            [self.metadata],
            self.metadata.component.get_all_nested_components(include_self=True) if self.metadata.component else [],
            chain.from_iterable(c.get_all_nested_components(include_self=True) for c in self.components),
            self.services
        ):
            if len(elem.licenses) > 1 and any(isinstance(li, LicenseExpression) for li in elem.licenses):
                raise LicenseExpressionAlongWithOthersException(
                    f'Found LicenseExpression along with others licenses in: {elem!r}')

        return True

    def __hash__(self) -> int:
        return hash((
            self.serial_number, self.version, self.metadata,
            tuple(self.components), tuple(self.services),
            tuple(self.external_references), tuple(self.dependencies),
            tuple(self.properties), tuple(self.vulnerabilities),
        ))

    @classmethod
    def from_json(cls, data: Union[dict, str, bytes]) -> 'Bom':
        """
        Create a Bom from JSON data.

        Args:
            data: JSON data as a dict, string, or bytes

        Returns:
            A new Bom instance
        """
        import json

        from ..serialization import make_converter

        if isinstance(data, (str, bytes)):
            data = json.loads(data)

        # Determine schema version from data
        spec_version = data.get('specVersion', '1.4')
        version_map = {
            '1.0': SchemaVersion.V1_0,
            '1.1': SchemaVersion.V1_1,
            '1.2': SchemaVersion.V1_2,
            '1.3': SchemaVersion.V1_3,
            '1.4': SchemaVersion.V1_4,
            '1.5': SchemaVersion.V1_5,
            '1.6': SchemaVersion.V1_6,
            '1.7': SchemaVersion.V1_7,
        }
        schema_version = version_map.get(spec_version, SchemaVersion.V1_4)

        converter = make_converter(schema_version)
        return converter.structure(data, cls)

    @classmethod
    def from_xml(cls, data: Union['Element', str, bytes, Any]) -> 'Bom':
        """
        Create a Bom from XML data.

        Args:
            data: XML data as an Element, string, bytes, or file-like object

        Returns:
            A new Bom instance
        """
        from xml.etree.ElementTree import Element, fromstring, parse

        from ..serialization import make_converter

        if isinstance(data, (str, bytes)):
            data = fromstring(data)
        elif hasattr(data, 'read'):
            # Handle file-like objects
            data = parse(data).getroot()

        # Determine schema version from namespace
        ns = data.tag.split('}')[0].strip('{') if data.tag.startswith('{') else ''
        version_map = {
            'http://cyclonedx.org/schema/bom/1.0': SchemaVersion.V1_0,
            'http://cyclonedx.org/schema/bom/1.1': SchemaVersion.V1_1,
            'http://cyclonedx.org/schema/bom/1.2': SchemaVersion.V1_2,
            'http://cyclonedx.org/schema/bom/1.3': SchemaVersion.V1_3,
            'http://cyclonedx.org/schema/bom/1.4': SchemaVersion.V1_4,
            'http://cyclonedx.org/schema/bom/1.5': SchemaVersion.V1_5,
            'http://cyclonedx.org/schema/bom/1.6': SchemaVersion.V1_6,
            'http://cyclonedx.org/schema/bom/1.7': SchemaVersion.V1_7,
        }
        schema_version = version_map.get(ns, SchemaVersion.V1_4)

        # Convert XML to dict and then structure
        xml_dict = cls._xml_to_dict(data)
        converter = make_converter(schema_version)
        return converter.structure(xml_dict, cls)

    @staticmethod
    def _xml_to_dict(element: 'Element') -> dict:
        """Convert an XML element to a dictionary.

        Handles XML container patterns like <components><component>...</component></components>
        by unwrapping to arrays that match the JSON structure.
        """
        from xml.etree.ElementTree import Element

        result: dict = {}

        # Handle attributes
        for key, value in element.attrib.items():
            # Remove namespace prefix from attribute names
            if '}' in key:
                key = key.split('}')[1]
            # Convert hyphen to underscore for Python field names
            key = key.replace('-', '_')
            result[key] = value

        # Handle child elements
        for child in element:
            # Remove namespace prefix from tag names
            tag = child.tag.split('}')[1] if '}' in child.tag else child.tag

            if len(child) == 0 and not child.attrib:
                # Simple text content
                value = child.text
            else:
                # Complex element
                value = Bom._xml_to_dict(child)

            # Handle lists (multiple elements with same tag)
            if tag in result:
                if not isinstance(result[tag], list):
                    result[tag] = [result[tag]]
                result[tag].append(value)
            else:
                result[tag] = value

        # If element has only text content (no attributes, no children)
        if not result and element.text:
            return element.text  # type: ignore[return-value]

        # Handle elements with both attributes and text content
        # e.g., <text content-type="text/plain">content here</text>
        # This should produce {"content-type": "text/plain", "content": "content here"}
        if result and element.text and element.text.strip():
            # Check if there are no child elements (only attributes)
            has_child_elements = any(True for _ in element)
            if not has_child_elements:
                result['content'] = element.text

        # Unwrap XML container patterns to match JSON structure
        # e.g., {"components": {"component": [...]}} -> {"components": [...]}
        result = Bom._unwrap_xml_containers(result)

        return result

    @staticmethod
    def _unwrap_xml_containers(data: dict) -> dict:
        """Unwrap XML container patterns to match JSON structure.

        XML uses patterns like <components><component>...</component></components>
        while JSON uses direct arrays: "components": [...]

        This detects containers where the only child key is a singular form
        and unwraps them to direct arrays.
        """
        # Known container mappings (plural -> singular)
        container_mappings = {
            'components': 'component',
            'dependencies': 'dependency',
            'properties': 'property',
            'hashes': 'hash',
            'licenses': 'license',
            'externalReferences': 'reference',
            'vulnerabilities': 'vulnerability',
            'services': 'service',
            'tools': 'tool',
            'authors': 'author',
            'patches': 'patch',
            'commits': 'commit',
            'compositions': 'composition',
            'annotations': 'annotation',
            'formulation': 'formula',
            'methods': 'method',
            'identities': 'identity',
            'occurrences': 'occurrence',
            'callstack': 'frame',
            'algorithms': 'algorithm',
            'identifiers': 'identifier',
            'cipherSuites': 'cipherSuite',
            'cryptoRefArray': 'cryptoRef',
            'subjectAlternativeNames': 'name',
            'manufacturers': 'manufacturer',
            'constraints': 'constraint',
            'targets': 'target',
            'affects': 'target',
            'credits': 'organizationalContact',
            'workarounds': 'workaround',
            'references': 'reference',  # Vulnerability references use 'reference' as child
            'advisories': 'advisory',
            'ratings': 'rating',
            'cwes': 'cwe',
            'declarations': 'standards',
            # 'definitions' is a complex object, not a simple container
            # It contains 'standards' which contains 'standard' children
            'standards': 'standard',
            # Standard contains levels and requirements containers
            'levels': 'level',
            'requirements': 'requirement',
            # Requirement contains descriptions container
            'descriptions': 'description',
            # Affects target contains versions
            'versions': 'version',
            # Credits containers
            'organizations': 'organization',
            'contacts': 'contact',
            'individuals': 'individual',
            'claims': 'claim',
            'evidence': 'evidence',
            'counters': 'counter',
            'assessors': 'assessor',
            'attestations': 'attestation',
            'encr': 'ref',
            'prf': 'ref',
            'integ': 'ref',
            # Service data classifications
            'data': 'classification',
            'endpoints': 'endpoint',
            'ke': 'ref',
            'auth': 'ref',
            # Pedigree component containers
            'ancestors': 'component',
            'descendants': 'component',
            'variants': 'component',
            # Callstack frames
            'frames': 'frame',
            'parameters': 'parameter',
            # Metadata lifecycles
            'lifecycles': 'lifecycle',
            # ReleaseNotes fields
            'resolves': 'issue',
            'notes': 'note',
            'aliases': 'alias',
            'tags': 'tag',
            # Crypto fields
            'cryptoFunctions': 'cryptoFunction',
            'certificationLevel': 'certification',
            # Vulnerability analysis responses
            'responses': 'response',
        }

        # XML element names that need to be renamed to JSON names
        # When XML has elements directly (no container), we need to use the JSON name
        xml_to_json_name = {
            'cryptoRef': 'cryptoRefArray',  # <cryptoRef>...</cryptoRef> -> cryptoRefArray
            'responses': 'response',  # XML container name -> JSON field name for VulnerabilityAnalysis
        }

        unwrapped = {}
        for key, value in data.items():
            # Rename XML element names to JSON names if needed
            out_key = xml_to_json_name.get(key, key)
            if isinstance(value, dict):
                # Special handling for licenses which can contain both 'license' and 'expression'
                if key == 'licenses':
                    result: list = []
                    # Collect license children (DisjunctiveLicense)
                    if 'license' in value:
                        license_val = value['license']
                        if isinstance(license_val, list):
                            for lic in license_val:
                                if isinstance(lic, dict):
                                    result.append(Bom._unwrap_xml_containers(lic))
                                else:
                                    result.append(lic)
                        else:
                            if isinstance(license_val, dict):
                                result.append(Bom._unwrap_xml_containers(license_val))
                            else:
                                result.append(license_val)
                    # Collect expression children (LicenseExpression)
                    if 'expression' in value:
                        expr_val = value['expression']
                        if isinstance(expr_val, list):
                            for expr in expr_val:
                                # Keep the 'expression' wrapper for structuring
                                if isinstance(expr, dict):
                                    result.append({'expression': expr})
                                else:
                                    result.append({'expression': expr})
                        else:
                            # Single expression - keep the 'expression' wrapper
                            if isinstance(expr_val, dict):
                                result.append({'expression': expr_val})
                            else:
                                result.append({'expression': expr_val})
                    # If we found licenses, use the collected result
                    if result:
                        unwrapped[out_key] = result
                    else:
                        # No recognized children, pass through
                        unwrapped[out_key] = Bom._unwrap_xml_containers(value)
                    continue

                # Special handling for copyright which contains 'text' children
                # that should become Copyright objects
                if key == 'copyright' and 'text' in value:
                    text_val = value['text']
                    if isinstance(text_val, list):
                        # Multiple text elements -> list of Copyright objects
                        unwrapped[out_key] = [{'text': t} for t in text_val]
                    else:
                        # Single text element -> list with one Copyright object
                        unwrapped[out_key] = [{'text': text_val}]
                    continue

                # Special handling for references in issues - contains 'url' children
                # that should become a list of URLs (XsUri)
                if key == 'references' and 'url' in value and len(value) == 1:
                    url_val = value['url']
                    if isinstance(url_val, list):
                        unwrapped[out_key] = url_val
                    else:
                        unwrapped[out_key] = [url_val]
                    continue

                # Special handling for tools in identity - contains 'tool' with 'ref' attr
                # that should become a list of ref strings (BomRef)
                if key == 'tools' and 'tool' in value:
                    tool_val = value['tool']
                    if not isinstance(tool_val, list):
                        tool_val = [tool_val]
                    # Extract ref values from tool dicts
                    refs = []
                    for t in tool_val:
                        if isinstance(t, dict) and 'ref' in t:
                            refs.append(t['ref'])
                        elif isinstance(t, str):
                            refs.append(t)
                    if refs:
                        unwrapped[out_key] = refs
                        continue

                # Check if this is a container that should be unwrapped
                singular = container_mappings.get(key)
                if singular and singular in value and len(value) == 1:
                    # Unwrap: {"components": {"component": [...]}} -> {"components": [...]}
                    inner = value[singular]
                    # Ensure it's a list
                    if not isinstance(inner, list):
                        inner = [inner]
                    unwrapped[out_key] = inner
                else:
                    # Recursively unwrap nested structures
                    unwrapped[out_key] = Bom._unwrap_xml_containers(value)
            elif isinstance(value, list):
                # Recursively unwrap items in lists
                unwrapped[out_key] = [
                    Bom._unwrap_xml_containers(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                unwrapped[out_key] = value

        return unwrapped
