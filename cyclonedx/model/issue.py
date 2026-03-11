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

from ..serialization import ALL_VERSIONS
from ..schema import SchemaVersion
from collections.abc import Iterable
from enum import Enum
from typing import Any, Optional

import attrs
from sortedcontainers import SortedSet

from ..serialization import METADATA_KEY_XML_ATTR, METADATA_KEY_XML_SEQUENCE
from . import XsUri


class IssueClassification(str, Enum):
    """
    This is our internal representation of the enum `issueClassification`.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_issueClassification
    """
    DEFECT = 'defect'
    ENHANCEMENT = 'enhancement'
    SECURITY = 'security'


# Issue classification support by schema version
ISSUE_CLASSIFICATION_VERSIONS: dict[IssueClassification, set[SchemaVersion]] = {
    IssueClassification.DEFECT: ALL_VERSIONS,
    IssueClassification.ENHANCEMENT: ALL_VERSIONS,
    IssueClassification.SECURITY: ALL_VERSIONS,
}


@attrs.define
class IssueTypeSource:
    """
    This is our internal representation of a source within the IssueType complex type that can be used in multiple
    places within a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition:
        https://cyclonedx.org/docs/1.7/json/#components_items_pedigree_patches_items_resolves_items_source
    """
    name: Optional[str] = attrs.field(default=None)
    url: Optional[XsUri] = attrs.field(default=None)

    @staticmethod
    def _cmp(val: Any) -> tuple:
        """Wrap value for None-safe comparison (None sorts last)."""
        return (0, val) if val is not None else (1, '')

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, IssueTypeSource):
            return (self._cmp(self.name), self._cmp(self.url)) < (self._cmp(other.name), self._cmp(other.url))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.name, self.url))

    def __repr__(self) -> str:
        return f'<IssueTypeSource name={self.name}, url={self.url}>'


def _sortedset_factory() -> SortedSet:
    return SortedSet()


def _sortedset_converter(value: Any) -> SortedSet:
    if value is None:
        return SortedSet()
    if isinstance(value, SortedSet):
        return value
    return SortedSet(value)


@attrs.define
class IssueType:
    """
    This is our internal representation of an IssueType complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_issueType
    """
    type: IssueClassification = attrs.field(
        metadata={METADATA_KEY_XML_ATTR: True}
    )
    id: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 1}
    )
    name: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 2}
    )
    description: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 3}
    )
    source: Optional[IssueTypeSource] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 4}
    )
    references: 'SortedSet[XsUri]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={METADATA_KEY_XML_SEQUENCE: 5}
    )

    @staticmethod
    def _cmp_issue(val: Any) -> tuple:
        """Wrap value for None-safe comparison (None sorts last)."""
        return (0, val) if val is not None else (1, '')

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, IssueType):
            c = self._cmp_issue
            return (self.type, c(self.id), c(self.name), c(self.description), c(self.source), tuple(self.references)) < (
                other.type, c(other.id), c(other.name), c(other.description), c(other.source), tuple(other.references))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.type, self.id, self.name, self.description, self.source, tuple(self.references)))

    def __repr__(self) -> str:
        return f'<IssueType type={self.type}, id={self.id}, name={self.name}>'
