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
from datetime import datetime, timezone
from typing import Iterable, Optional, Set
from uuid import uuid4, UUID

from . import ExternalReference, ThisTool, Tool
from .component import Component
from .service import Service
from ..parser import BaseParser


class BomMetaData:
    """
    This is our internal representation of the metadata complex type within the CycloneDX standard.

    .. note::
        See the CycloneDX Schema for Bom metadata: https://cyclonedx.org/docs/1.3/#type_metadata
    """

    def __init__(self, *, tools: Optional[Iterable[Tool]] = None) -> None:
        self.timestamp = datetime.now(tz=timezone.utc)
        self.tools = set(tools or [])

        if not self.tools:
            self.tools.add(ThisTool)

        self.component: Optional[Component] = None

    @property
    def tools(self) -> Set[Tool]:
        """
        Tools used to create this BOM.

        Returns:
            `Set` of `Tool` objects.
        """
        return self._tools

    @tools.setter
    def tools(self, tools: Iterable[Tool]) -> None:
        self._tools = set(tools)

    @property
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

    @property
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

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BomMetaData):
            return hash(other) == hash(self)
        return False

    def __hash__(self) -> int:
        return hash((
            self.timestamp, self.tools, self.component
        ))

    def __repr__(self) -> str:
        return f'<BomMetaData timestamp={self.timestamp.utcnow()}>'


class Bom:
    """
    This is our internal representation of a bill-of-materials (BOM).

    You can either create a `cyclonedx.model.bom.Bom` yourself programmatically, or generate a `cyclonedx.model.bom.Bom`
    from a `cyclonedx.parser.BaseParser` implementation.

    Once you have an instance of `cyclonedx.model.bom.Bom`, you can pass this to an instance of
    `cyclonedx.output.BaseOutput` to produce a CycloneDX document according to a specific schema version and format.
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
                 external_references: Optional[Iterable[ExternalReference]] = None) -> None:
        """
        Create a new Bom that you can manually/programmatically add data to later.

        Returns:
            New, empty `cyclonedx.model.bom.Bom` instance.
        """
        self.uuid = uuid4()
        self.metadata = BomMetaData()
        self.components = set(components or [])
        self.services = set(services or [])
        self.external_references = set(external_references or [])

    @property
    def uuid(self) -> UUID:
        """
        Unique UUID for this BOM

        Returns:
            `UUID` instance
        """
        return self.__uuid

    @uuid.setter
    def uuid(self, uuid: UUID) -> None:
        self.__uuid = uuid

    @property
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

    @property
    def components(self) -> Set[Component]:
        """
        Get all the Components currently in this Bom.

        Returns:
             Set of `Component` in this Bom
        """
        return self._components

    @components.setter
    def components(self, components: Iterable[Component]) -> None:
        self._components = set(components)

    def component_count(self) -> int:
        """
        Returns the current count of Components within this Bom.

        Returns:
             The number of Components in this BOM as `int`.
        """
        return len(self.components)

    def get_component_by_purl(self, purl: Optional[str]) -> Optional[Component]:
        """
        Get a Component already in the Bom by its PURL

        Args:
             purl:
                Package URL as a `str` to look and find `Component`

        Returns:
            `Component` or `None`
        """
        if purl:
            found = list(filter(lambda x: x.purl == purl, self.components))
            if len(found) == 1:
                return found[0]

        return None

    def get_urn_uuid(self) -> str:
        """
        Get the unique reference for this Bom.

        Returns:
            URN formatted UUID that uniquely identified this Bom instance.
        """
        return 'urn:uuid:{}'.format(self.__uuid)

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

    @property
    def services(self) -> Set[Service]:
        """
        Get all the Services currently in this Bom.

        Returns:
             Set of `Service` in this BOM
        """
        return self._services

    @services.setter
    def services(self, services: Iterable[Service]) -> None:
        self._services = set(services)

    def has_service(self, service: Service) -> bool:
        """
        Check whether this Bom contains the provided Service.

        Args:
            service:
                The instance of `cyclonedx.model.service.Service` to check if this Bom contains.

        Returns:
            `bool` - `True` if the supplied Service is part of this Bom, `False` otherwise.
        """
        return service in self.services

    def service_count(self) -> int:
        """
        Returns the current count of Services within this Bom.

        Returns:
             The number of Services in this Bom as `int`.
        """
        return len(self.services)

    @property
    def external_references(self) -> Set[ExternalReference]:
        """
        Provides the ability to document external references related to the BOM or to the project the BOM describes.

        Returns:
            Set of `ExternalReference`
        """
        return self._external_references

    @external_references.setter
    def external_references(self, external_references: Iterable[ExternalReference]) -> None:
        self._external_references = set(external_references)

    def has_vulnerabilities(self) -> bool:
        """
        Check whether this Bom has any declared vulnerabilities.

        Returns:
            `bool` - `True` if at least one `cyclonedx.model.component.Component` has at least one Vulnerability,
                `False` otherwise.
        """
        return any(c.has_vulnerabilities() for c in self.components)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Bom):
            return hash(other) == hash(self)
        return False

    def __hash__(self) -> int:
        return hash((
            self.uuid, self.metadata, tuple(self.components), tuple(self.services), tuple(self.external_references)
        ))

    def __repr__(self) -> str:
        return f'<Bom uuid={self.uuid}>'
