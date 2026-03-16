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
License related things
"""

from collections.abc import Iterable
from datetime import datetime
from enum import Enum
from json import loads as json_loads
from typing import TYPE_CHECKING, Any, Optional, Union
from warnings import warn
from xml.etree.ElementTree import Element  # nosec B405

import py_serializable as serializable
from sortedcontainers import SortedSet

from .._internal.bom_ref import bom_ref_from_str as _bom_ref_from_str
from .._internal.compare import ComparableTuple as _ComparableTuple
from ..exception.model import MutuallyExclusivePropertiesException
from ..exception.serialization import CycloneDxDeserializationException
from ..schema.schema import SchemaVersion1Dot5, SchemaVersion1Dot6, SchemaVersion1Dot7
from . import AttachedText, XsUri
from .bom_ref import BomRef
from .contact import OrganizationalContact, OrganizationalEntity


@serializable.serializable_enum
class LicenseAcknowledgement(str, Enum):
    """
    This is our internal representation of the `type_licenseAcknowledgementEnumerationType` ENUM type
    within the CycloneDX standard.

    .. note::
        Introduced in CycloneDX v1.6

    .. note::
        See the CycloneDX Schema for hashType:
        https://cyclonedx.org/docs/1.7/xml/#type_licenseAcknowledgementEnumerationType
    """

    CONCLUDED = 'concluded'
    DECLARED = 'declared'


# In an error, the name of the enum was `LicenseExpressionAcknowledgement`.
# Even though this was changed, there might be some downstream usage of this symbol, so we keep it around ...
LicenseExpressionAcknowledgement = LicenseAcknowledgement
"""Deprecated — Alias for :class:`LicenseAcknowledgement`

.. deprecated:: next Import `LicenseAcknowledgement` instead.
    The exported original symbol itself is NOT deprecated - only this import path.
