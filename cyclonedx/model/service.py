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


"""
This set of classes represents the data that is possible about known Services.

.. note::
    See the CycloneDX Schema extension definition https://cyclonedx.org/docs/1.4/xml/#type_servicesType
"""


from typing import Any, Iterable, Optional, Union

import serializable
from sortedcontainers import SortedSet

from cyclonedx.serialization import BomRefHelper, LicenseRepositoryHelper

from .._internal.compare import ComparableTuple as _ComparableTuple
from ..schema.schema import SchemaVersion1Dot3, SchemaVersion1Dot4, SchemaVersion1Dot5, SchemaVersion1Dot6
from . import DataClassification, DataFlow, ExternalReference, Property, XsUri
from .bom_ref import BomRef
from .contact import OrganizationalEntity
from .dependency import Dependable
from .license import License, LicenseRepository
from .release_note import ReleaseNotes


@serializable.serializable_class
class Service(Dependable):
    """
    Class that models the `service` complex type in the CycloneDX schema.

    .. note::
        See the CycloneDX schema: https://cyclonedx.org/docs/1.4/xml/#type_service
    """

    def __init__(
        self, *,
        name: str,
        bom_ref: Optional[Union[str, BomRef]] = None,
        provider: Optional[OrganizationalEntity] = None,
        group: Optional[str] = None,
        version: Optional[str] = None,
        description: Optional[str] = None,
        endpoints: Optional[Iterable[XsUri]] = None,
        authenticated: Optional[bool] = None,
        x_trust_boundary: Optional[bool] = None,
        data: Optional[Iterable[DataClassification]] = None,
        licenses: Optional[Iterable[License]] = None,
        external_references: Optional[Iterable[ExternalReference]] = None,
        properties: Optional[Iterable[Property]] = None,
        services: Optional[Iterable['Service']] = None,
        release_notes: Optional[ReleaseNotes] = None,
    ) -> None:
        if isinstance(bom_ref, BomRef):
            self._bom_ref = bom_ref
        else:
            self._bom_ref = BomRef(value=str(bom_ref) if bom_ref else None)
        self.provider = provider
        self.group = group
        self.name = name
        self.version = version
        self.description = description
        self.endpoints = endpoints or []  # type:ignore[assignment]
        self.authenticated = authenticated
        self.x_trust_boundary = x_trust_boundary
        self.data = data or []  # type:ignore[assignment]
        self.licenses = licenses or []  # type:ignore[assignment]
        self.external_references = external_references or []  # type:ignore[assignment]
        self.services = services or []  # type:ignore[assignment]
        self.release_notes = release_notes
        self.properties = properties or []  # type:ignore[assignment]

    @property
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

    @property
    @serializable.xml_sequence(1)
    def provider(self) -> Optional[OrganizationalEntity]:
        """
        Get the organization that provides the service.

        Returns:
            `OrganizationalEntity` if set else `None`
        """
        return self._provider

    @provider.setter
    def provider(self, provider: Optional[OrganizationalEntity]) -> None:
        self._provider = provider

    @property
    @serializable.xml_sequence(2)
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
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

    @property
    @serializable.xml_sequence(3)
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
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

    @property
    @serializable.xml_sequence(4)
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
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

    @property
    @serializable.xml_sequence(5)
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
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

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'endpoint')
    @serializable.xml_sequence(6)
    def endpoints(self) -> 'SortedSet[XsUri]':
        """
        A list of endpoints URI's this service provides.

        Returns:
            Set of `XsUri`
        """
        return self._endpoints

    @endpoints.setter
    def endpoints(self, endpoints: Iterable[XsUri]) -> None:
        self._endpoints = SortedSet(endpoints)

    @property
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

    @property
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

    # @property
    # ...
    # @serializable.view(SchemaVersion1Dot5)
    # @serializable.xml_sequence(9)
    # def trust_zone(self) -> ...:
    #     ... # since CDX1.5
    #
    # @trust_zone.setter
    # def trust_zone(self, ...) -> None:
    #     ... # since CDX1.5

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'classification')
    @serializable.xml_sequence(10)
    def data(self) -> 'SortedSet[DataClassification]':
        """
        Specifies the data classification.

        Returns:
            Set of `DataClassification`
        """
        # TODO since CDX1.5 also supports `dataflow`, not only `DataClassification`
        return self._data

    @data.setter
    def data(self, data: Iterable[DataClassification]) -> None:
        self._data = SortedSet(data)

    @property
    @serializable.type_mapping(LicenseRepositoryHelper)
    @serializable.xml_sequence(11)
    def licenses(self) -> LicenseRepository:
        """
        A optional list of statements about how this Service is licensed.

        Returns:
            Set of `LicenseChoice`
        """
        # TODO since CDX1.5 also supports `dataflow`, not only `DataClassification`
        return self._licenses

    @licenses.setter
    def licenses(self, licenses: Iterable[License]) -> None:
        self._licenses = LicenseRepository(licenses)

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'reference')
    @serializable.xml_sequence(12)
    def external_references(self) -> 'SortedSet[ExternalReference]':
        """
        Provides the ability to document external references related to the Service.

        Returns:
            Set of `ExternalReference`
        """
        return self._external_references

    @external_references.setter
    def external_references(self, external_references: Iterable[ExternalReference]) -> None:
        self._external_references = SortedSet(external_references)

    @property
    @serializable.view(SchemaVersion1Dot3)
    @serializable.view(SchemaVersion1Dot4)
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'property')
    @serializable.xml_sequence(13)
    def properties(self) -> 'SortedSet[Property]':
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

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'service')
    @serializable.xml_sequence(14)
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

    @property
    @serializable.view(SchemaVersion1Dot4)
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.xml_sequence(15)
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

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Service):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Service):
            return _ComparableTuple((
                self.group, self.name, self.version
            )) < _ComparableTuple((
                other.group, other.name, other.version
            ))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((
            self.authenticated, tuple(self.data), self.description, tuple(self.endpoints),
            tuple(self.external_references), self.group, tuple(self.licenses), self.name, tuple(self.properties),
            self.provider, self.release_notes, tuple(self.services), self.version, self.x_trust_boundary
        ))

    def __repr__(self) -> str:
        return f'<Service bom-ref={self.bom_ref}, group={self.group}, name={self.name}, version={self.version}>'


