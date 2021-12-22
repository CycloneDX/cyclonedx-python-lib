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
        self._aliases: Optional[List[str]] = aliases
        self._tags: Optional[List[str]] = tags
        self._resolves: Optional[List[IssueType]] = resolves
        self._notes: Optional[List[Note]] = notes
        self._properties: Optional[Properties] = properties
