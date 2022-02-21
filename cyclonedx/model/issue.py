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
from typing import Iterable, Optional, Set

from . import XsUri
from ..exception.model import NoPropertiesProvidedException


class IssueClassification(Enum):
    """
    This is out internal representation of the enum `issueClassification`.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_issueClassification
    """
    DEFECT = 'defect'
    ENHANCEMENT = 'enhancement'
    SECURITY = 'security'


class IssueTypeSource:
    """
    This is out internal representation ofa source within the IssueType complex type that can be used in multiple
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

    def __hash__(self) -> int:
        return hash((self.name, self.url))

    def __repr__(self) -> str:
        return f'<IssueTypeSource name={self._name}, url={self.url}>'


class IssueType:
    """
    This is out internal representation of an IssueType complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_issueType
    """

    def __init__(self, *, classification: IssueClassification, id_: Optional[str] = None, name: Optional[str] = None,
                 description: Optional[str] = None, source: Optional[IssueTypeSource] = None,
                 references: Optional[Iterable[XsUri]] = None) -> None:
        self.type = classification
        self.id = id_
        self.name = name
        self.description = description
        self.source = source
        self.references = set(references or [])

    @property
    def type(self) -> IssueClassification:
        """
        Specifies the type of issue.

        Returns:
            `IssueClassification`
        """
        return self._type

    @type.setter
    def type(self, classification: IssueClassification) -> None:
        self._type = classification

    @property
    def id(self) -> Optional[str]:
        """
        The identifier of the issue assigned by the source of the issue.

        Returns:
            `str` if set else `None`
        """
        return self._id

    @id.setter
    def id(self, id_: Optional[str]) -> None:
        self._id = id_

    @property
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

    @property
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

    @property
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

    @property
    def references(self) -> Set[XsUri]:
        """
        Any reference URLs related to this issue.

        Returns:
            Set of `XsUri`
        """
        return self._references

    @references.setter
    def references(self, references: Iterable[XsUri]) -> None:
        self._references = set(references)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, IssueType):
            return hash(other) == hash(self)
        return False

    def __hash__(self) -> int:
        return hash((
            self.type, self.id, self.name, self.description, self.source, tuple(self.references)
        ))

    def __repr__(self) -> str:
        return f'<IssueType type={self.type}, id={self.id}, name={self.name}>'
