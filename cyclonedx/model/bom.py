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
from typing import cast, List, Optional
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

    def __init__(self, tools: Optional[List[Tool]] = None) -> None:
        self.timestamp = datetime.now(tz=timezone.utc)
        self.tools = tools if tools else []

        if not self.tools:
            self.add_tool(ThisTool)

        self.component: Optional[Component] = None

    @property
    def tools(self) -> List[Tool]:
        """
        Tools used to create this BOM.

        Returns:
            `List` of `Tool` objects where there are any, else an empty `List`.
        """
        return self._tools

    @tools.setter
    def tools(self, tools: List[Tool]) -> None:
        self._tools = tools

    def add_tool(self, tool: Tool) -> None:
        """
        Add a Tool definition to this Bom Metadata. The `cyclonedx-python-lib` is automatically added - you do not need
        to add this yourself.

        Args:
            tool:
                Instance of `Tool` that represents the tool you are using.
        """
        self._tools.append(tool)

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
            self.timestamp,
            tuple([hash(tool) for tool in set(sorted(self.tools, key=hash))]) if self.tools else None,
            hash(self.component)
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
        bom.add_components(parser.get_components())
        return bom

    def __init__(self, components: Optional[List[Component]] = None, services: Optional[List[Service]] = None,
                 external_references: Optional[List[ExternalReference]] = None) -> None:
        """
        Create a new Bom that you can manually/programmatically add data to later.

        Returns:
            New, empty `cyclonedx.model.bom.Bom` instance.
        """
        self.uuid = uuid4()
        self.metadata = BomMetaData()
        self.components = components
        self.services = services
        self.external_references = external_references

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
    def components(self) -> Optional[List[Component]]:
        """
        Get all the Components currently in this Bom.

        Returns:
             List of all Components in this Bom or `None`
        """
        return self._components

    @components.setter
    def components(self, components: Optional[List[Component]]) -> None:
        self._components = components

    def add_component(self, component: Component) -> None:
        """
        Add a Component to this Bom instance.

        Args:
            component:
                `cyclonedx.model.component.Component` instance to add to this Bom.

        Returns:
            None
        """
        if not self.components:
            self.components = [component]
        elif not self.has_component(component=component):
            self.components.append(component)

    def add_components(self, components: List[Component]) -> None:
        """
        Add multiple Components at once to this Bom instance.

        Args:
            components:
                List of `cyclonedx.model.component.Component` instances to add to this Bom.

        Returns:
            None
        """
        self.components = (self._components or []) + components

    def component_count(self) -> int:
        """
        Returns the current count of Components within this Bom.

        Returns:
             The number of Components in this Bom as `int`.
        """
        return len(self._components) if self._components else 0

    def get_component_by_purl(self, purl: Optional[str]) -> Optional[Component]:
        """
        Get a Component already in the Bom by it's PURL

        Args:
             purl:
                Package URL as a `str` to look and find `Component`

        Returns:
            `Component` or `None`
        """
        if not self._components:
            return None

        if purl:
            found = list(filter(lambda x: x.purl == purl, cast(List[Component], self.components)))
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
        if not self.components:
            return False
        return component in self.components

    @property
    def services(self) -> Optional[List[Service]]:
        """
        Get all the Services currently in this Bom.

        Returns:
             List of `Service` in this Bom or `None`
        """
        return self._services

    @services.setter
    def services(self, services: Optional[List[Service]]) -> None:
        self._services = services

    def add_service(self, service: Service) -> None:
        """
        Add a Service to this Bom instance.

        Args:
            service:
                `cyclonedx.model.service.Service` instance to add to this Bom.

        Returns:
            None
        """
        if not self.services:
            self.services = [service]
        elif not self.has_service(service=service):
            self.services.append(service)

    def add_services(self, services: List[Service]) -> None:
        """
        Add multiple Services at once to this Bom instance.

        Args:
            services:
                List of `cyclonedx.model.service.Service` instances to add to this Bom.

        Returns:
            None
        """
        self.services = (self.services or []) + services

    def has_service(self, service: Service) -> bool:
        """
        Check whether this Bom contains the provided Service.

        Args:
            service:
                The instance of `cyclonedx.model.service.Service` to check if this Bom contains.

        Returns:
            `bool` - `True` if the supplied Service is part of this Bom, `False` otherwise.
        """
        if not self.services:
            return False

        return service in self.services

    def service_count(self) -> int:
        """
        Returns the current count of Services within this Bom.

        Returns:
             The number of Services in this Bom as `int`.
        """
        if not self.services:
            return 0

        return len(self.services)

    @property
    def external_references(self) -> Optional[List[ExternalReference]]:
        """
        Provides the ability to document external references related to the BOM or to the project the BOM describes.

        Returns:
            List of `ExternalReference` else `None`
        """
        return self._external_references

    @external_references.setter
    def external_references(self, external_references: Optional[List[ExternalReference]]) -> None:
        self._external_references = external_references

    def add_external_reference(self, external_reference: ExternalReference) -> None:
        """
        Add an external reference to this Bom.

        Args:
            external_reference:
                `ExternalReference` to add to this Bom.

        Returns:
            None
        """
        self.external_references = (self.external_references or []) + [external_reference]

    def has_vulnerabilities(self) -> bool:
        """
        Check whether this Bom has any declared vulnerabilities.

        Returns:
            `bool` - `True` if at least one `cyclonedx.model.component.Component` has at least one Vulnerability,
                `False` otherwise.
        """
        if self.components:
            for c in self.components:
                if c.has_vulnerabilities():
                    return True

        return False

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Bom):
            return hash(other) == hash(self)
        return False

    def __hash__(self) -> int:
        return hash((
            self.uuid, hash(self.metadata),
            tuple([hash(c) for c in set(sorted(self.components, key=hash))]) if self.components else None,
            tuple([hash(s) for s in set(sorted(self.services, key=hash))]) if self.services else None
        ))

    def __repr__(self) -> str:
        return f'<Bom uuid={self.uuid}>'