"""


@serializable.serializable_enum
class LicenseType(str, Enum):
    """
    This is our internal representation of the `licenseTypeEnumeration` ENUM type
    within the CycloneDX standard.

    .. note::
        Introduced in CycloneDX v1.5

    .. note::
        See the CycloneDX Schema:
        https://cyclonedx.org/docs/1.7/json/#components_items_licenses_items_license_licensing_licenseTypes
    """

    ACADEMIC = 'academic'
    APPLIANCE = 'appliance'
    CLIENT_ACCESS = 'client-access'
    CONCURRENT_USER = 'concurrent-user'
    CORE_POINTS = 'core-points'
    CUSTOM_METRIC = 'custom-metric'
    DEVICE = 'device'
    EVALUATION = 'evaluation'
    NAMED_USER = 'named-user'
    NODE_LOCKED = 'node-locked'
    OEM = 'oem'
    PERPETUAL = 'perpetual'
    PROCESSOR_POINTS = 'processor-points'
    SUBSCRIPTION = 'subscription'
    USER = 'user'
    OTHER = 'other'


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class LicenseEntity:
    """
    This is our internal representation of the licensor/licensee/purchaser type
    within the CycloneDX standard.

    Exactly one of ``organization`` or ``individual`` MUST be provided.

    .. note::
        Introduced in CycloneDX v1.5

    .. note::
        See the CycloneDX Schema definition:
        https://cyclonedx.org/docs/1.7/json/#components_items_licenses_items_license_licensing_licensor
    """

    def __init__(
        self, *,
        organization: Optional[OrganizationalEntity] = None,
        individual: Optional[OrganizationalContact] = None,
    ) -> None:
        if not organization and not individual:
            raise MutuallyExclusivePropertiesException(
                'Either `organization` or `individual` MUST be supplied'
            )
        if organization and individual:
            raise MutuallyExclusivePropertiesException(
                'Only one of `organization` or `individual` MUST be supplied - not both'
            )
        self._organization = organization
        self._individual = individual

    @property
    @serializable.xml_sequence(1)
    def organization(self) -> Optional[OrganizationalEntity]:
        """
        The organization.

        Returns:
            `OrganizationalEntity` or `None`
        """
        return self._organization

    @organization.setter
    def organization(self, organization: Optional[OrganizationalEntity]) -> None:
        self._organization = organization
        if organization is not None:
            self._individual = None

    @property
    @serializable.xml_sequence(2)
    def individual(self) -> Optional[OrganizationalContact]:
        """
        The individual.

        Returns:
            `OrganizationalContact` or `None`
        """
        return self._individual

    @individual.setter
    def individual(self, individual: Optional[OrganizationalContact]) -> None:
        self._individual = individual
        if individual is not None:
            self._organization = None

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((
            self._organization, self._individual,
        ))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, LicenseEntity):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, LicenseEntity):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<LicenseEntity organization={self._organization!r}, individual={self._individual!r}>'


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class Licensing:
    """
    This is our internal representation of the `licensingType` complex type
    within the CycloneDX standard.

    Licensing details describing the licensor/licensee, license type, renewal
    and expiration dates, and other important metadata.

    .. note::
        Introduced in CycloneDX v1.5

    .. note::
        See the CycloneDX Schema definition:
        https://cyclonedx.org/docs/1.7/json/#components_items_licenses_items_license_licensing
    """

    def __init__(
        self, *,
        alt_ids: Optional[Iterable[str]] = None,
        licensor: Optional[LicenseEntity] = None,
        licensee: Optional[LicenseEntity] = None,
        purchaser: Optional[LicenseEntity] = None,
        purchase_order: Optional[str] = None,
        license_types: Optional[Iterable[LicenseType]] = None,
        last_renewal: Optional[datetime] = None,
        expiration: Optional[datetime] = None,
    ) -> None:
        self.alt_ids = alt_ids or []
        self.licensor = licensor
        self.licensee = licensee
        self.purchaser = purchaser
        self.purchase_order = purchase_order
        self.license_types = license_types or []
        self.last_renewal = last_renewal
        self.expiration = expiration

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'altId')
    @serializable.xml_sequence(1)
    def alt_ids(self) -> 'SortedSet[str]':
        """
        License identifiers that may be used to manage licenses and their lifecycle.

        Returns:
            `SortedSet[str]`
        """
        return self._alt_ids

    @alt_ids.setter
    def alt_ids(self, alt_ids: Iterable[str]) -> None:
        self._alt_ids = SortedSet(alt_ids)

    @property
    @serializable.xml_sequence(2)
    def licensor(self) -> Optional[LicenseEntity]:
        """
        The individual or organization that grants a license to another individual or organization.

        Returns:
            `LicenseEntity` or `None`
        """
        return self._licensor

    @licensor.setter
    def licensor(self, licensor: Optional[LicenseEntity]) -> None:
        self._licensor = licensor

    @property
    @serializable.xml_sequence(3)
    def licensee(self) -> Optional[LicenseEntity]:
        """
        The individual or organization for which a license was granted to.

        Returns:
            `LicenseEntity` or `None`
        """
        return self._licensee

    @licensee.setter
    def licensee(self, licensee: Optional[LicenseEntity]) -> None:
        self._licensee = licensee

    @property
    @serializable.xml_sequence(4)
    def purchaser(self) -> Optional[LicenseEntity]:
        """
        The individual or organization that purchased the license.

        Returns:
            `LicenseEntity` or `None`
        """
        return self._purchaser

    @purchaser.setter
    def purchaser(self, purchaser: Optional[LicenseEntity]) -> None:
        self._purchaser = purchaser

    @property
    @serializable.xml_sequence(5)
    def purchase_order(self) -> Optional[str]:
        """
        The purchase order identifier the purchaser sent to a supplier or vendor to
        authorize a purchase.

        Returns:
            `str` or `None`
        """
        return self._purchase_order

    @purchase_order.setter
    def purchase_order(self, purchase_order: Optional[str]) -> None:
        self._purchase_order = purchase_order

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'licenseType')
    @serializable.xml_sequence(6)
    def license_types(self) -> 'SortedSet[LicenseType]':
        """
        The type of license(s) that was granted to the licensee.

        Returns:
            `SortedSet[LicenseType]`
        """
        return self._license_types

    @license_types.setter
    def license_types(self, license_types: Iterable[LicenseType]) -> None:
        self._license_types = SortedSet(license_types)

    @property
    @serializable.type_mapping(serializable.helpers.XsdDateTime)
    @serializable.xml_sequence(7)
    def last_renewal(self) -> Optional[datetime]:
        """
        The timestamp indicating when the license was last renewed. For new purchases, this is
        often the purchase or acquisition date. For non-perpetual licenses or subscriptions, this
        is the timestamp of when the license was last renewed.

        Returns:
            `datetime` or `None`
        """
        return self._last_renewal

    @last_renewal.setter
    def last_renewal(self, last_renewal: Optional[datetime]) -> None:
        self._last_renewal = last_renewal

    @property
    @serializable.type_mapping(serializable.helpers.XsdDateTime)
    @serializable.xml_sequence(8)
    def expiration(self) -> Optional[datetime]:
        """
        The timestamp indicating when the current license expires (if applicable).

        Returns:
            `datetime` or `None`
        """
        return self._expiration

    @expiration.setter
    def expiration(self, expiration: Optional[datetime]) -> None:
        self._expiration = expiration

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((
            _ComparableTuple(self._alt_ids),
            self._licensor, self._licensee, self._purchaser,
            self._purchase_order,
            _ComparableTuple(self._license_types),
            self._last_renewal, self._expiration,
        ))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Licensing):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Licensing):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<Licensing alt_ids={self._alt_ids!r}, licensor={self._licensor!r}, licensee={self._licensee!r}, ' \
            f'purchaser={self._purchaser!r}, purchase_order={self._purchase_order!r}, ' \
            f'license_types={self._license_types!r}, last_renewal={self._last_renewal!r}, ' \
            f'expiration={self._expiration!r}>'


@serializable.serializable_class(
    name='license',
    ignore_unknown_during_deserialization=True
)
class DisjunctiveLicense:
    """
    This is our internal representation of `licenseType` complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_licenseType
    """

    def __init__(
        self, *,
        bom_ref: Optional[Union[str, BomRef]] = None,
        id: Optional[str] = None, name: Optional[str] = None,
        text: Optional[AttachedText] = None, url: Optional[XsUri] = None,
        licensing: Optional[Licensing] = None,
        acknowledgement: Optional[LicenseAcknowledgement] = None,
    ) -> None:
        if not id and not name:
            raise MutuallyExclusivePropertiesException('Either `id` or `name` MUST be supplied')
        if id and name:
            warn(
                'Both `id` and `name` have been supplied - `name` will be ignored!',
                category=RuntimeWarning, stacklevel=1
            )
        self._bom_ref = _bom_ref_from_str(bom_ref)
        self._id = id
        self._name = name if not id else None
        self._text = text
        self._url = url
        self._licensing = licensing
        self._acknowledgement = acknowledgement

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.type_mapping(BomRef)
    @serializable.xml_attribute()
    @serializable.xml_name('bom-ref')
    @serializable.json_name('bom-ref')
    def bom_ref(self) -> BomRef:
        """
        An optional identifier which can be used to reference the component elsewhere in the BOM. Every bom-ref MUST be
        unique within the BOM.

        Returns:
            `BomRef`
        """
        return self._bom_ref

    @property
    @serializable.xml_sequence(1)
    def id(self) -> Optional[str]:
        """
        A SPDX license ID.

        .. note::
          See the list of expected values:
          https://cyclonedx.org/docs/1.7/json/#components_items_licenses_items_license_id

        Returns:
            `str` or `None`
        """
        return self._id

    @id.setter
    def id(self, id: Optional[str]) -> None:
        self._id = id
        if id is not None:
            self._name = None

    @property
    @serializable.xml_sequence(1)
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def name(self) -> Optional[str]:
        """
        If SPDX does not define the license used, this field may be used to provide the license name.

        Returns:
            `str` or `None`
        """
        return self._name

    @name.setter
    def name(self, name: Optional[str]) -> None:
        self._name = name
        if name is not None:
            self._id = None

    @property
    @serializable.xml_sequence(2)
    def text(self) -> Optional[AttachedText]:
        """
        Specifies the optional full text of the attachment

        Returns:
            `AttachedText` else `None`
        """
        return self._text

    @text.setter
    def text(self, text: Optional[AttachedText]) -> None:
        self._text = text

    @property
    @serializable.xml_sequence(3)
    def url(self) -> Optional[XsUri]:
        """
        The URL to the attachment file. If the attachment is a license or BOM, an externalReference should also be
        specified for completeness.

        Returns:
            `XsUri` or `None`
        """
        return self._url

    @url.setter
    def url(self, url: Optional[XsUri]) -> None:
        self._url = url

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(5)
    def licensing(self) -> Optional[Licensing]:
        """
        Licensing details describing the licensor/licensee, license type, renewal and expiration
        dates, and other important metadata.

        Returns:
            `Licensing` or `None`
        """
        return self._licensing

    @licensing.setter
    def licensing(self, licensing: Optional[Licensing]) -> None:
        self._licensing = licensing

    # @property
    # ...
    # @serializable.view(SchemaVersion1Dot5)
    # @serializable.view(SchemaVersion1Dot6)
    # @serializable.xml_sequence(6)
    # def properties(self) -> ...:
    #     ...  # TODO since CDX1.5
    #
    # @properties.setter
    # def properties(self, ...) -> None:
    #     ...  # TODO since CDX1.5

    @property
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_attribute()
    def acknowledgement(self) -> Optional[LicenseAcknowledgement]:
        """
        Declared licenses and concluded licenses represent two different stages in the licensing process within
        software development.

        Declared licenses refer to the initial intention of the software authors regarding the
        licensing terms under which their code is released. On the other hand, concluded licenses are the result of a
        comprehensive analysis of the project's codebase to identify and confirm the actual licenses of the components
        used, which may differ from the initially declared licenses. While declared licenses provide an upfront
        indication of the licensing intentions, concluded licenses offer a more thorough understanding of the actual
        licensing within a project, facilitating proper compliance and risk management. Observed licenses are defined
        in evidence.licenses. Observed licenses form the evidence necessary to substantiate a concluded license.

        Returns:
            `LicenseAcknowledgement` or `None`
        """
        return self._acknowledgement

    @acknowledgement.setter
    def acknowledgement(self, acknowledgement: Optional[LicenseAcknowledgement]) -> None:
        self._acknowledgement = acknowledgement

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((
            self._acknowledgement,
            self._id, self._name,
            self._url,
            self._text,
            self._licensing,
            self._bom_ref.value,
        ))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DisjunctiveLicense):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, DisjunctiveLicense):
            return self.__comparable_tuple() < other.__comparable_tuple()
        if isinstance(other, LicenseExpression):
            return False  # self after any LicenseExpression
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<License id={self._id!r}, name={self._name!r}>'


@serializable.serializable_class(
    name='expression',
    ignore_unknown_during_deserialization=True
)
class LicenseExpression:
    """
    This is our internal representation of `licenseType`'s  expression type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition:
        https://cyclonedx.org/docs/1.7/json/#components_items_licenses_items_expression
    """

    def __init__(
        self, value: str, *,
        bom_ref: Optional[Union[str, BomRef]] = None,
        acknowledgement: Optional[LicenseAcknowledgement] = None,
    ) -> None:
        self._bom_ref = _bom_ref_from_str(bom_ref)
        self._value = value
        self._acknowledgement = acknowledgement

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.type_mapping(BomRef)
    @serializable.xml_attribute()
    @serializable.xml_name('bom-ref')
    @serializable.json_name('bom-ref')
    def bom_ref(self) -> BomRef:
        """
        An optional identifier which can be used to reference the component elsewhere in the BOM. Every bom-ref MUST be
        unique within the BOM.

        Returns:
            `BomRef`
        """
        return self._bom_ref

    @property
    @serializable.xml_name('.')
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    @serializable.json_name('expression')
    def value(self) -> str:
        """
        Value of this LicenseExpression.

        Returns:
             `str`
        """
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        self._value = value

    @property
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_attribute()
    def acknowledgement(self) -> Optional[LicenseAcknowledgement]:
        """
        Declared licenses and concluded licenses represent two different stages in the licensing process within
        software development.

        Declared licenses refer to the initial intention of the software authors regarding the
        licensing terms under which their code is released. On the other hand, concluded licenses are the result of a
        comprehensive analysis of the project's codebase to identify and confirm the actual licenses of the components
        used, which may differ from the initially declared licenses. While declared licenses provide an upfront
        indication of the licensing intentions, concluded licenses offer a more thorough understanding of the actual
        licensing within a project, facilitating proper compliance and risk management. Observed licenses are defined
        in evidence.licenses. Observed licenses form the evidence necessary to substantiate a concluded license.

        Returns:
            `LicenseAcknowledgement` or `None`
        """
        return self._acknowledgement

    @acknowledgement.setter
    def acknowledgement(self, acknowledgement: Optional[LicenseAcknowledgement]) -> None:
        self._acknowledgement = acknowledgement

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((
            self._acknowledgement,
            self._value,
            self._bom_ref.value,
        ))

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __eq__(self, other: object) -> bool:
        if isinstance(other, LicenseExpression):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, LicenseExpression):
            return self.__comparable_tuple() < other.__comparable_tuple()
        if isinstance(other, DisjunctiveLicense):
            return True  # self before any DisjunctiveLicense
        return NotImplemented

    def __repr__(self) -> str:
        return f'<LicenseExpression value={self._value!r}>'


License = Union[LicenseExpression, DisjunctiveLicense]
"""TypeAlias for a union of supported license models.

