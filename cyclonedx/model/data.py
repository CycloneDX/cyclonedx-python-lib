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
This set of classes represents the component data types in the CycloneDX standard.

.. note::
    Introduced in CycloneDX v1.5.

.. note::
    See the CycloneDX Schema for component data:\n
    - XML: https://cyclonedx.org/docs/1.7/xml/#type_componentDataType\n
    - JSON: https://cyclonedx.org/docs/1.7/json/#components_items_data
"""

from collections.abc import Iterable
from enum import Enum
from typing import Any, Optional, Union

import py_serializable as serializable
from sortedcontainers import SortedSet

from .._internal.bom_ref import bom_ref_from_str as _bom_ref_from_str
from .._internal.compare import ComparableTuple as _ComparableTuple
from ..exception.model import InvalidValueException, MutuallyExclusivePropertiesException
from ..schema.schema import SchemaVersion1Dot5, SchemaVersion1Dot6, SchemaVersion1Dot7
from . import AttachedText, Property, XsUri
from .bom_ref import BomRef
from .contact import OrganizationalContact, OrganizationalEntity
from .graphics import GraphicsCollection


@serializable.serializable_enum
class ComponentDataKind(str, Enum):
    """Enumeration for `componentDataTypeEnumeration`: the type of data."""
    SOURCE_CODE = 'source-code'
    CONFIGURATION = 'configuration'
    DATASET = 'dataset'
    DEFINITION = 'definition'
    OTHER = 'other'


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class DataContents:
    """Contents or references to the contents of the data being described."""

    def __init__(
        self, *,
        attachment: Optional[AttachedText] = None,
        url: Optional[XsUri] = None,
        properties: Optional[Iterable[Property]] = None,
    ) -> None:
        self.attachment = attachment
        self.url = url
        self.properties = properties or []

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(1)
    def attachment(self) -> Optional[AttachedText]:
        """
        An optional way to include textual or encoded data.

        Returns:
            `AttachedText` if set else `None`
        """
        return self._attachment

    @attachment.setter
    def attachment(self, attachment: Optional[AttachedText]) -> None:
        self._attachment = attachment

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(2)
    def url(self) -> Optional[XsUri]:
        """
        The URL to where the data can be retrieved.

        Returns:
            `XsUri` if set else `None`
        """
        return self._url

    @url.setter
    def url(self, url: Optional[XsUri]) -> None:
        self._url = url

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'property')
    @serializable.xml_sequence(3)
    def properties(self) -> 'SortedSet[Property]':
        """
        Provides the ability to document properties in a name-value store.

        Returns:
            Set of `Property`
        """
        return self._properties

    @properties.setter
    def properties(self, properties: Iterable[Property]) -> None:
        self._properties = SortedSet(properties)

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((self.attachment, self.url, _ComparableTuple(self.properties)))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DataContents):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, DataContents):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, DataContents):
            return self.__comparable_tuple() <= other.__comparable_tuple()
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, DataContents):
            return self.__comparable_tuple() >= other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<DataContents attachment={self.attachment is not None} url={self.url is not None}>'


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class DataGovernanceResponsibleParty:
    """
    A party that is responsible for data: either an organization or an individual.

    Exactly one of `organization` and `contact` MUST be supplied, as required by the JSON schema.
    """

    def __init__(
        self, *,
        organization: Optional[OrganizationalEntity] = None,
        contact: Optional[OrganizationalContact] = None,
    ) -> None:
        if organization is None and contact is None:
            raise MutuallyExclusivePropertiesException('Either `organization` or `contact` MUST be supplied')
        self.organization = organization
        self.contact = contact

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(1)
    def organization(self) -> Optional[OrganizationalEntity]:
        """
        The organization that is responsible for the data.

        Returns:
            `OrganizationalEntity` if set else `None`
        """
        return self._organization

    @organization.setter
    def organization(self, organization: Optional[OrganizationalEntity]) -> None:
        if organization is not None and getattr(self, '_contact', None) is not None:
            raise MutuallyExclusivePropertiesException('`organization` and `contact` are mutually exclusive')
        self._organization = organization

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.json_name('contact')
    @serializable.xml_name('individual')
    @serializable.xml_sequence(2)
    def contact(self) -> Optional[OrganizationalContact]:
        """
        The individual that is responsible for the data.

        Returns:
            `OrganizationalContact` if set else `None`
        """
        return self._contact

    @contact.setter
    def contact(self, contact: Optional[OrganizationalContact]) -> None:
        if contact is not None and getattr(self, '_organization', None) is not None:
            raise MutuallyExclusivePropertiesException('`organization` and `contact` are mutually exclusive')
        self._contact = contact

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((self.organization, self.contact))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DataGovernanceResponsibleParty):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, DataGovernanceResponsibleParty):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, DataGovernanceResponsibleParty):
            return self.__comparable_tuple() <= other.__comparable_tuple()
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, DataGovernanceResponsibleParty):
            return self.__comparable_tuple() >= other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return (
            f'<DataGovernanceResponsibleParty organization={self.organization is not None} '
            f'contact={self.contact is not None}>'
        )


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class DataGovernance:
    """Governance of the data: its custodians, stewards and owners."""

    def __init__(
        self, *,
        custodians: Optional[Iterable[DataGovernanceResponsibleParty]] = None,
        stewards: Optional[Iterable[DataGovernanceResponsibleParty]] = None,
        owners: Optional[Iterable[DataGovernanceResponsibleParty]] = None,
    ) -> None:
        self.custodians = custodians or []
        self.stewards = stewards or []
        self.owners = owners or []

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'custodian')
    @serializable.xml_sequence(1)
    def custodians(self) -> 'SortedSet[DataGovernanceResponsibleParty]':
        """
        Data custodians are responsible for the safe custody, transport, and storage of data.

        Returns:
            Set of `DataGovernanceResponsibleParty`
        """
        return self._custodians

    @custodians.setter
    def custodians(self, custodians: Iterable[DataGovernanceResponsibleParty]) -> None:
        self._custodians = SortedSet(custodians)

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'steward')
    @serializable.xml_sequence(2)
    def stewards(self) -> 'SortedSet[DataGovernanceResponsibleParty]':
        """
        Data stewards are responsible for data content, context, and associated business rules.

        Returns:
            Set of `DataGovernanceResponsibleParty`
        """
        return self._stewards

    @stewards.setter
    def stewards(self, stewards: Iterable[DataGovernanceResponsibleParty]) -> None:
        self._stewards = SortedSet(stewards)

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'owner')
    @serializable.xml_sequence(3)
    def owners(self) -> 'SortedSet[DataGovernanceResponsibleParty]':
        """
        Data owners are concerned with risk and appropriate access to data.

        Returns:
            Set of `DataGovernanceResponsibleParty`
        """
        return self._owners

    @owners.setter
    def owners(self, owners: Iterable[DataGovernanceResponsibleParty]) -> None:
        self._owners = SortedSet(owners)

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((
            _ComparableTuple(self.custodians),
            _ComparableTuple(self.stewards),
            _ComparableTuple(self.owners),
        ))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DataGovernance):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, DataGovernance):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, DataGovernance):
            return self.__comparable_tuple() <= other.__comparable_tuple()
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, DataGovernance):
            return self.__comparable_tuple() >= other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return (
            f'<DataGovernance custodians={len(self.custodians)} '
            f'stewards={len(self.stewards)} owners={len(self.owners)}>'
        )


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class ComponentData:
    """
    Inline data of a component, as defined by `componentDataType`: a dataset, source code, configuration, etc.
    """

    def __init__(
        self, *,
        type: ComponentDataKind,
        bom_ref: Optional[Union[str, BomRef]] = None,
        name: Optional[str] = None,
        contents: Optional[DataContents] = None,
        classification: Optional[str] = None,
        sensitive_data: Optional[Iterable[str]] = None,
        graphics: Optional[GraphicsCollection] = None,
        description: Optional[str] = None,
        governance: Optional[DataGovernance] = None,
    ) -> None:
        self._bom_ref = _bom_ref_from_str(bom_ref)
        self.type = type
        self.name = name
        self.contents = contents
        self.classification = classification
        self.sensitive_data = sensitive_data or []
        self.graphics = graphics
        self.description = description
        self.governance = governance

    @property
    @serializable.json_name('bom-ref')
    @serializable.type_mapping(BomRef)
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_attribute()
    @serializable.xml_name('bom-ref')
    def bom_ref(self) -> BomRef:
        """
        An identifier which can be used to reference the data elsewhere in the BOM. Every `bom-ref` must be unique
        within the BOM.

        Returns:
            `BomRef`
        """
        return self._bom_ref

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(1)
    def type(self) -> ComponentDataKind:
        """
        The general theme or subject matter of the data being specified.

        Returns:
            `ComponentDataKind`
        """
        return self._type

    @type.setter
    def type(self, type: ComponentDataKind) -> None:
        self._type = type

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(2)
    def name(self) -> Optional[str]:
        """
        The name of the dataset.

        Returns:
            `str` if set else `None`
        """
        return self._name

    @name.setter
    def name(self, name: Optional[str]) -> None:
        self._name = name

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(3)
    def contents(self) -> Optional[DataContents]:
        """
        The contents or references to the contents of the data being described.

        Returns:
            `DataContents` if set else `None`
        """
        return self._contents

    @contents.setter
    def contents(self, contents: Optional[DataContents]) -> None:
        self._contents = contents

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(4)
    def classification(self) -> Optional[str]:
        """
        Data classification tags data according to its type, sensitivity, and value if altered, stolen, or destroyed.

        Returns:
            `str` if set else `None`
        """
        return self._classification

    @classification.setter
    def classification(self, classification: Optional[str]) -> None:
        self._classification = classification

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.json_name('sensitiveData')
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'sensitiveData')
    @serializable.xml_sequence(5)
    def sensitive_data(self) -> 'SortedSet[str]':
        """
        A description of any sensitive data in a dataset.

        Returns:
            Set of `str`
        """
        return self._sensitive_data

    @sensitive_data.setter
    def sensitive_data(self, sensitive_data: Iterable[str]) -> None:
        self._sensitive_data = SortedSet(sensitive_data)

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(6)
    def graphics(self) -> Optional[GraphicsCollection]:
        """
        A collection of graphics that represent various measurements.

        Returns:
            `GraphicsCollection` if set else `None`
        """
        return self._graphics

    @graphics.setter
    def graphics(self, graphics: Optional[GraphicsCollection]) -> None:
        self._graphics = graphics

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(7)
    def description(self) -> Optional[str]:
        """
        A description of the dataset. Can describe size of dataset, whether it's downloadable, etc.

        Returns:
            `str` if set else `None`
        """
        return self._description

    @description.setter
    def description(self, description: Optional[str]) -> None:
        self._description = description

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(8)
    def governance(self) -> Optional[DataGovernance]:
        """
        Data governance captures information regarding data ownership, stewardship, and custodianship.

        Returns:
            `DataGovernance` if set else `None`
        """
        return self._governance

    @governance.setter
    def governance(self, governance: Optional[DataGovernance]) -> None:
        self._governance = governance

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((
            self.type, self.bom_ref.value, self.name, self.contents, self.classification,
            _ComparableTuple(self.sensitive_data), self.graphics, self.description, self.governance,
        ))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ComponentData):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, ComponentData):
            return self.__comparable_tuple() < other.__comparable_tuple()
        if isinstance(other, DatasetReference):
            return True  # self before any DatasetReference
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, ComponentData):
            return self.__comparable_tuple() <= other.__comparable_tuple()
        if isinstance(other, DatasetReference):
            return True
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, ComponentData):
            return self.__comparable_tuple() >= other.__comparable_tuple()
        if isinstance(other, DatasetReference):
            return False
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<ComponentData bom-ref={self.bom_ref.value!r} type={self.type!r} name={self.name!r}>'


class DatasetReference:
    """
    A reference to a data component, as used by `modelCard.modelParameters.datasets`.

    The reference is either the `bom-ref` of a data component in the same BOM,
    or a BOM-Link (`urn:cdx:...`) to an element of another BOM.

    .. note::
        Serialization is handled by :attr:`cyclonedx.model.model_card.ModelParameters.datasets`.
    """

    def __init__(self, *, ref: Union[str, BomRef, XsUri]) -> None:
        self.ref = ref

    @property
    def ref(self) -> Union[str, BomRef, XsUri]:
        """
        The `bom-ref` of a data component, or a BOM-Link to one.

        Returns:
            `str`, `BomRef` or `XsUri`
        """
        return self._ref

    @ref.setter
    def ref(self, ref: Union[str, BomRef, XsUri]) -> None:
        # a `BomRef` may legitimately have no value yet, as it can be assigned when the BOM is serialized
        if isinstance(ref, (str, XsUri)) and not str(ref):
            raise InvalidValueException('`ref` MUST NOT be empty')
        self._ref = ref

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((str(self.ref),))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DatasetReference):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, DatasetReference):
            return self.__comparable_tuple() < other.__comparable_tuple()
        if isinstance(other, ComponentData):
            return False  # self after any ComponentData
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, DatasetReference):
            return self.__comparable_tuple() <= other.__comparable_tuple()
        if isinstance(other, ComponentData):
            return False
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, DatasetReference):
            return self.__comparable_tuple() >= other.__comparable_tuple()
        if isinstance(other, ComponentData):
            return True
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<DatasetReference ref={str(self.ref)!r}>'
