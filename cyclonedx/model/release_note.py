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
from datetime import datetime
from typing import Any, Optional

import attrs
from sortedcontainers import SortedSet

from ..model import Note, Property, XsUri
from ..model.issue import IssueType
from ..serialization import METADATA_KEY_XML_SEQUENCE


def _sortedset_factory() -> SortedSet:
    return SortedSet()


def _sortedset_converter(value: Any) -> SortedSet:
    if value is None:
        return SortedSet()
    if isinstance(value, SortedSet):
        return value
    return SortedSet(value)


@attrs.define
class ReleaseNotes:
    """
    This is our internal representation of a `releaseNotesType` for a Component in a BOM.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_releaseNotesType
    """
    type: str = attrs.field(
        metadata={METADATA_KEY_XML_SEQUENCE: 1}
    )
    title: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 2}
    )
    featured_image: Optional[XsUri] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 3}
    )
    social_image: Optional[XsUri] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 4}
    )
    description: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 5}
    )
    timestamp: Optional[datetime] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 6}
    )
    aliases: 'SortedSet[str]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={METADATA_KEY_XML_SEQUENCE: 7}
    )
    tags: 'SortedSet[str]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={METADATA_KEY_XML_SEQUENCE: 8}
    )
    resolves: 'SortedSet[IssueType]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={METADATA_KEY_XML_SEQUENCE: 9}
    )
    notes: 'SortedSet[Note]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={METADATA_KEY_XML_SEQUENCE: 10}
    )
    properties: 'SortedSet[Property]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={METADATA_KEY_XML_SEQUENCE: 11}
    )

    def __lt__(self, other: object) -> bool:
        if isinstance(other, ReleaseNotes):
            return (
                self.type, self.title, self.featured_image, self.social_image,
                self.description, self.timestamp, tuple(self.aliases), tuple(self.tags),
                tuple(self.resolves), tuple(self.notes), tuple(self.properties)
            ) < (
                other.type, other.title, other.featured_image, other.social_image,
                other.description, other.timestamp, tuple(other.aliases), tuple(other.tags),
                tuple(other.resolves), tuple(other.notes), tuple(other.properties)
            )
        return NotImplemented

    def __hash__(self) -> int:
        return hash((
            self.type, self.title, self.featured_image, self.social_image,
            self.description, self.timestamp, tuple(self.aliases), tuple(self.tags),
            tuple(self.resolves), tuple(self.notes), tuple(self.properties)
        ))

    def __repr__(self) -> str:
        return f'<ReleaseNotes type={self.type}, title={self.title}>'
