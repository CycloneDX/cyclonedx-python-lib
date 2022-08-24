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

import logging
from datetime import datetime
from os.path import dirname, join
from unittest.mock import Mock, patch
from uuid import UUID
from xml.etree import ElementTree

from cyclonedx.model import ThisTool
from cyclonedx.model.bom import Bom
from cyclonedx.output import SchemaVersion
from data import (
    MOCK_BOM_UUID_1,
    MOCK_UUID_4,
    get_bom_with_component_setuptools_basic,
    get_bom_with_component_setuptools_complete,
    get_bom_with_component_setuptools_with_cpe,
    get_bom_with_external_references,
)
from tests.base import BaseXmlTestCase

logger = logging.getLogger('serializable')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class TestDeserializeXml(BaseXmlTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        ThisTool.version = 'VERSION'

    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    def test_bom_external_references_v1_4(self, mock_uuid: Mock) -> None:
        bom = get_bom_with_external_references()
        bom.metadata.timestamp = datetime.fromisoformat('2021-09-01T10:50:42.051979+00:00')
        self._validate_xml_bom(bom=bom, schema_version=SchemaVersion.V1_4, fixture='bom_external_references.xml')
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    def test_simple_bom_v1_4(self, mock_uuid: Mock) -> None:
        bom = get_bom_with_component_setuptools_basic()
        bom.metadata.timestamp = datetime.fromisoformat('2021-09-01T10:50:42.051979+00:00')
        self._validate_xml_bom(bom=bom, schema_version=SchemaVersion.V1_4, fixture='bom_setuptools.xml')
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    def test_simple_bom_v1_4_with_cpe(self, mock_uuid: Mock) -> None:
        bom = get_bom_with_component_setuptools_with_cpe()
        bom.metadata.timestamp = datetime.fromisoformat('2021-09-01T10:50:42.051979+00:00')
        self._validate_xml_bom(bom=bom, schema_version=SchemaVersion.V1_4, fixture='bom_setuptools_with_cpe.xml')
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    @patch('cyclonedx.model.bom_ref.uuid4', return_value=MOCK_UUID_4)
    def test_bom_v1_4_full_component(self, mock_bom_uuid: Mock, mock_bom_ref_uuid: Mock) -> None:
        bom = get_bom_with_component_setuptools_complete()
        bom.metadata.timestamp = datetime.fromisoformat('2021-09-01T10:50:42.051979+00:00')
        self._validate_xml_bom(bom=bom, schema_version=SchemaVersion.V1_4, fixture='bom_setuptools_complete.xml')
        mock_bom_uuid.assert_called()
        mock_bom_ref_uuid.assert_called()

    # Helper methods
    def _validate_xml_bom(self, bom: Bom, schema_version: SchemaVersion, fixture: str) -> None:
        with open(
                join(dirname(__file__), f'fixtures/xml/{schema_version.to_version()}/{fixture}')) as input_xml:
            deserialized_bom = Bom.from_xml(data=ElementTree.fromstring(input_xml.read()))
            # print(f'{hash(bom.metadata)} == {hash(deserialized_bom.metadata)}')
            # for c1, c2 in zip(bom.components, deserialized_bom.components):
            #     print(f'c1: {hash(c1.release_notes)} == c2 {hash(c2.release_notes)}')
            # for c3, c4 in zip(c1.components, c2.components):
            #     print(f'    {c3}: {hash(c3)} == {c4} {hash(c4)}')
            self.assertEqual(bom, deserialized_bom)
