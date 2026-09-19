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
    See the CycloneDX Schema extension definition https://cyclonedx.org/docs/1.7/xml/#type_servicesType
"""


from collections.abc import Iterable
from json import loads as json_loads
from typing import Any, Optional, Union
from xml.etree.ElementTree import Element as XmlElement, SubElement  # nosec B405

import py_serializable as serializable
from sortedcontainers import SortedSet

from .._internal.bom_ref import bom_ref_from_str as _bom_ref_from_str
from .._internal.compare import ComparableTuple as _ComparableTuple
from ..schema import SchemaVersion
from ..schema.schema import (
    SchemaVersion1Dot3,
    SchemaVersion1Dot4,
    SchemaVersion1Dot5,
    SchemaVersion1Dot6,
    SchemaVersion1Dot7,
)
from . import DataClassification, DataFlow, ExternalReference, Property, XsUri
from .bom_ref import BomRef
from .contact import OrganizationalContact, OrganizationalEntity
from .dependency import Dependable
from .license import License, LicenseRepository, _LicenseRepositorySerializationHelper
from .release_note import ReleaseNotes


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
        individual: Optional[OrganizationalContact] = None,
    ) -> None:
        self.organization = organization
        self.individual = individual

    @property
    @serializable.xml_sequence(1)
    @serializable.xml_name('organization')
    def organization(self) -> Optional[OrganizationalEntity]:
        return self._organization

    @organization.setter
    def organization(self, organization: Optional[OrganizationalEntity]) -> None:
        self._organization = organization

    @property
    @serializable.json_name('contact')
    @serializable.xml_sequence(2)
    @serializable.xml_name('individual')
    def individual(self) -> Optional[OrganizationalContact]:
        return self._individual

    @individual.setter
    def individual(self, individual: Optional[OrganizationalContact]) -> None:
        self._individual = individual

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((
            self.organization, self.individual
        ))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, OrganizationOrIndividualType):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, OrganizationOrIndividualType):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())


@serializable.serializable_class
class DataGovernance:
    """
    This is our internal representation of the dataGovernance complex type within the CycloneDX standard.

    .. note::
        See the CycloneDX Schema: https://cyclonedx.org/docs/1.6/xml/#type_dataGovernance
    """

    def __init__(
        self, *,
        custodians: Optional[Iterable[OrganizationOrIndividualType]] = None,
        stewards: Optional[Iterable[OrganizationOrIndividualType]] = None,
        owners: Optional[Iterable[OrganizationOrIndividualType]] = None,
    ) -> None:
        self.custodians = custodians or []
        self.stewards = stewards or []
        self.owners = owners or []

    @property
    @serializable.xml_sequence(1)
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'custodian')
    def custodians(self) -> 'SortedSet[OrganizationOrIndividualType]':
        return self._custodians

    @custodians.setter
    def custodians(self, custodians: Iterable[OrganizationOrIndividualType]) -> None:
        self._custodians = SortedSet(custodians)

    @property
    @serializable.xml_sequence(2)
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'steward')
    def stewards(self) -> 'SortedSet[OrganizationOrIndividualType]':
        return self._stewards

    @stewards.setter
    def stewards(self, stewards: Iterable[OrganizationOrIndividualType]) -> None:
        self._stewards = SortedSet(stewards)

    @property
    @serializable.xml_sequence(3)
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'owner')
    def owners(self) -> 'SortedSet[OrganizationOrIndividualType]':
        return self._owners

    @owners.setter
    def owners(self, owners: Iterable[OrganizationOrIndividualType]) -> None:
        self._owners = SortedSet(owners)

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((
            _ComparableTuple(self.custodians), _ComparableTuple(self.stewards), _ComparableTuple(self.owners)
        ))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DataGovernance):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, DataGovernance):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())


class Data:
    """
    This is our internal representation of the ``serviceData`` complex type within the CycloneDX standard.

    .. note::
        See the CycloneDX Schema: https://cyclonedx.org/docs/1.6/xml/#type_service
    """

    def __init__(
        self, *,
        flow: DataFlow,
        classification: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        governance: Optional[DataGovernance] = None,
        source: Optional[Iterable[XsUri]] = None,
        destination: Optional[Iterable[XsUri]] = None
    ) -> None:
        self.flow = flow
        self.classification = classification
        self.name = name
        self.description = description
        self.governance = governance
        self.source = source or []
        self.destination = destination or []

    @property
    def flow(self) -> DataFlow:
        """
        Specifies the flow direction of the data. Direction is relative to the service.

        Returns:
            `DataFlow`
        """
        return self._flow

    @flow.setter
    def flow(self, flow: DataFlow) -> None:
        self._flow = flow

    @property
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

    @property
    def name(self) -> Optional[str]:
        """
        Name for the defined data.

        Returns:
            `str` if set else `None`
        """
        return self._name

    @name.setter
    def name(self, name: Optional[str]) -> None:
        self._name = name

    @property
    def description(self) -> Optional[str]:
        """
        Short description of the data content and usage.

        Returns:
            `str` if set else `None`
        """
        return self._description

    @description.setter
    def description(self, description: Optional[str]) -> None:
        self._description = description

    @property
    def governance(self) -> Optional[DataGovernance]:
        """
        Data governance information.

        Returns:
            `DataGovernance` if set else `None`
        """
        return self._governance

    @governance.setter
    def governance(self, governance: Optional[DataGovernance]) -> None:
        self._governance = governance

    @property
    def source(self) -> 'SortedSet[XsUri]':
        """
        The URI, URL, or BOM-Link of the components or services the data came in from.

        Returns:
            Set of `XsUri`
        """
        return self._source

    @source.setter
    def source(self, source: Iterable[XsUri]) -> None:
        self._source = SortedSet(source)

    @property
    def destination(self) -> 'SortedSet[XsUri]':
        """
        The URI, URL, or BOM-Link of the components or services the data is sent to.

        Returns:
            Set of `XsUri`
        """
        return self._destination

    @destination.setter
    def destination(self, destination: Iterable[XsUri]) -> None:
        self._destination = SortedSet(destination)

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((
            self.flow, self.classification, self.name, self.description, self.governance,
            _ComparableTuple(self.source), _ComparableTuple(self.destination)
        ))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Data):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Data):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<Data flow={self.flow}, classification={self.classification}>'


class _DataRepositorySerializationHelper(serializable.helpers.BaseHelper):
    """  THIS CLASS IS NON-PUBLIC API  """

    @staticmethod
    def __supports_service_data(view: Any) -> bool:
        try:
            return view is not None and view().schema_version_enum >= SchemaVersion.V1_5
        except Exception:  # pragma: no cover
            return False

    @classmethod
    def json_normalize(cls, o: 'SortedSet[Data]', *,
                       view: Optional[type[serializable.ViewType]],
                       **__: Any) -> Optional[list[Any]]:
        if not o:
            return None
        # CDX 1.5+ supports the full serviceData type; 1.2–1.4 only supports
        # the deprecated dataClassification (flow + classification string only).
        use_service_data = cls.__supports_service_data(view)
        result = []
        for d in o:
            if use_service_data:
                item: dict[str, Any] = {
                    'flow': d.flow.value,
                    'classification': d.classification,
                }
                if d.name is not None:
                    item['name'] = d.name
                if d.description is not None:
                    item['description'] = d.description
                if d.governance is not None:
                    item['governance'] = json_loads(
                        d.governance.as_json(view_=view)  # type:ignore[attr-defined]
                    )
                if d.source:
                    item['source'] = [str(u) for u in d.source]
                if d.destination:
                    item['destination'] = [str(u) for u in d.destination]
            else:
                # CDX 1.2–1.4: only flow + classification
                item = {
                    'flow': d.flow.value,
                    'classification': d.classification,
                }
            result.append(item)
        return result

    @classmethod
    def json_denormalize(cls, o: list[dict[str, Any]], **__: Any) -> 'SortedSet[Data]':
        result: SortedSet[Data] = SortedSet()
        for item in o:
            governance = None
            if 'governance' in item:
                governance = DataGovernance.from_json(  # type:ignore[attr-defined]
                    item['governance'])
            result.add(Data(
                flow=DataFlow(item['flow']),
                classification=item['classification'],
                name=item.get('name'),
                description=item.get('description'),
                governance=governance,
                source=[XsUri(u) for u in item.get('source', [])],
                destination=[XsUri(u) for u in item.get('destination', [])],
            ))
        return result

    @classmethod
    def _xml_single_dataflow(
        cls, d: 'Data', *,
        pfx: str,
        view: Optional[type[serializable.ViewType]],
        xmlns: Optional[str],
    ) -> XmlElement:
        """Build a CDX 1.5+ ``<dataflow>`` element for a single Data item."""
        dataflow_elem = XmlElement(f'{pfx}dataflow')
        if d.name is not None:
            dataflow_elem.set(f'{pfx}name', d.name)
        if d.description is not None:
            dataflow_elem.set(f'{pfx}description', d.description)
        dataflow_elem.append(
            DataClassification(
                flow=d.flow, classification=d.classification
            ).as_xml(  # type:ignore[attr-defined]
                view_=view, as_string=False, element_name='classification', xmlns=xmlns
            )
        )
        if d.governance is not None:
            gov_elem = d.governance.as_xml(  # type:ignore[attr-defined]
                view_=view, as_string=False, element_name='governance', xmlns=xmlns)
            dataflow_elem.append(gov_elem)
        if d.source:
            src_elem = SubElement(dataflow_elem, f'{pfx}source')
            for u in d.source:
                SubElement(src_elem, f'{pfx}url').text = str(u)
        if d.destination:
            dst_elem = SubElement(dataflow_elem, f'{pfx}destination')
            for u in d.destination:
                SubElement(dst_elem, f'{pfx}url').text = str(u)
        return dataflow_elem

    @classmethod
    def xml_normalize(cls, o: 'SortedSet[Data]', *,
                      element_name: str,
                      view: Optional[type[serializable.ViewType]],
                      xmlns: Optional[str],
                      **__: Any) -> Optional[XmlElement]:
        if not o:
            return None
        # element_name is already namespace-qualified by py_serializable when xmlns is set.
        # Build a prefix for child elements we create manually.
        pfx = f'{{{xmlns}}}' if xmlns else ''
        wrapper = XmlElement(element_name)
        # CDX 1.5+ uses <dataflow> elements; 1.2–1.4 uses the deprecated flat <classification>
        use_dataflow = cls.__supports_service_data(view)
        for d in o:
            if use_dataflow:
                wrapper.append(cls._xml_single_dataflow(d, pfx=pfx, view=view, xmlns=xmlns))
            else:
                # CDX 1.2–1.4 (deprecated): <classification flow="...">text</classification>
                wrapper.append(
                    DataClassification(
                        flow=d.flow, classification=d.classification
                    ).as_xml(  # type:ignore[attr-defined]
                        view_=view, as_string=False, element_name='classification', xmlns=xmlns
                    )
                )
        return wrapper

    @classmethod
    def xml_denormalize(cls, o: XmlElement, *,
                        default_ns: Optional[str],
                        **__: Any) -> 'SortedSet[Data]':
        result: SortedSet[Data] = SortedSet()
        ns = f'{{{default_ns}}}' if default_ns else ''
        for elem in o:
            tag = elem.tag.replace(f'{{{default_ns}}}', '') if default_ns else elem.tag
            if tag == 'dataflow':
                # CDX 1.5+ <dataflow> element
                cls_elem = elem.find(f'{ns}classification')
                # flow attribute may be namespace-qualified or plain
                flow_val = (cls_elem.get(f'{ns}flow') or cls_elem.get('flow')) if cls_elem is not None else None
                classification_text = cls_elem.text or '' if cls_elem is not None else ''
                flow = DataFlow(flow_val) if flow_val else DataFlow.UNKNOWN
                gov_elem = elem.find(f'{ns}governance')
                governance = None
                if gov_elem is not None:
                    governance = DataGovernance.from_xml(  # type:ignore[attr-defined]
                        gov_elem, default_ns)
                src_elem = elem.find(f'{ns}source')
                source = [XsUri(u.text or '') for u in src_elem.findall(f'{ns}url')] if src_elem is not None else []
                dst_elem = elem.find(f'{ns}destination')
                destination = [XsUri(u.text or '')
                               for u in dst_elem.findall(f'{ns}url')] if dst_elem is not None else []
                # name and description may be namespace-qualified or plain attributes
                name = elem.get(f'{ns}name') or elem.get('name')
                description = elem.get(f'{ns}description') or elem.get('description')
                result.add(Data(
                    flow=flow,
                    classification=classification_text,
                    name=name,
                    description=description,
                    governance=governance,
                    source=source,
                    destination=destination,
                ))
            elif tag == 'classification':
                # CDX 1.2–1.4 deprecated <classification flow="...">text</classification>
                flow_val = elem.get(f'{ns}flow') or elem.get('flow')
                result.add(Data(
                    flow=DataFlow(flow_val) if flow_val else DataFlow.UNKNOWN,
                    classification=elem.text or '',
                ))
        return result


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class Service(Dependable):
    """
    Class that models the `service` complex type in the CycloneDX schema.

    .. note::
        See the CycloneDX schema: https://cyclonedx.org/docs/1.7/xml/#type_service
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
        data: Optional[Iterable['Data']] = None,
        licenses: Optional[Iterable[License]] = None,
        external_references: Optional[Iterable[ExternalReference]] = None,
        properties: Optional[Iterable[Property]] = None,
        services: Optional[Iterable['Service']] = None,
        release_notes: Optional[ReleaseNotes] = None,
    ) -> None:
        self._bom_ref = _bom_ref_from_str(bom_ref)
        self.provider = provider
        self.group = group
        self.name = name
        self.version = version
        self.description = description
        self.endpoints = endpoints or []
        self.authenticated = authenticated
        self.x_trust_boundary = x_trust_boundary
        self.data = data or []
        self.licenses = licenses or []
        self.external_references = external_references or []
        self.services = services or []
        self.release_notes = release_notes
        self.properties = properties or []

    @property
    @serializable.json_name('bom-ref')
    @serializable.type_mapping(BomRef)
    @serializable.xml_attribute()
    @serializable.xml_name('bom-ref')
    def bom_ref(self) -> BomRef:
        """
        An optional identifier which can be used to reference the service elsewhere in the BOM. Uniqueness is enforced
        within all elements and children of the root-level bom element.

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
    @serializable.type_mapping(_DataRepositorySerializationHelper)
    @serializable.xml_sequence(10)
    def data(self) -> 'SortedSet[Data]':
        """
        Specifies the data flow and classification.

        Returns:
            Set of `Data`
        """
        return self._data

    @data.setter
    def data(self, data: Iterable['Data']) -> None:
        self._data = SortedSet(data)

    @property
    @serializable.type_mapping(_LicenseRepositorySerializationHelper)
    @serializable.xml_sequence(11)
    def licenses(self) -> LicenseRepository:
        """
        A optional list of statements about how this Service is licensed.

        Returns:
            Set of `LicenseChoice`
        """
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
    @serializable.view(SchemaVersion1Dot7)
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
    @serializable.view(SchemaVersion1Dot7)
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

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((
            self.group, self.name, self.version,
            self.bom_ref.value,
            self.provider, self.description,
            self.authenticated, _ComparableTuple(self.data), _ComparableTuple(self.endpoints),
            _ComparableTuple(self.external_references), _ComparableTuple(self.licenses),
            _ComparableTuple(self.properties), self.release_notes, _ComparableTuple(self.services),
            self.x_trust_boundary
        ))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Service):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Service):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<Service bom-ref={self.bom_ref}, group={self.group}, name={self.name}, version={self.version}>'
