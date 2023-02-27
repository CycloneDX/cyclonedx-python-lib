# encoding: utf-8

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

from typing import Any, Iterable, Optional, Union
from uuid import uuid4

import serializable
from sortedcontainers import SortedSet

from cyclonedx.serialization import BomRefHelper

from ..schema.schema import SchemaVersion1Dot3, SchemaVersion1Dot4
from . import (
    ComparableTuple,
    DataClassification,
    ExternalReference,
    LicenseChoice,
    OrganizationalEntity,
    Property,
    XsUri,
)
from .bom_ref import BomRef
from .dependency import Dependable
from .release_note import ReleaseNotes

"""
This set of classes represents the data that is possible about known Services.

.. note::
    See the CycloneDX Schema extension definition https://cyclonedx.org/docs/1.4/xml/#type_servicesType
"""


@serializable.serializable_class
class Service(Dependable):
    """
    Class that models the `service` complex type in the CycloneDX schema.

    .. note::
        See the CycloneDX schema: https://cyclonedx.org/docs/1.4/xml/#type_service
    """

    def __init__(self, *, name: str, bom_ref: Optional[Union[str, BomRef]] = None,
                 provider: Optional[OrganizationalEntity] = None,
                 group: Optional[str] = None, version: Optional[str] = None, description: Optional[str] = None,
                 endpoints: Optional[Iterable[XsUri]] = None, authenticated: Optional[bool] = None,
                 x_trust_boundary: Optional[bool] = None, data: Optional[Iterable[DataClassification]] = None,
                 licenses: Optional[Iterable[LicenseChoice]] = None,
                 external_references: Optional[Iterable[ExternalReference]] = None,
                 properties: Optional[Iterable[Property]] = None,
                 services: Optional[Iterable['Service']] = None,
                 release_notes: Optional[ReleaseNotes] = None,
                 ) -> None:
        if type(bom_ref) == BomRef:
            self._bom_ref = bom_ref
        else:
            self._bom_ref = BomRef(value=str(bom_ref) if bom_ref else str(uuid4()))
        self.provider = provider
        self.group = group
        self.name = name
        self.version = version
        self.description = description
        self.endpoints = endpoints or []  # type: ignore
        self.authenticated = authenticated
        self.x_trust_boundary = x_trust_boundary
        self.data = data or []  # type: ignore
        self.licenses = licenses or []  # type: ignore
        self.external_references = external_references or []  # type: ignore
        self.services = services or []  # type: ignore
        self.release_notes = release_notes
        self.properties = properties or []  # type: ignore

    @property  # type: ignore[misc]
    @serializable.json_name('bom-ref')
    @serializable.type_mapping(BomRefHelper)
    @serializable.xml_attribute()
    @serializable.xml_name('bom-ref')
    def bom_ref(self) -> BomRef:
        """
        An optional identifier which can be used to reference the service elsewhere in the BOM. Uniqueness is enforced
        within all elements and children of the root-level bom element.

        If a value was not provided in the constructor, a UUIDv4 will have been assigned.

        Returns:
           `BomRef` unique identifier for this Service
        """
        return self._bom_ref

    @property  # type: ignore[misc]
    @serializable.xml_sequence(1)
    def provider(self) -> Optional[OrganizationalEntity]:
        """
        Get the The organization that provides the service.

        Returns:
            `OrganizationalEntity` if set else `None`
        """
        return self._provider

    @provider.setter
    def provider(self, provider: Optional[OrganizationalEntity]) -> None:
        self._provider = provider

    @property  # type: ignore[misc]
    @serializable.xml_sequence(2)
    def group(self) -> Optional[str]:
        """
        The grouping name, namespace, or identifier. This will often be a shortened, single name of the company or
        project that produced the service or domain name. Whitespace and special characters should be avoided.

        Returns:
            `str` if provided else `None`
        """
        return self._group

    @group.setter
    def group(self, group: Optional[str]) -> None:
        self._group = group

    @property  # type: ignore[misc]
    @serializable.xml_sequence(3)
    def name(self) -> str:
        """
        The name of the service. This will often be a shortened, single name of the service.

        Returns:
            `str`
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property  # type: ignore[misc]
    @serializable.xml_sequence(4)
    def version(self) -> Optional[str]:
        """
        The service version.

        Returns:
            `str` if set else `None`
        """
        return self._version

    @version.setter
    def version(self, version: Optional[str]) -> None:
        self._version = version

    @property  # type: ignore[misc]
    @serializable.xml_sequence(5)
    def description(self) -> Optional[str]:
        """
        Specifies a description for the service.

        Returns:
            `str` if set else `None`
        """
        return self._description

    @description.setter
    def description(self, description: Optional[str]) -> None:
        self._description = description

    @property  # type: ignore[misc]
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'endpoint')
    @serializable.xml_sequence(6)
    def endpoints(self) -> "SortedSet[XsUri]":
        """
        A list of endpoints URI's this service provides.

        Returns:
            Set of `XsUri`
        """
        return self._endpoints

    @endpoints.setter
    def endpoints(self, endpoints: Iterable[XsUri]) -> None:
        self._endpoints = SortedSet(endpoints)

    @property  # type: ignore[misc]
    @serializable.xml_sequence(7)
    def authenticated(self) -> Optional[bool]:
        """
        A boolean value indicating if the service requires authentication. A value of true indicates the service
        requires authentication prior to use.

        A value of false indicates the service does not require authentication.

        Returns:
            `bool` if set else `None`
        """
        return self._authenticated

    @authenticated.setter
    def authenticated(self, authenticated: Optional[bool]) -> None:
        self._authenticated = authenticated

    @property  # type: ignore[misc]
    @serializable.json_name('x-trust-boundary')
    @serializable.xml_name('x-trust-boundary')
    @serializable.xml_sequence(8)
    def x_trust_boundary(self) -> Optional[bool]:
        """
        A boolean value indicating if use of the service crosses a trust zone or boundary. A value of true indicates
        that by using the service, a trust boundary is crossed.

        A value of false indicates that by using the service, a trust boundary is not crossed.

        Returns:
            `bool` if set else `None`
        """
        return self._x_trust_boundary

    @x_trust_boundary.setter
    def x_trust_boundary(self, x_trust_boundary: Optional[bool]) -> None:
        self._x_trust_boundary = x_trust_boundary

    @property  # type: ignore[misc]
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'classification')
    @serializable.xml_sequence(9)
    def data(self) -> "SortedSet[DataClassification]":
        """
        Specifies the data classification.

        Returns:
            Set of `DataClassification`
        """
        return self._data

    @data.setter
    def data(self, data: Iterable[DataClassification]) -> None:
        self._data = SortedSet(data)

    @property  # type: ignore[misc]
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'licenses')
    @serializable.xml_sequence(10)
    def licenses(self) -> "SortedSet[LicenseChoice]":
        """
        A optional list of statements about how this Service is licensed.

        Returns:
            Set of `LicenseChoice`
        """
        return self._licenses

    @licenses.setter
    def licenses(self, licenses: Iterable[LicenseChoice]) -> None:
        self._licenses = SortedSet(licenses)

    @property  # type: ignore[misc]
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'reference')
    @serializable.xml_sequence(11)
    def external_references(self) -> "SortedSet[ExternalReference]":
        """
        Provides the ability to document external references related to the Service.

        Returns:
            Set of `ExternalReference`
        """
        return self._external_references

    @external_references.setter
    def external_references(self, external_references: Iterable[ExternalReference]) -> None:
        self._external_references = SortedSet(external_references)

    @property  # type: ignore[misc]
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'service')
    @serializable.xml_sequence(13)
    def services(self) -> "SortedSet['Service']":
        """
        A list of services included or deployed behind the parent service.

        This is not a dependency tree.

        It provides a way to specify a hierarchical representation of service assemblies.

        Returns:
            Set of `Service`
        """
        return self._services

    @services.setter
    def services(self, services: Iterable['Service']) -> None:
        self._services = SortedSet(services)

    @property  # type: ignore[misc]
    @serializable.view(SchemaVersion1Dot4)
    @serializable.xml_sequence(14)
    def release_notes(self) -> Optional[ReleaseNotes]:
        """
        Specifies optional release notes.

        Returns:
            `ReleaseNotes` or `None`
        """
        return self._release_notes

    @release_notes.setter
    def release_notes(self, release_notes: Optional[ReleaseNotes]) -> None:
        self._release_notes = release_notes

    @property  # type: ignore[misc]
    @serializable.view(SchemaVersion1Dot3)
    @serializable.view(SchemaVersion1Dot4)
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'property')
    @serializable.xml_sequence(12)
    def properties(self) -> "SortedSet[Property]":
        """
        Provides the ability to document properties in a key/value store. This provides flexibility to include data not
        officially supported in the standard without having to use additional namespaces or create extensions.

        Return:
            Set of `Property`
        """
        return self._properties

    @properties.setter
    def properties(self, properties: Iterable[Property]) -> None:
        self._properties = SortedSet(properties)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Service):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Service):
            return ComparableTuple((self.group, self.name, self.version)) < \
                ComparableTuple((other.group, other.name, other.version))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((
            self.authenticated, tuple(self.data), self.description, tuple(self.endpoints),
            tuple(self.external_references), self.group, tuple(self.licenses), self.name, tuple(self.properties),
            self.provider, self.release_notes, tuple(self.services), self.version, self.x_trust_boundary
        ))

    def __repr__(self) -> str:
        return f'<Service bom-ref={self.bom_ref}, group={self.group}, name={self.name}, version={self.version}>'
