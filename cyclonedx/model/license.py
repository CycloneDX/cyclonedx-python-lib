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

from enum import Enum
from typing import TYPE_CHECKING, Any, Optional, Union
from warnings import warn

import attrs
from sortedcontainers import SortedSet

from .._internal.bom_ref import bom_ref_from_str as _bom_ref_from_str
from ..exception.model import MutuallyExclusivePropertiesException
from ..serialization import (
    METADATA_KEY_JSON_NAME,
    METADATA_KEY_VERSIONS,
    METADATA_KEY_XML_ATTR,
    METADATA_KEY_XML_NAME,
    METADATA_KEY_XML_SEQUENCE,
    VERSIONS_1_5_AND_LATER,
    VERSIONS_1_6_AND_LATER,
)
from . import AttachedText, XsUri
from .bom_ref import BomRef


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


def _bom_ref_converter(value: Optional[Union[str, BomRef]]) -> BomRef:
    """Convert string or BomRef to BomRef."""
    return _bom_ref_from_str(value)


@attrs.define(slots=False, on_setattr=attrs.setters.NO_OP)
class DisjunctiveLicense:
    """
    This is our internal representation of `licenseType` complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_licenseType
    """
    # Note: Either id or name must be provided, but not both
    id: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 1}
    )
    name: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 1}
    )
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
    text: Optional[AttachedText] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 2}
    )
    url: Optional[XsUri] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 3}
    )
    acknowledgement: Optional[LicenseAcknowledgement] = attrs.field(
        default=None,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_6_AND_LATER,
            METADATA_KEY_XML_ATTR: True,
        }
    )
    _initialized: bool = attrs.field(default=False, init=False, repr=False, eq=False, hash=False)

    def __attrs_post_init__(self) -> None:
        if not self.id and not self.name:
            raise MutuallyExclusivePropertiesException('Either `id` or `name` MUST be supplied')
        if self.id and self.name:
            warn(
                'Both `id` and `name` have been supplied - `name` will be ignored!',
                category=RuntimeWarning, stacklevel=2
            )
            object.__setattr__(self, 'name', None)
        object.__setattr__(self, '_initialized', True)

    def __setattr__(self, attr_name: str, value: Any) -> None:
        # Handle mutual exclusivity between id and name (only after initialization)
        if getattr(self, '_initialized', False):
            if attr_name == 'id' and value is not None:
                object.__setattr__(self, 'name', None)
            elif attr_name == 'name' and value is not None:
                object.__setattr__(self, 'id', None)
        object.__setattr__(self, attr_name, value)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DisjunctiveLicense):
            return (self.acknowledgement, self.id, self.name, self.url, self.text, self.bom_ref.value) == (
                other.acknowledgement, other.id, other.name, other.url, other.text, other.bom_ref.value)
        return NotImplemented

    @staticmethod
    def _cmp(val: Any) -> tuple:
        """Wrap value for None-safe comparison (None sorts last)."""
        return (0, val) if val is not None else (1, '')

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, DisjunctiveLicense):
            c = self._cmp
            return (c(self.acknowledgement), c(self.id), c(self.name), c(self.url), c(self.text),
                    c(self.bom_ref.value)) < (
                c(other.acknowledgement), c(other.id), c(other.name), c(other.url), c(other.text),
                c(other.bom_ref.value))
        if isinstance(other, LicenseExpression):
            return False  # self after any LicenseExpression
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.acknowledgement, self.id, self.name, self.url, self.text, self.bom_ref.value))

    def __repr__(self) -> str:
        return f'<License id={self.id!r}, name={self.name!r}>'


@attrs.define
class LicenseExpression:
    """
    This is our internal representation of `licenseType`'s expression type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition:
        https://cyclonedx.org/docs/1.7/json/#components_items_licenses_items_expression
    """
    value: str = attrs.field(
        metadata={
            METADATA_KEY_XML_NAME: '.',
            METADATA_KEY_JSON_NAME: 'expression',
        }
    )
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
    acknowledgement: Optional[LicenseAcknowledgement] = attrs.field(
        default=None,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_6_AND_LATER,
            METADATA_KEY_XML_ATTR: True,
        }
    )

    def __hash__(self) -> int:
        return hash((self.acknowledgement, self.value, self.bom_ref.value))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, LicenseExpression):
            return (self.acknowledgement, self.value, self.bom_ref.value) == (
                other.acknowledgement, other.value, other.bom_ref.value)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, LicenseExpression):
            return (self.acknowledgement, self.value, self.bom_ref.value) < (
                other.acknowledgement, other.value, other.bom_ref.value)
        if isinstance(other, DisjunctiveLicense):
            return True  # self before any DisjunctiveLicense
        return NotImplemented

    def __repr__(self) -> str:
        return f'<LicenseExpression value={self.value!r}>'


License = Union[LicenseExpression, DisjunctiveLicense]
"""TypeAlias for a union of supported license models.

- :class:`LicenseExpression`
- :class:`DisjunctiveLicense`
"""

if TYPE_CHECKING:  # pragma: no cover
    # workaround for https://github.com/python/mypy/issues/5264
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
