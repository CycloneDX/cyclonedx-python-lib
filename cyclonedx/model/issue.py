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

from enum import Enum
from typing import List, Optional

from . import XsUri
from ..exception.model import NoPropertiesProvidedException


class IssueClassification(Enum):
    """
    This is out internal representation of the enum `issueClassification`.

    .. note::
        See the CycloneDX Schema definition: hhttps://cyclonedx.org/docs/1.4/xml/#type_issueClassification
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

    def __init__(self, name: Optional[str] = None, url: Optional[XsUri] = None) -> None:
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


class IssueType:
    """
    This is out internal representation of an IssueType complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_issueType
    """

    def __init__(self, classification: IssueClassification, id: Optional[str] = None, name: Optional[str] = None,
                 description: Optional[str] = None, source_name: Optional[str] = None,
                 source_url: Optional[XsUri] = None, references: Optional[List[XsUri]] = None) -> None:
        self._type: IssueClassification = classification
        self._id: Optional[str] = id
        self._name: Optional[str] = name
        self._description: Optional[str] = description
        self._source: Optional[IssueTypeSource] = None
        self._references: List[XsUri] = references or []
        if source_name or source_url:
            self._source = IssueTypeSource(
                name=source_name, url=source_url
            )

    @property
    def source(self) -> Optional[IssueTypeSource]:
        return self._source

    @source.setter
    def source(self, source: IssueTypeSource) -> None:
        self._source = source

    def add_reference(self, reference: XsUri) -> None:
        """
        Add a reference URL to this Issue.

        Args:
            reference:
                `XsUri` Reference URL to add
        """
        self._references.append(reference)

    def get_classification(self) -> IssueClassification:
        """
        Get the classification of this IssueType.

        Returns:
            `IssueClassification` that represents the classification of this `IssueType`.
        """
        return self._type

    def get_id(self) -> Optional[str]:
        """
        Get the ID of this IssueType.

        Returns:
            `str` that represents the ID of this `IssueType` if set else `None`.
        """
        return self._id

    def get_name(self) -> Optional[str]:
        """
        Get the name of this IssueType.

        Returns:
            `str` that represents the name of this `IssueType` if set else `None`.
        """
        return self._name

    def get_description(self) -> Optional[str]:
        """
        Get the description of this IssueType.

        Returns:
            `str` that represents the description of this `IssueType` if set else `None`.
        """
        return self._description

    def get_source_name(self) -> Optional[str]:
        """
        Get the source_name of this IssueType.

        For example, this might be "NVD" or "National Vulnerability Database".

        Returns:
            `str` that represents the source_name of this `IssueType` if set else `None`.
        """
        if self._source:
            return self._source.name
        return None

    def get_source_url(self) -> Optional[XsUri]:
        """
        Get the source_url of this IssueType.

        For example, this would likely be a URL to the issue on the NVD.

        Returns:
            `XsUri` that represents the source_url of this `IssueType` if set else `None`.
        """
        if self._source:
            return self._source.url
        return None

    def get_references(self) -> List[XsUri]:
        """
        Get any references for this IssueType.

        References are an arbitrary list of URIs that relate to this issue.

        Returns:
            List of `XsUri` objects.
        """
        return self._references

    def set_id(self, id: str) -> None:
        """
        Set the ID of this Issue.

        Args:
            id:
                `str` the Issue ID

        Returns:
            None
        """
        self._id = id

    def set_name(self, name: str) -> None:
        """
        Set the name of this Issue.

        Args:
            name:
                `str` the name of this Issue

        Returns:
            None
        """
        self._name = name

    def set_description(self, description: str) -> None:
        """
        Set the description of this Issue.

        Args:
            description:
                `str` the description of this Issue

        Returns:
            None
        """
        self._description = description

    def set_source_name(self, source_name: str) -> None:
        """
        Set the name of the source of this Issue.

        Args:
            source_name:
                `str` For example, this might be "NVD" or "National Vulnerability Database"

        Returns:
            None
        """
        if self._source:
            self._source.name = source_name
        else:
            self._source = IssueTypeSource(name=source_name)

    def set_source_url(self, source_url: XsUri) -> None:
        """
        Set the URL for the source of this Issue.

        Args:
            source_url:
                `XsUri` For example, this would likely be a URL to the issue on the NVD

        Returns:
            None
        """
        if self._source:
            self._source.url = source_url
        else:
            self._source = IssueTypeSource(url=source_url)
