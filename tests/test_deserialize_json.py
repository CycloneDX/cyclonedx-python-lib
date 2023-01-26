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

import json
import logging
from datetime import datetime
from os.path import dirname, join
from typing import cast
from unittest.mock import Mock, patch
from uuid import UUID

from cyclonedx.model.bom import Bom
from cyclonedx.output import LATEST_SUPPORTED_SCHEMA_VERSION, OutputFormat, SchemaVersion, get_instance
from tests.base import BaseJsonTestCase
from tests.data import (
    MOCK_BOM_UUID_1,
    MOCK_UUID_6,
    get_bom_with_component_setuptools_basic,
    get_bom_with_component_setuptools_complete,
    get_bom_with_component_setuptools_with_cpe,
    get_bom_with_external_references,
)

logger = logging.getLogger('serializable')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def fixed_date_time() -> datetime:
    return datetime.fromisoformat('2023-01-07 13:44:32.312678+00:00')


@patch('cyclonedx.model.ThisTool._version', 'TESTING')
@patch('cyclonedx.model.bom.get_now_utc', fixed_date_time)
class TestOutputJson(BaseJsonTestCase):

    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    def test_bom_external_references_v1_4(self, mock_uuid: Mock) -> None:
        self._validate_json_bom(
            bom=get_bom_with_external_references(), schema_version=SchemaVersion.V1_4,
            fixture='bom_external_references.json'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    def test_bom_external_references_v1_3(self, mock_uuid: Mock) -> None:
        self._validate_json_bom(
            bom=get_bom_with_external_references(), schema_version=SchemaVersion.V1_3,
            fixture='bom_external_references.json'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    def test_bom_external_references_v1_2(self, mock_uuid: Mock) -> None:
        self._validate_json_bom(
            bom=get_bom_with_external_references(), schema_version=SchemaVersion.V1_2,
            fixture='bom_external_references.json'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    def test_simple_bom_v1_4(self, mock_uuid: Mock) -> None:
        self._validate_json_bom(
            bom=get_bom_with_component_setuptools_basic(), schema_version=SchemaVersion.V1_4,
            fixture='bom_setuptools.json'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    def test_simple_bom_v1_3(self, mock_uuid: Mock) -> None:
        self._validate_json_bom(
            bom=get_bom_with_component_setuptools_basic(), schema_version=SchemaVersion.V1_3,
            fixture='bom_setuptools.json'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    def test_simple_bom_v1_2(self, mock_uuid: Mock) -> None:
        self._validate_json_bom(
            bom=get_bom_with_component_setuptools_basic(), schema_version=SchemaVersion.V1_2,
            fixture='bom_setuptools.json'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    def test_simple_bom_v1_4_with_cpe(self, mock_uuid: Mock) -> None:
        self._validate_json_bom(
            bom=get_bom_with_component_setuptools_with_cpe(), schema_version=SchemaVersion.V1_4,
            fixture='bom_setuptools_with_cpe.json'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    def test_simple_bom_v1_3_with_cpe(self, mock_uuid: Mock) -> None:
        self._validate_json_bom(
            bom=get_bom_with_component_setuptools_with_cpe(), schema_version=SchemaVersion.V1_3,
            fixture='bom_setuptools_with_cpe.json'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    def test_simple_bom_v1_2_with_cpe(self, mock_uuid: Mock) -> None:
        self._validate_json_bom(
            bom=get_bom_with_component_setuptools_with_cpe(), schema_version=SchemaVersion.V1_2,
            fixture='bom_setuptools_with_cpe.json'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom_ref.uuid4', return_value=MOCK_UUID_6)
    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    def test_bom_v1_4_full_component(self, mock1: Mock, mock2: Mock) -> None:
        self.maxDiff = None
        self._validate_json_bom(
            bom=get_bom_with_component_setuptools_complete(), schema_version=SchemaVersion.V1_4,
            fixture='bom_setuptools_complete.json'
        )
        mock1.assert_called()
        mock2.assert_called()

    # --

    # Helper methods
    def _validate_json_bom(self, bom: Bom, schema_version: SchemaVersion, fixture: str) -> None:
        bom.metadata.timestamp = fixed_date_time()
        bom.validate()

        if schema_version != LATEST_SUPPORTED_SCHEMA_VERSION:
            # Rewind the BOM to only have data supported by the SchemaVersion in question
            outputter = get_instance(bom=bom, output_format=OutputFormat.JSON, schema_version=schema_version)
            bom = cast(Bom, Bom.from_json(data=json.loads(outputter.output_as_string())))

        with open(
            join(dirname(__file__), f'fixtures/json/{schema_version.to_version()}/{fixture}')) as input_json:
            deserialized_bom = cast(Bom, Bom.from_json(data=json.loads(input_json.read())))

            self.assertEqual(bom.metadata, deserialized_bom.metadata)

            # This comparison fails for Dependencies despite the SortedSet's being identical
            # self.assertEqual(bom.dependencies, deserialized_bom.dependencies)
            self.assertSetEqual(set(bom.dependencies), set(deserialized_bom.dependencies))

            self.assertEqual(bom.vulnerabilities, deserialized_bom.vulnerabilities)

            self.assertEqual(bom, deserialized_bom)
