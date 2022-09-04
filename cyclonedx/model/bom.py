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
from typing import Iterable, Optional, Set
from uuid import UUID, uuid4

from sortedcontainers import SortedSet

from ..exception.model import UnknownComponentDependencyException
from ..parser import BaseParser
from . import ExternalReference
from .bom_meta import BomMetaData
from .component import Component
from .service import Service


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
        bom.metadata.update(parser.get_metadata())
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
        self.components = components or []  # type: ignore
        self.services = services or []  # type: ignore
        self.external_references = external_references or []  # type: ignore

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

    @property
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

        for c in self.components:
            components.update(c.get_all_nested_components(include_self=True))

        return components

    def has_vulnerabilities(self) -> bool:
        """
        Check whether this Bom has any declared vulnerabilities.

        Returns:
            `bool` - `True` if at least one `cyclonedx.model.component.Component` has at least one Vulnerability,
                `False` otherwise.
        """
        return any(c.has_vulnerabilities() for c in self.components)

    def validate(self) -> bool:
        """
        Perform data-model level validations to make sure we have some known data integrity prior to attempting output
        of this `Bom`

        Returns:
             `bool`
        """

        # 1. Make sure dependencies are all in this Bom.
        all_bom_refs = set(map(lambda c: c.bom_ref, self._get_all_components())) | set(
            map(lambda s: s.bom_ref, self.services))

        all_dependency_bom_refs = set().union(*(c.dependencies for c in self.components))
        dependency_diff = all_dependency_bom_refs - all_bom_refs
        if len(dependency_diff) > 0:
            raise UnknownComponentDependencyException(
                f'One or more Components have Dependency references to Components/Services that are not known in this '
                f'BOM. They are: {dependency_diff}')

        # 2. Dependencies should exist for the Component this BOM is describing, if one is set
        if self.metadata.component and not self.metadata.component.dependencies:
            warnings.warn(
                f'The Component this BOM is describing (PURL={self.metadata.component.purl}) has no defined '
                f'dependencies which means the Dependency Graph is incomplete - you should add direct dependencies to '
                f'this Component to complete the Dependency Graph data.',
                UserWarning
            )

        return True

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