@serializable.serializable_class
class OrganizationOrIndividualType:
    """
    This is our internal representation of the organizationOrIndividualType complex type within the CycloneDX standard.

    .. note::
        See the CycloneDX Schema: https://cyclonedx.org/docs/1.6/xml/#type_organizationOrIndividualType
    """

    def __init__(
        self, *,
        organization: Optional[OrganizationalEntity] = None,
        individual: Optional[OrganizationalEntity] = None,
    ) -> None:
        self.organization = organization
        self.individual = individual

        # Property for organization
    @property
    @serializable.xml_sequence(1)
    @serializable.xml_name('organization')
    def organization(self) -> Optional[OrganizationalEntity]:
        return self._organization

    @organization.setter
    def organization(self, organization: Optional[OrganizationalEntity]) -> None:
        self._organization = organization

    # Property for individual
    @property
    @serializable.xml_sequence(2)
    @serializable.xml_name('individual')
    def individual(self) -> Optional[OrganizationalEntity]:
        return self._individual

    @individual.setter
    def individual(self, individual: Optional[OrganizationalEntity]) -> None:
        self._individual = individual


@serializable.serializable_class
class DataGovernance:
    """
    This is our internal representation of the dataGovernance complex type within the CycloneDX standard.

    .. note::
        See the CycloneDX Schema: https://cyclonedx.org/docs/1.6/xml/#type_dataGovernance
    """

    def __init__(
        self, *,
        custodian: Optional[OrganizationOrIndividualType] = None,
        steward: Optional[OrganizationOrIndividualType] = None,
        owner: Optional[OrganizationOrIndividualType] = None,
    ) -> None:
        self.custodian = custodian
        self.steward = steward
        self.owner = owner

    # Property for custodian
    @property
    @serializable.xml_sequence(1)
    @serializable.xml_name('custodian')
    def custodian(self) -> Optional[OrganizationOrIndividualType]:
        return self._custodian

    @custodian.setter
    def custodian(self, custodian: Optional[OrganizationOrIndividualType]) -> None:
        self._custodian = custodian

    # Property for steward
    @property
    @serializable.xml_sequence(2)
    @serializable.xml_name('steward')
    def steward(self) -> Optional[OrganizationOrIndividualType]:
        return self._steward

    @steward.setter
    def steward(self, steward: Optional[OrganizationOrIndividualType]) -> None:
        self._steward = steward

    # Property for owner
    @property
    @serializable.xml_sequence(3)
    @serializable.xml_name('owner')
    def owner(self) -> Optional[OrganizationOrIndividualType]:
        return self._owner

    @owner.setter
    def owner(self, owner: Optional[OrganizationOrIndividualType]) -> None:
        self._owner = owner


