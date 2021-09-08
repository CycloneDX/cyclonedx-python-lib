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
from typing import List
from uuid import uuid4

from .component import Component
from ..parser import BaseParser


class BomMetaData:
    """
    Our internal representation of the metadata complex type within the CycloneDX standard.

    See https://cyclonedx.org/docs/1.3/#type_metadata
    """

    _timestamp: datetime.datetime

    def __init__(self):
        self._timestamp = datetime.datetime.now(tz=datetime.timezone.utc)

    def get_timestamp(self) -> datetime.datetime:
        return self._timestamp


class Bom:
    """
    This is our internal representation of the BOM.

    We can pass a BOM instance to a Generator to produce CycloneDX in the required format and according
    to the requested schema version.
    """

    _uuid: str
    _metadata: BomMetaData = None
    _components: List[Component] = []

    @staticmethod
    def from_parser(parser: BaseParser):
        bom = Bom()
        bom.add_components(parser.get_components())
        return bom

    def __init__(self):
        self._uuid = uuid4()
        self._metadata = BomMetaData()
        self._components.clear()

    def add_component(self, component: Component):
        self._components.append(component)

    def add_components(self, components: List[Component]):
        self._components = self._components + components

    def component_count(self) -> int:
        return len(self._components)

    def get_components(self) -> List[Component]:
        return self._components

    def get_metadata(self) -> BomMetaData:
        return self._metadata

    def get_urn_uuid(self) -> str:
        return 'urn:uuid:{}'.format(self._uuid)

    def has_component(self, component: Component) -> bool:
        return component in self._components
