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
from typing import List, Optional

from ..model import Note, Property, XsUri
from ..model.issue import IssueType


class ReleaseNotes:
    """
    This is our internal representation of a `releaseNotesType` for a Component in a BOM.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/#type_releaseNotesType
    """

    def __init__(self, type: str, title: Optional[str] = None, featured_image: Optional[XsUri] = None,
                 social_image: Optional[XsUri] = None, description: Optional[str] = None,
                 timestamp: Optional[datetime] = None, aliases: Optional[List[str]] = None,
                 tags: Optional[List[str]] = None, resolves: Optional[List[IssueType]] = None,
                 notes: Optional[List[Note]] = None, properties: Optional[List[Property]] = None) -> None:
        self.type = type
        self.title = title
        self.featured_image = featured_image
        self.social_image = social_image
        self.description = description
        self.timestamp = timestamp
        self.aliases = aliases
        self.tags = tags
        self.resolves = resolves
        self.notes = notes
        self._properties: Optional[List[Property]] = properties or None

    @property
    def type(self) -> str:
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

    @type.setter
    def type(self, type: str) -> None:
        self._type = type

    @property
    def title(self) -> Optional[str]:
        """
        The title of the release.
        """
        return self._title

    @title.setter
    def title(self, title: Optional[str]) -> None:
        self._title = title

    @property
    def featured_image(self) -> Optional[XsUri]:
        """
        The URL to an image that may be prominently displayed with the release note.
        """
        return self._featured_image

    @featured_image.setter
    def featured_image(self, featured_image: Optional[XsUri]) -> None:
        self._featured_image = featured_image

    @property
    def social_image(self) -> Optional[XsUri]:
        """
        The URL to an image that may be used in messaging on social media platforms.
        """
        return self._social_image

    @social_image.setter
    def social_image(self, social_image: Optional[XsUri]) -> None:
        self._social_image = social_image

    @property
    def description(self) -> Optional[str]:
        """
        A short description of the release.
        """
        return self._description

    @description.setter
    def description(self, description: Optional[str]) -> None:
        self._description = description

    @property
    def timestamp(self) -> Optional[datetime]:
        """
        The date and time (timestamp) when the release note was created.
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: Optional[datetime]) -> None:
        self._timestamp = timestamp

    @property
    def aliases(self) -> Optional[List[str]]:
        """
        One or more alternate names the release may be referred to. This may include unofficial terms used by
        development and marketing teams (e.g. code names).
        """
        return self._aliases

    @aliases.setter
    def aliases(self, aliases: Optional[List[str]]) -> None:
        if not aliases:
            aliases = None
        self._aliases = aliases

    def add_alias(self, alias: str) -> None:
        """
        Adds an alias to this Release.

        Args:
            alias:
                `str` alias
        """
        self.aliases = (self.aliases or []) + [alias]

    @property
    def tags(self) -> Optional[List[str]]:
        """
        One or more tags that may aid in search or retrieval of the release note.
        """
        return self._tags

    @tags.setter
    def tags(self, tags: Optional[List[str]]) -> None:
        if not tags:
            tags = None
        self._tags = tags

    def add_tag(self, tag: str) -> None:
        """
        Add a tag to this Release.

        Args:
            tag:
                `str` tag to add
        """
        self.tags = (self.tags or []) + [tag]

    @property
    def resolves(self) -> Optional[List[IssueType]]:
        """
        A collection of issues that have been resolved.
        """
        return self._resolves

    @resolves.setter
    def resolves(self, resolves: Optional[List[IssueType]]) -> None:
        if not resolves:
            resolves = None
        self._resolves = resolves

    def add_resolves(self, issue: IssueType) -> None:
        """
        Adds an issue that this Release resolves.

        Args:
            issue:
                `IssueType` object that is resolved by this Release
        """
        self.resolves = (self.resolves or []) + [issue]

    @property
    def notes(self) -> Optional[List[Note]]:
        """
        Zero or more release notes containing the locale and content. Multiple note elements may be specified to support
        release notes in a wide variety of languages.
        """
        return self._notes

    @notes.setter
    def notes(self, notes: Optional[List[Note]]) -> None:
        if not notes:
            notes = None
        self._notes = notes

    def add_note(self, note: Note) -> None:
        """
        Adds a release note to this Release.

        Args:
            note:
                `Note` to be added
        """
        self.notes = (self.notes or []) + [note]

    @property
    def properties(self) -> Optional[List[Property]]:
        """
        Provides the ability to document properties in a name-value store. This provides flexibility to include data not
        officially supported in the standard without having to use additional namespaces or create extensions. Unlike
        key-value stores, properties support duplicate names, each potentially having different values.

        Returns:
            List of `Property` or `None`
        """
        return self._properties

    @properties.setter
    def properties(self, properties: Optional[List[Property]]) -> None:
        self._properties = properties
