# encoding: utf-8

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

from enum import Enum
from typing import Any, Iterable, Optional

import serializable
from sortedcontainers import SortedSet

from ..exception.model import NoPropertiesProvidedException
from . import ComparableTuple, XsUri


class IssueClassification(str, Enum):
    """
    This is our internal representation of the enum `issueClassification`.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_issueClassification
    """
    DEFECT = 'defect'
    ENHANCEMENT = 'enhancement'
    SECURITY = 'security'


@serializable.serializable_class
class IssueTypeSource:
    """
    This is our internal representation ofa source within the IssueType complex type that can be used in multiple
    places within a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_issueType
    """

    def __init__(self, *, name: Optional[str] = None, url: Optional[XsUri] = None) -> None:
        if not name and not url:
            raise NoPropertiesProvidedException(
                'Neither `name` nor `url` were provided - at least one must be provided.'
            )
        self.name = name
        self.url = url

    @property
    def name(self) -> Optional[str]:
        """
        The name of the source. For example "National Vulnerability Database", "NVD", and "Apache".

        Returns:
            `str` if set else `None`
        """
        return self._name

    @name.setter
    def name(self, name: Optional[str]) -> None:
        self._name = name

    @property
    def url(self) -> Optional[XsUri]:
        """
        Optional url of the issue documentation as provided by the source.

        Returns:
            `XsUri` if set else `None`
        """
        return self._url

    @url.setter
    def url(self, url: Optional[XsUri]) -> None:
        self._url = url

    def __eq__(self, other: object) -> bool:
        if isinstance(other, IssueTypeSource):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, IssueTypeSource):
            return ComparableTuple((self.name, self.url)) < ComparableTuple((other.name, other.url))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.name, self.url))

    def __repr__(self) -> str:
        return f'<IssueTypeSource name={self._name}, url={self.url}>'


@serializable.serializable_class
class IssueType:
    """
    This is our internal representation of an IssueType complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_issueType
    """

    def __init__(self, *, type_: IssueClassification, id_: Optional[str] = None, name: Optional[str] = None,
                 description: Optional[str] = None, source: Optional[IssueTypeSource] = None,
                 references: Optional[Iterable[XsUri]] = None) -> None:
        self.type_ = type_
        self.id_ = id_
        self.name = name
        self.description = description
        self.source = source
        self.references = references or []  # type: ignore

    @property  # type: ignore[misc]
    @serializable.xml_attribute()
    def type_(self) -> IssueClassification:
        """
        Specifies the type of issue.

        Returns:
            `IssueClassification`
        """
        return self._type

    @type_.setter
    def type_(self, type_: IssueClassification) -> None:
        self._type = type_

    @property  # type: ignore[misc]
    @serializable.xml_sequence(1)
    def id_(self) -> Optional[str]:
        """
        The identifier of the issue assigned by the source of the issue.

        Returns:
            `str` if set else `None`
        """
        return self._id

    @id_.setter
    def id_(self, id_: Optional[str]) -> None:
        self._id = id_

    @property  # type: ignore[misc]
    @serializable.xml_sequence(2)
    def name(self) -> Optional[str]:
        """
        The name of the issue.

        Returns:
            `str` if set else `None`
        """
        return self._name

    @name.setter
    def name(self, name: Optional[str]) -> None:
        self._name = name

    @property  # type: ignore[misc]
    @serializable.xml_sequence(3)
    def description(self) -> Optional[str]:
        """
        A description of the issue.

        Returns:
            `str` if set else `None`
        """
        return self._description

    @description.setter
    def description(self, description: Optional[str]) -> None:
        self._description = description

    @property  # type: ignore[misc]
    @serializable.xml_sequence(4)
    def source(self) -> Optional[IssueTypeSource]:
        """
        The source of this issue.

        Returns:
            `IssueTypeSource` if set else `None`
        """
        return self._source

    @source.setter
    def source(self, source: Optional[IssueTypeSource]) -> None:
        self._source = source

    @property  # type: ignore[misc]
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'url')
    @serializable.xml_sequence(5)
    def references(self) -> "SortedSet[XsUri]":
        """
        Any reference URLs related to this issue.

        Returns:
            Set of `XsUri`
        """
        return self._references

    @references.setter
    def references(self, references: Iterable[XsUri]) -> None:
        self._references = SortedSet(references)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, IssueType):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, IssueType):
            return ComparableTuple((self.type_, self.id_, self.name, self.description, self.source)) < \
                ComparableTuple((other.type_, other.id_, other.name, other.description, other.source))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((
            self.type_, self.id_, self.name, self.description, self.source, tuple(self.references)
        ))

    def __repr__(self) -> str:
        return f'<IssueType type={self.type_}, id={self.id_}, name={self.name}>'
