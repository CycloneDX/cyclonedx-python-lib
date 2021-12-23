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
import datetime
from typing import List, Optional

from ..model import IssueType, Note, Properties, XsUri


class ReleaseNotes:
    """
    This is our internal representation of a `releaseNotesType` for a Component in a BOM.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/#type_releaseNotesType
    """

    def __init__(self, type: str, title: Optional[str] = None, featured_image: Optional[XsUri] = None,
                 social_image: Optional[XsUri] = None, description: Optional[str] = None,
                 timestamp: Optional[datetime.datetime] = None, aliases: Optional[List[str]] = None,
                 tags: Optional[List[str]] = None, resolves: Optional[List[IssueType]] = None,
                 notes: Optional[List[Note]] = None, properties: Optional[Properties] = None) -> None:
        self._type: str = type
        self._title: Optional[str] = title
        self._featured_image: Optional[XsUri] = featured_image
        self._social_image: Optional[XsUri] = social_image
        self._description: Optional[str] = description
        self._timestamp: Optional[datetime.datetime] = timestamp
        self._aliases: Optional[List[str]] = aliases or None
        self._tags: Optional[List[str]] = tags or None
        self._resolves: Optional[List[IssueType]] = resolves or None
        self._notes: Optional[List[Note]] = notes or None
        self._properties: Optional[Properties] = properties or None

    def add_alias(self, alias: str) -> None:
        """
        Adds an alias to this Release.

        An alias is an alternate name the release may be referred to. This may include unofficial terms used by
        development and marketing teams (e.g. code names).

        Args:
            alias:
                `str` alias
        """
        self._aliases.append(alias)

    def add_tag(self, tag: str) -> None:
        """
        Adds a tag to this Release.

        Tags may aid in search or retrieval of the release note.

        Args:
            tag:
                `str` tag to add
        """
        self._tags.append(tag)

    def add_resolves(self, issue: IssueType) -> None:
        """
        Adds an issue that this Release resolves.

        Args:
            issue:
                `IssueType` object that is resolved by this Release
        """
        self._resolves.append(issue)

    def add_note(self, note: Note) -> None:
        """
        Adds a Release Note to this Release.

        Multiple note elements may be specified to support release notes in a wide variety of languages.

        Args:
            note:
                `Note` to be added
        """
        self._notes.append(note)

    def get_type(self) -> str:
        """
        Get all the type for this Release.

        The software versioning type. It is RECOMMENDED that the release type use one of 'major', 'minor', 'patch',
        'pre-release', or 'internal'.

        Representing all possible software release types is not practical, so standardizing on the recommended values,
        whenever possible, is strongly encouraged.

        * major = A major release may contain significant changes or may introduce breaking changes.
        * minor = A minor release, also known as an update, may contain a smaller number of changes than major releases.
        * patch = Patch releases are typically unplanned and may resolve defects or important security issues.
        * pre-release = A pre-release may include alpha, beta, or release candidates and typically have limited support.
            They provide the ability to preview a release prior to its general availability.
        * internal = Internal releases are not for public consumption and are intended to be used exclusively by the
            project or manufacturer that produced it.

        Returns:
             `str`
        """
        return self._type

    def get_title(self) -> Optional[str]:
        """
        Get the title of this Release.

        Returns:
            `str` release title if set or `None`.
        """
        return self._title

    def get_featured_image(self) -> Optional[XsUri]:
        """
        Get the featured image for this Release.

        The URL to an image that may be prominently displayed with the release note.

        Returns:
            `XsUri` for the featured image if set else `None`.
        """
        return self._featured_image

    def get_social_image(self) -> Optional[XsUri]:
        """
        Get the social image for this Release.

        The URL to an image that may be used in messaging on social media platforms.

        Returns:
            `XsUri` for the social image if set else `None`.
        """
        return self._social_image

    def get_description(self) -> Optional[str]:
        """
        Get the description of this Release.

        A short description of the release.

        Returns:
            `str` description if set or `None`.
        """
        return self._description

    def get_timestamp(self) -> Optional[datetime.datetime]:
        """
        Get the date and time (timestamp) when the release note was created.

        Returns:
            `datetime.datetime` timestamp if set or `None`.
        """
        return self._timestamp

    def get_aliases(self) -> Optional[List[str]]:
        """
        Get any alternate names the release may be referred to.

        This may include unofficial terms used by development and marketing teams (e.g. code names).

        Returns:
            `List[str]` list of alternative names or aliases if there are any or `None`.
        """
        return self._aliases

    def get_tags(self) -> Optional[List[str]]:
        """
        Get any tags that may aid in search or retrieval of the release note.

        Returns:
            `List[str]` list of tags if there are any or `None`.
        """
        return self._tags

    def get_resolves(self) -> Optional[List[IssueType]]:
        """
        Get a collection of issues that have been resolved by this Release.

        Returns:
            `List[IssueType]` list of issues resolved by this Release if there are any or `None`.
        """
        return self._resolves

    def get_notes(self) -> Optional[List[Note]]:
        """
        Get any release notes containing the locale and content.

        Multiple note elements may be specified to support release notes in a wide variety of languages.

        Returns:
            `List[Note]` list of releases notes if there are any or `None`.
        """
        return self._notes

    def get_properties(self) -> Optional[Properties]:
        """
        Get any document properties in a name-value store.

        These provide for a flexibility to include data not officially supported in the standard without having to use
        additional namespaces or create extensions. Unlike key-value stores, properties support duplicate names, each
        potentially having different values.

        Returns:
            `Properties` object if set or `None`.
        """
        return self._properties
