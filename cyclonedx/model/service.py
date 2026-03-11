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


from .._internal.bom_ref import bom_ref_from_str as _bom_ref_from_str
from .release_note import ReleaseNotes
from .license import License, LicenseRepository
from .dependency import Dependable
from .contact import OrganizationalEntity
from .bom_ref import BomRef
from . import DataClassification, ExternalReference, Property, XsUri
from ..serialization import (
    METADATA_KEY_JSON_NAME,
    METADATA_KEY_VERSIONS,
    METADATA_KEY_XML_ATTR,
    METADATA_KEY_XML_NAME,
    METADATA_KEY_XML_SEQUENCE,
    VERSIONS_1_3_AND_LATER,
    VERSIONS_1_4_AND_LATER,
)
from collections.abc import Iterable
from typing import Any, Optional, Union

import attrs
from sortedcontainers import SortedSet


def _sortedset_converter(value: Any) -> SortedSet:
    """Converter to ensure values are always SortedSet."""
    if value is None:
        return SortedSet()
    if isinstance(value, SortedSet):
        return value
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes, dict)):
        return SortedSet(value)
    return SortedSet([value])


def _bom_ref_converter(value: Optional[Union[str, BomRef]]) -> BomRef:
    """Convert string or BomRef to BomRef."""
    return _bom_ref_from_str(value)


def _sortedset_factory() -> SortedSet:
    return SortedSet()


def _license_repository_factory() -> LicenseRepository:
    return LicenseRepository()


def _license_repository_converter(value: Any) -> LicenseRepository:
    """Convert a value to LicenseRepository."""
    if value is None:
        return LicenseRepository()
    if isinstance(value, LicenseRepository):
        return value
    # Convert generators, lists, etc. to LicenseRepository
    return LicenseRepository(value)


@attrs.define
class Service(Dependable):
    """
    Class that models the `service` complex type in the CycloneDX schema.

    .. note::
        See the CycloneDX schema: https://cyclonedx.org/docs/1.7/xml/#type_service
    """
    name: str = attrs.field(
        metadata={METADATA_KEY_XML_SEQUENCE: 3}
    )
    bom_ref: BomRef = attrs.field(
        factory=BomRef,
        converter=_bom_ref_converter,
        metadata={
            METADATA_KEY_JSON_NAME: 'bom-ref',
            METADATA_KEY_XML_ATTR: True,
            METADATA_KEY_XML_NAME: 'bom-ref',
        }
    )
    provider: Optional[OrganizationalEntity] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 1}
    )
    group: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 2}
    )
    version: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 4}
    )
    description: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 5}
    )
    endpoints: 'SortedSet[XsUri]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={METADATA_KEY_XML_SEQUENCE: 6}
    )
    authenticated: Optional[bool] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 7}
    )
    x_trust_boundary: Optional[bool] = attrs.field(
        default=None,
        metadata={
            METADATA_KEY_JSON_NAME: 'x-trust-boundary',
            METADATA_KEY_XML_NAME: 'x-trust-boundary',
            METADATA_KEY_XML_SEQUENCE: 8,
        }
    )
    data: 'SortedSet[DataClassification]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={METADATA_KEY_XML_SEQUENCE: 10}
    )
    licenses: LicenseRepository = attrs.field(
        factory=_license_repository_factory,
        converter=_license_repository_converter,
        metadata={METADATA_KEY_XML_SEQUENCE: 11}
    )
    external_references: 'SortedSet[ExternalReference]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={METADATA_KEY_XML_SEQUENCE: 12}
    )
    properties: 'SortedSet[Property]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_3_AND_LATER,
            METADATA_KEY_XML_SEQUENCE: 13,
        }
    )
    services: 'SortedSet[Service]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={METADATA_KEY_XML_SEQUENCE: 14}
    )
    release_notes: Optional[ReleaseNotes] = attrs.field(
        default=None,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_4_AND_LATER,
            METADATA_KEY_XML_SEQUENCE: 15,
        }
    )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Service):
            return (
                self.group, self.name, self.version, self.bom_ref.value,
                self.provider, self.description, self.authenticated,
                tuple(self.data), tuple(self.endpoints), tuple(self.external_references),
                tuple(self.licenses), tuple(self.properties), self.release_notes,
                tuple(self.services), self.x_trust_boundary
            ) == (
                other.group, other.name, other.version, other.bom_ref.value,
                other.provider, other.description, other.authenticated,
                tuple(other.data), tuple(other.endpoints), tuple(other.external_references),
                tuple(other.licenses), tuple(other.properties), other.release_notes,
                tuple(other.services), other.x_trust_boundary
            )
        return NotImplemented

    @staticmethod
    def _none_safe(val: Any) -> tuple:
        """Convert value to tuple for safe comparison (None sorts last)."""
        return (0, val) if val is not None else (1, '')

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Service):
            # Use _none_safe to handle None values in comparisons
            return (
                self._none_safe(self.group), self.name, self._none_safe(self.version),
                self._none_safe(self.bom_ref.value),
                self._none_safe(self.provider), self._none_safe(self.description),
                self._none_safe(self.authenticated),
                tuple(self.data), tuple(self.endpoints), tuple(self.external_references),
                tuple(self.licenses), tuple(self.properties), self.release_notes,
                tuple(self.services), self._none_safe(self.x_trust_boundary)
            ) < (
                self._none_safe(other.group), other.name, self._none_safe(other.version),
                self._none_safe(other.bom_ref.value),
                self._none_safe(other.provider), self._none_safe(other.description),
                self._none_safe(other.authenticated),
                tuple(other.data), tuple(other.endpoints), tuple(other.external_references),
                tuple(other.licenses), tuple(other.properties), other.release_notes,
                tuple(other.services), self._none_safe(other.x_trust_boundary)
            )
        return NotImplemented

    def __hash__(self) -> int:
        return hash((
            self.group, self.name, self.version, self.bom_ref.value,
            self.provider, self.description, self.authenticated,
            tuple(self.data), tuple(self.endpoints), tuple(self.external_references),
            tuple(self.licenses), tuple(self.properties), self.release_notes,
            tuple(self.services), self.x_trust_boundary
        ))

    def __repr__(self) -> str:
        return f'<Service bom-ref={self.bom_ref}, group={self.group}, name={self.name}, version={self.version}>'