- :class:`LicenseExpression`
- :class:`DisjunctiveLicense`
"""

if TYPE_CHECKING:  # pragma: no cover
    # workaround for https://github.com/python/mypy/issues/5264
    # this code path is taken when static code analysis or documentation tools runs through.
    class LicenseRepository(SortedSet[License]):
        """Collection of :class:`License`.

        This is a `set`, not a `list`.  Order MUST NOT matter here.
        If you wanted a certain order, then you should also express whether the items are concat by `AND` or `OR`.
        If you wanted to do so, you should use :class:`LicenseExpression`.

        As a model, this MUST accept multiple :class:`LicenseExpression` along with
        multiple :class:`DisjunctiveLicense`, as this was an accepted in CycloneDX JSON before v1.5.
        So for modeling purposes, this is supported.
        Denormalizers/deserializers will be thankful.
        The normalization/serialization process SHOULD take care of these facts and do what is needed.
        """

else:
    class LicenseRepository(SortedSet):
        """Collection of :class:`License`.

        This is a `set`, not a `list`.  Order MUST NOT matter here.
        If you wanted a certain order, then you should also express whether the items are concat by `AND` or `OR`.
        If you wanted to do so, you should use :class:`LicenseExpression`.

        As a model, this MUST accept multiple :class:`LicenseExpression` along with
        multiple :class:`DisjunctiveLicense`, as this was an accepted in CycloneDX JSON before v1.5.
        So for modeling purposes, this is supported.
        Denormalizers/deserializers will be thankful.
        The normalization/serialization process SHOULD take care of these facts and do what is needed.
        """


class _LicenseRepositorySerializationHelper(serializable.helpers.BaseHelper):
    """  THIS CLASS IS NON-PUBLIC API  """

    @classmethod
    def json_normalize(cls, o: LicenseRepository, *,
                       view: Optional[type[serializable.ViewType]],
                       **__: Any) -> Any:
        if len(o) == 0:
            return None
        expression = next((li for li in o if isinstance(li, LicenseExpression)), None)
        if expression:
            # mixed license expression and license? this is an invalid constellation according to schema!
            # see https://github.com/CycloneDX/specification/pull/205
            # but models need to allow it for backwards compatibility with JSON CDX < 1.5
            return [json_loads(expression.as_json(view_=view))]  # type:ignore[attr-defined]
        return [
            {'license': json_loads(
                li.as_json(  # type:ignore[attr-defined]
                    view_=view)
            )}
            for li in o
            if isinstance(li, DisjunctiveLicense)
        ]

    @classmethod
    def json_denormalize(cls, o: list[dict[str, Any]],
                         **__: Any) -> LicenseRepository:
        repo = LicenseRepository()
        for li in o:
            if 'license' in li:
                repo.add(DisjunctiveLicense.from_json(  # type:ignore[attr-defined]
                    li['license']))
            elif 'expression' in li:
                repo.add(LicenseExpression.from_json(  # type:ignore[attr-defined]
                    li
                ))
            else:
                raise CycloneDxDeserializationException(f'unexpected: {li!r}')
        return repo

    @classmethod
    def xml_normalize(cls, o: LicenseRepository, *,
                      element_name: str,
                      view: Optional[type[serializable.ViewType]],
                      xmlns: Optional[str],
                      **__: Any) -> Optional[Element]:
        if len(o) == 0:
            return None
        elem = Element(element_name)
        expression = next((li for li in o if isinstance(li, LicenseExpression)), None)
        if expression:
            # mixed license expression and license? this is an invalid constellation according to schema!
            # see https://github.com/CycloneDX/specification/pull/205
            # but models need to allow it for backwards compatibility with JSON CDX < 1.5
            elem.append(expression.as_xml(  # type:ignore[attr-defined]
                view_=view, as_string=False, element_name='expression', xmlns=xmlns))
        else:
            elem.extend(
                li.as_xml(  # type:ignore[attr-defined]
                    view_=view, as_string=False, element_name='license', xmlns=xmlns)
                for li in o
                if isinstance(li, DisjunctiveLicense)
            )
        return elem

    @classmethod
    def xml_denormalize(cls, o: Element,
                        default_ns: Optional[str],
                        **__: Any) -> LicenseRepository:
        repo = LicenseRepository()
        for li in o:
            tag = li.tag if default_ns is None else li.tag.replace(f'{{{default_ns}}}', '')
            if tag == 'license':
                repo.add(DisjunctiveLicense.from_xml(  # type:ignore[attr-defined]
                    li, default_ns))
            elif tag == 'expression':
                repo.add(LicenseExpression.from_xml(  # type:ignore[attr-defined]
                    li, default_ns))
            else:
                raise CycloneDxDeserializationException(f'unexpected: {li!r}')
        return repo
