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


from collections.abc import Iterable
from typing import Any, Optional, Union

import attrs
from sortedcontainers import SortedSet

from .._internal.bom_ref import bom_ref_from_str as _bom_ref_from_str
from .._internal.compare import ComparableTuple as _ComparableTuple
from ..serialization import (
    METADATA_KEY_JSON_NAME,
    METADATA_KEY_VERSIONS,
    METADATA_KEY_XML_ATTR,
    METADATA_KEY_XML_NAME,
    METADATA_KEY_XML_SEQUENCE,
    VERSIONS_1_5_AND_LATER,
    VERSIONS_1_6_AND_LATER,
)
from . import XsUri
from .bom_ref import BomRef


def _bom_ref_converter(value: Optional[Union[str, BomRef]]) -> BomRef:
    """Convert string or BomRef to BomRef."""
    return _bom_ref_from_str(value)


def _sortedset_factory() -> SortedSet:
    """Factory for creating empty SortedSet."""
    return SortedSet()


def _sortedset_converter(value: Any) -> SortedSet:
    """Convert a value to SortedSet."""
    if value is None:
        return SortedSet()
    if isinstance(value, SortedSet):
        return value
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes, dict)):
        return SortedSet(value)
    return SortedSet([value])


@attrs.define
class PostalAddress:
    """
    This is our internal representation of the `postalAddressType` complex type that can be used in multiple places
    within a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_postalAddressType
    """
    bom_ref: BomRef = attrs.field(
        factory=BomRef,
        converter=_bom_ref_converter,
        metadata={
            METADATA_KEY_XML_ATTR: True,
            METADATA_KEY_XML_NAME: 'bom-ref',
            METADATA_KEY_JSON_NAME: 'bom-ref',
        }
    )
    country: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 10}
    )
    region: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 20}
    )
    locality: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 30}
    )
    post_office_box_number: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 40}
    )
    postal_code: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 60}
    )
    street_address: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 70}
    )

    @staticmethod
    def _cmp(val: Any) -> tuple:
        """Wrap value for None-safe comparison (None sorts last)."""
        return (0, val) if val is not None else (1, '')

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, PostalAddress):
            c = self._cmp
            return (
                c(self.country), c(self.region), c(self.locality), c(self.postal_code),
                c(self.post_office_box_number), c(self.street_address), c(self.bom_ref.value)
            ) < (
                c(other.country), c(other.region), c(other.locality), c(other.postal_code),
                c(other.post_office_box_number), c(other.street_address), c(other.bom_ref.value)
            )
        return NotImplemented

    def __hash__(self) -> int:
        return hash((
            self.country, self.region, self.locality, self.postal_code,
            self.post_office_box_number, self.street_address, self.bom_ref.value
        ))

    def __repr__(self) -> str:
        return f'<PostalAddress bom-ref={self.bom_ref}, street_address={self.street_address}, country={self.country}>'


@attrs.define
class OrganizationalContact:
    """
    This is our internal representation of the `organizationalContact` complex type that can be used in multiple places
    within a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_organizationalContact
    """
    bom_ref: BomRef = attrs.field(
        factory=BomRef,
        converter=_bom_ref_converter,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_5_AND_LATER,
            METADATA_KEY_XML_ATTR: True,
            METADATA_KEY_XML_NAME: 'bom-ref',
            METADATA_KEY_JSON_NAME: 'bom-ref',
        }
    )
    name: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 1}
    )
    email: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 2}
    )
    phone: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 3}
    )

    @staticmethod
    def _cmp(val: Any) -> tuple:
        """Wrap value for None-safe comparison (None sorts last)."""
        return (0, val) if val is not None else (1, '')

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, OrganizationalContact):
            return (self._cmp(self.name), self._cmp(self.email), self._cmp(self.phone),
                    self._cmp(self.bom_ref.value)) < (
                self._cmp(other.name), self._cmp(other.email), self._cmp(other.phone),
                self._cmp(other.bom_ref.value))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.name, self.email, self.phone, self.bom_ref.value))

    def __repr__(self) -> str:
        return f'<OrganizationalContact name={self.name}, email={self.email}, phone={self.phone}>'


def _sortedset_factory() -> SortedSet:
    return SortedSet()


@attrs.define
class OrganizationalEntity:
    """
    This is our internal representation of the `organizationalEntity` complex type that can be used in multiple places
    within a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_organizationalEntity
    """
    bom_ref: BomRef = attrs.field(
        factory=BomRef,
        converter=_bom_ref_converter,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_5_AND_LATER,
            METADATA_KEY_XML_ATTR: True,
            METADATA_KEY_XML_NAME: 'bom-ref',
            METADATA_KEY_JSON_NAME: 'bom-ref',
        }
    )
    name: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 10}
    )
    address: Optional[PostalAddress] = attrs.field(
        default=None,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_6_AND_LATER,
            METADATA_KEY_XML_SEQUENCE: 20,
        }
    )
    urls: 'SortedSet[XsUri]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={
            METADATA_KEY_JSON_NAME: 'url',
            METADATA_KEY_XML_SEQUENCE: 30,
        }
    )
    contacts: 'SortedSet[OrganizationalContact]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={
            METADATA_KEY_JSON_NAME: 'contact',
            METADATA_KEY_XML_SEQUENCE: 40,
        }
    )

    @urls.validator
    def _validate_urls(self, attribute: attrs.Attribute, value: Any) -> None:
        if value is not None and not isinstance(value, SortedSet):
            object.__setattr__(self, 'urls', SortedSet(value))

    @contacts.validator
    def _validate_contacts(self, attribute: attrs.Attribute, value: Any) -> None:
        if value is not None and not isinstance(value, SortedSet):
            object.__setattr__(self, 'contacts', SortedSet(value))

    @staticmethod
    def _cmp(val: Any) -> tuple:
        """Wrap value for None-safe comparison (None sorts last)."""
        return (0, val) if val is not None else (1, '')

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, OrganizationalEntity):
            return (self._cmp(self.name), tuple(self.urls), tuple(self.contacts),
                    self._cmp(self.bom_ref.value)) < (
                self._cmp(other.name), tuple(other.urls), tuple(other.contacts),
                self._cmp(other.bom_ref.value))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.name, tuple(self.urls), tuple(self.contacts), self.bom_ref.value))

    def __repr__(self) -> str:
        return f'<OrganizationalEntity name={self.name}>'
