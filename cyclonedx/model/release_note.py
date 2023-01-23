# encoding: utf-8

# This file is part of CycloneDX Python Lib
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

from datetime import datetime
from typing import Iterable, Optional

import serializable
from sortedcontainers import SortedSet

from ..model import Note, Property, XsUri
from ..model.issue import IssueType


@serializable.serializable_class
class ReleaseNotes:
    """
    This is our internal representation of a `releaseNotesType` for a Component in a BOM.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/#type_releaseNotesType
    """

    def __init__(self, *, type_: str, title: Optional[str] = None, featured_image: Optional[XsUri] = None,
                 social_image: Optional[XsUri] = None, description: Optional[str] = None,
                 timestamp: Optional[datetime] = None, aliases: Optional[Iterable[str]] = None,
                 tags: Optional[Iterable[str]] = None, resolves: Optional[Iterable[IssueType]] = None,
                 notes: Optional[Iterable[Note]] = None, properties: Optional[Iterable[Property]] = None) -> None:
        self.type_ = type_
        self.title = title
        self.featured_image = featured_image
        self.social_image = social_image
        self.description = description
        self.timestamp = timestamp
        self.aliases = aliases or []  # type: ignore
        self.tags = tags or []  # type: ignore
        self.resolves = resolves or []  # type: ignore
        self.notes = notes or []  # type: ignore
        self.properties = properties or []  # type: ignore

    @property  # type: ignore[misc]
    @serializable.xml_sequence(1)
    def type_(self) -> str:
        """
        The software versioning type.

        It is **RECOMMENDED** that the release type use one of 'major', 'minor', 'patch', 'pre-release', or 'internal'.

        Representing all possible software release types is not practical, so standardizing on the recommended values,
        whenever possible, is strongly encouraged.

        * **major** = A major release may contain significant changes or may introduce breaking changes.
        * **minor** = A minor release, also known as an update, may contain a smaller number of changes than major
            releases.
        * **patch** = Patch releases are typically unplanned and may resolve defects or important security issues.
        * **pre-release** = A pre-release may include alpha, beta, or release candidates and typically have limited
            support. They provide the ability to preview a release prior to its general availability.
        * **internal** = Internal releases are not for public consumption and are intended to be used exclusively by the
            project or manufacturer that produced it.
        """
        return self._type

    @type_.setter
    def type_(self, type_: str) -> None:
        self._type = type_

    @property  # type: ignore[misc]
    @serializable.xml_sequence(2)
    def title(self) -> Optional[str]:
        """
        The title of the release.
        """
        return self._title

    @title.setter
    def title(self, title: Optional[str]) -> None:
        self._title = title

    @property  # type: ignore[misc]
    @serializable.xml_sequence(3)
    def featured_image(self) -> Optional[XsUri]:
        """
        The URL to an image that may be prominently displayed with the release note.
        """
        return self._featured_image

    @featured_image.setter
    def featured_image(self, featured_image: Optional[XsUri]) -> None:
        self._featured_image = featured_image

    @property  # type: ignore[misc]
    @serializable.xml_sequence(4)
    def social_image(self) -> Optional[XsUri]:
        """
        The URL to an image that may be used in messaging on social media platforms.
        """
        return self._social_image

    @social_image.setter
    def social_image(self, social_image: Optional[XsUri]) -> None:
        self._social_image = social_image

    @property  # type: ignore[misc]
    @serializable.xml_sequence(5)
    def description(self) -> Optional[str]:
        """
        A short description of the release.
        """
        return self._description

    @description.setter
    def description(self, description: Optional[str]) -> None:
        self._description = description

    @property  # type: ignore[misc]
    @serializable.type_mapping(serializable.helpers.XsdDateTime)
    @serializable.xml_sequence(6)
    def timestamp(self) -> Optional[datetime]:
        """
        The date and time (timestamp) when the release note was created.
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: Optional[datetime]) -> None:
        self._timestamp = timestamp

    @property  # type: ignore[misc]
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'alias')
    @serializable.xml_sequence(7)
    def aliases(self) -> "SortedSet[str]":
        """
        One or more alternate names the release may be referred to. This may include unofficial terms used by
        development and marketing teams (e.g. code names).

        Returns:
            Set of `str`
        """
        return self._aliases

    @aliases.setter
    def aliases(self, aliases: Iterable[str]) -> None:
        self._aliases = SortedSet(aliases)

    @property  # type: ignore[misc]
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'tag')
    @serializable.xml_sequence(8)
    def tags(self) -> "SortedSet[str]":
        """
        One or more tags that may aid in search or retrieval of the release note.

        Returns:
            Set of `str`
        """
        return self._tags

    @tags.setter
    def tags(self, tags: Iterable[str]) -> None:
        self._tags = SortedSet(tags)

    @property  # type: ignore[misc]
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'issue')
    @serializable.xml_sequence(9)
    def resolves(self) -> "SortedSet[IssueType]":
        """
        A collection of issues that have been resolved.

        Returns:
            Set of `IssueType`
        """
        return self._resolves

    @resolves.setter
    def resolves(self, resolves: Iterable[IssueType]) -> None:
        self._resolves = SortedSet(resolves)

    @property  # type: ignore[misc]
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'note')
    @serializable.xml_sequence(10)
    def notes(self) -> "SortedSet[Note]":
        """
        Zero or more release notes containing the locale and content. Multiple note elements may be specified to support
        release notes in a wide variety of languages.

        Returns:
            Set of `Note`
        """
        return self._notes

    @notes.setter
    def notes(self, notes: Iterable[Note]) -> None:
        self._notes = SortedSet(notes)

    @property  # type: ignore[misc]
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'property')
    @serializable.xml_sequence(11)
    def properties(self) -> "SortedSet[Property]":
        """
        Provides the ability to document properties in a name-value store. This provides flexibility to include data not
        officially supported in the standard without having to use additional namespaces or create extensions. Unlike
        key-value stores, properties support duplicate names, each potentially having different values.

        Returns:
            Set of `Property`
        """
        return self._properties

    @properties.setter
    def properties(self, properties: Iterable[Property]) -> None:
        self._properties = SortedSet(properties)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ReleaseNotes):
            return hash(other) == hash(self)
        return False

    def __hash__(self) -> int:
        return hash((
            self.type_, self.title, self.featured_image, self.social_image, self.description, self.timestamp,
            tuple(self.aliases), tuple(self.tags), tuple(self.resolves), tuple(self.notes), tuple(self.properties)
        ))

    def __repr__(self) -> str:
        return f'<ReleaseNotes type={self.type_}, title={self.title}>'