@serializable.serializable_class
class Data:
    """
    This is our internal representation of the service.data complex type within the CycloneDX standard.

    .. note::
    See the CycloneDX Schema: https://cyclonedx.org/docs/1.6/xml/#type_service
    """
    #  @serializable.xml_string(serializable.XmlStringSerializationType.STRING)

    def __init__(
        self, *,
        flow: DataFlow,
        classification: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        governance: Optional[DataGovernance] = None,
        source: Optional[Iterable[Union[BomRef, XsUri]]] = None,
        destination: Optional[Iterable[Union[BomRef, XsUri]]] = None
    ) -> None:
        self.flow = flow
        self.classification = classification
        self.name = name
        self.description = description
        self.governance = governance
        self.source = source
        self.destination = destination

    @property
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def name(self) -> Optional[str]:
        """
        The name of the service data.

        Returns:
            `str` if provided else None
        """
        return self._name

    @name.setter
    def name(self, name: Optional[str]) -> None:
        self._name = name

    @property
    @serializable.xml_attribute()
    def flow(self) -> DataFlow:
        """
        Specifies the flow direction of the data.

        Valid values are: inbound, outbound, bi-directional, and unknown.

        Direction is relative to the service.

        - Inbound flow states that data enters the service
        - Outbound flow states that data leaves the service
        - Bi-directional states that data flows both ways
        - Unknown states that the direction is not known

        Returns:
            `DataFlow`
        """
        return self._flow

    @flow.setter
    def flow(self, flow: DataFlow) -> None:
        self._flow = flow

    @property
    @serializable.xml_name('.')
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def classification(self) -> str:
        """
        Data classification tags data according to its type, sensitivity, and value if altered, stolen, or destroyed.

        Returns:
            `str`
        """
        return self._classification

    @classification.setter
    def classification(self, classification: str) -> None:
        self._classification = classification

        # description property

    @property
    @serializable.xml_sequence(2)  # Assuming order after name
    @serializable.xml_string(serializable.XmlStringSerializationType.STRING)
    def description(self) -> Optional[str]:
        """
        The description of the service data.

        Returns:
            `str` if provided else None
        """
        return self._description

    @description.setter
    def description(self, description: Optional[str]) -> None:
        self._description = description

    # governance property
    @property
    @serializable.xml_sequence(3)  # Assuming order after description
    def governance(self) -> Optional[DataGovernance]:
        """
        Governance information for the service data.

        Returns:
            `DataGovernance` if provided else None
        """
        return self._governance

    @governance.setter
    def governance(self, governance: Optional[DataGovernance]) -> None:
        self._governance = governance

    # source property
    @property
    @serializable.xml_sequence(4)  # Assuming order after governance
    def source(self) -> Optional[Iterable[Union[BomRef, XsUri]]]:
        """
        The source(s) of the service data.

        Returns:
            Iterable of `BomRef` or `XsUri` if provided else None
        """
        return self._source

    @source.setter
    def source(self, source: Optional[Iterable[Union[BomRef, XsUri]]]) -> None:
        self._source = source

    # destination property
    @property
    @serializable.xml_sequence(5)  # Assuming order after source
    def destination(self) -> Optional[Iterable[Union[BomRef, XsUri]]]:
        """
        The destination(s) of the service data.

        Returns:
            Iterable of `BomRef` or `XsUri` if provided else None
        """
        return self._destination

    @destination.setter
    def destination(self, destination: Optional[Iterable[Union[BomRef, XsUri]]]) -> None:
        self._destination = destination

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DataClassification):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: object) -> bool:
        if isinstance(other, DataClassification):
            return _ComparableTuple((
                self.flow, self.classification
            )) < _ComparableTuple((
                other.flow, other.classification
            ))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.flow, self.classification))

    def __repr__(self) -> str:
        return f'<DataClassification flow={self.flow}>'
