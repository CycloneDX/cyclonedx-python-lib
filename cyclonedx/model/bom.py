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

import datetime
from typing import List
from uuid import uuid4

from .component import Component
from ..parser import BaseParser


class BomMetaData:
    """
    This is our internal representation of the metadata complex type within the CycloneDX standard.

    .. note::
        See the CycloneDX Schema for Bom metadata: https://cyclonedx.org/docs/1.3/#type_metadata
    """

    _timestamp: datetime.datetime

    def __init__(self):
        self._timestamp = datetime.datetime.now(tz=datetime.timezone.utc)

    def get_timestamp(self) -> datetime.datetime:
        """
        The date and time (in UTC) when this BomMetaData was created.

        Returns:
            `datetime.datetime` instance in UTC timezone
        """
        return self._timestamp


class Bom:
    """
    This is our internal representation of a bill-of-materials (BOM).

    You can either create a `cyclonedx.model.bom.Bom` yourself programmatically, or generate a `cyclonedx.model.bom.Bom`
    from a `cyclonedx.parser.BaseParser` implementation.

    Once you have an instance of `cyclonedx.model.bom.Bom`, you can pass this to an instance of
    `cyclonedx.output.BaseOutput` to produce a CycloneDX document according to a specific schema version and format.
    """

    _uuid: str
    _metadata: BomMetaData = None
    _components: List[Component] = []

    @staticmethod
    def from_parser(parser: BaseParser):
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

    def __init__(self):
        """
        Create a new Bom that you can manually/programmatically add data to later.

        Returns:
            New, empty `cyclonedx.model.bom.Bom` instance.
        """
        self._uuid = uuid4()
        self._metadata = BomMetaData()
        self._components.clear()

    def add_component(self, component: Component):
        """
        Add a Component to this Bom instance.

        Args:
            component:
                `cyclonedx.model.component.Component` instance to add to this Bom.

        Returns:
            None
        """
        self._components.append(component)

    def add_components(self, components: List[Component]):
        """
        Add multiple Components at once to this Bom instance.

        Args:
            components:
                List of `cyclonedx.model.component.Component` instances to add to this Bom.

        Returns:
            None
        """
        self._components = self._components + components

    def component_count(self) -> int:
        """
        Returns the current count of Components within this Bom.

        Returns:
             The number of Components in this Bom as `int`.
        """
        return len(self._components)

    def get_components(self) -> List[Component]:
        """
        Get all the Components currently in this Bom.

        Returns:
             List of all Components in this Bom.
        """
        return self._components

    def get_metadata(self) -> BomMetaData:
        """
        Get our internal metadata object for this Bom.

        Returns:
            Metadata object instance for this Bom.

        .. note::
            See the CycloneDX Schema for Bom metadata: https://cyclonedx.org/docs/1.3/#type_metadata
        """
        return self._metadata

    def get_urn_uuid(self) -> str:
        """
        Get the unique reference for this Bom.

        Returns:
            URN formatted UUID that uniquely identified this Bom instance.
        """
        return 'urn:uuid:{}'.format(self._uuid)

    def has_component(self, component: Component) -> bool:
        """
        Check whether this Bom contains the provided Component.

        Args:
            component:
                The instance of `cyclonedx.model.component.Component` to check if this Bom contains.

        Returns:
            `bool` - `True` if the supplied Component is part of this Bom, `False` otherwise.
        """
        return component in self._components

    def has_vulnerabilities(self) -> bool:
        """
        Check whether this Bom has any declared vulnerabilities.

        Returns:
            `bool` - `True` if at least one `cyclonedx.model.component.Component` has at least one Vulnerability,
                `False` otherwise.
        """
        for c in self.get_components():
            if c.has_vulnerabilities():
                return True

        return False
