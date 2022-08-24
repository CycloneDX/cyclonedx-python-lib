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
import unittest
from datetime import datetime
from os.path import dirname, join
from unittest.mock import Mock, patch
from uuid import UUID
from xml.etree import ElementTree

from cyclonedx.exception.model import UnknownComponentDependencyException
from cyclonedx.model import ThisTool
from cyclonedx.model.bom import Bom
from cyclonedx.output import SchemaVersion
from data import (
    MOCK_BOM_UUID_1,
    MOCK_UUID_4,
    MOCK_UUID_6,
    TEST_UUIDS,
    get_bom_for_issue_275_components,
    get_bom_just_complete_metadata,
    get_bom_with_component_setuptools_basic,
    get_bom_with_component_setuptools_complete,
    get_bom_with_component_setuptools_no_component_version,
    get_bom_with_component_setuptools_with_cpe,
    get_bom_with_component_setuptools_with_release_notes,
    get_bom_with_component_toml_1,
    get_bom_with_dependencies_invalid,
    get_bom_with_dependencies_valid,
    get_bom_with_external_references,
    get_bom_with_metadata_component_and_dependencies,
    get_bom_with_services_complex,
    get_bom_with_services_simple,
)
from tests.base import BaseXmlTestCase


class TestDeserializeXml(BaseXmlTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        ThisTool.version = 'VERSION'

    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    def test_bom_external_references_v1_4(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_external_references(), schema_version=SchemaVersion.V1_4,
            fixture='bom_external_references.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    def test_simple_bom_v1_4(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_basic(), schema_version=SchemaVersion.V1_4,
            fixture='bom_setuptools.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    def test_simple_bom_v1_4_with_cpe(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_with_cpe(), schema_version=SchemaVersion.V1_4,
            fixture='bom_setuptools_with_cpe.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    @patch('cyclonedx.model.bom_ref.uuid4', return_value=MOCK_UUID_4)
    def test_bom_v1_4_full_component(self, mock_bom_uuid: Mock, mock_bom_ref_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_complete(), schema_version=SchemaVersion.V1_4,
            fixture='bom_setuptools_complete.xml'
        )
        mock_bom_uuid.assert_called()
        mock_bom_ref_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    def test_bom_v1_4_component_hashes_external_references(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_toml_1(), schema_version=SchemaVersion.V1_4,
            fixture='bom_toml_hashes_and_references.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    def test_bom_v1_4_no_component_version(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_no_component_version(), schema_version=SchemaVersion.V1_4,
            fixture='bom_setuptools_no_version.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    def test_bom_v1_4_component_with_release_notes(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_with_release_notes(), schema_version=SchemaVersion.V1_4,
            fixture='bom_setuptools_with_release_notes.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    @patch('cyclonedx.model.bom_ref.uuid4', return_value=MOCK_UUID_6)
    def test_bom_v1_4_with_metadata_component(self, mock_bom_uuid: Mock, mock_bom_ref_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_just_complete_metadata(), schema_version=SchemaVersion.V1_4,
            fixture='bom_with_full_metadata.xml'
        )
        mock_bom_uuid.assert_called()
        mock_bom_ref_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    @patch('cyclonedx.model.bom_ref.uuid4', side_effect=TEST_UUIDS)
    def test_bom_v1_4_services_simple(self, mock_bom_uuid: Mock, mock_bom_ref_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_services_simple(), schema_version=SchemaVersion.V1_4,
            fixture='bom_services_simple.xml'
        )
        mock_bom_uuid.assert_called()
        mock_bom_ref_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    @patch('cyclonedx.model.bom_ref.uuid4', side_effect=TEST_UUIDS)
    def test_bom_v1_4_services_complex(self, mock_bom_uuid: Mock, mock_bom_ref_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_services_complex(), schema_version=SchemaVersion.V1_4,
            fixture='bom_services_complex.xml'
        )
        mock_bom_uuid.assert_called()
        mock_bom_ref_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    def test_bom_v1_4_dependencies(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_dependencies_valid(), schema_version=SchemaVersion.V1_4,
            fixture='bom_dependencies.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    def test_bom_v1_4_dependencies_for_bom_component(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_metadata_component_and_dependencies(), schema_version=SchemaVersion.V1_4,
            fixture='bom_dependencies_component.xml'
        )
        mock_uuid.assert_called()

    @unittest.skip('Dependencies not yet supported')
    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    def test_bom_v1_4_dependencies_invalid(self, mock_uuid: Mock) -> None:
        with self.assertRaises(UnknownComponentDependencyException):
            self._validate_xml_bom(
                bom=get_bom_with_dependencies_invalid(), schema_version=SchemaVersion.V1_4,
                fixture='bom_dependencies.xml'
            )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=UUID(MOCK_BOM_UUID_1))
    def test_bom_v1_4_issue_275_components(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_for_issue_275_components(), schema_version=SchemaVersion.V1_4,
            fixture='bom_issue_275_components.xml'
        )
        mock_uuid.assert_called()

    # Helper methods
    def _validate_xml_bom(self, bom: Bom, schema_version: SchemaVersion, fixture: str) -> None:
        bom.metadata.timestamp = datetime.fromisoformat('2021-09-01T10:50:42.051979+00:00')
        with open(
                join(dirname(__file__), f'fixtures/xml/{schema_version.to_version()}/{fixture}')) as input_xml:
            deserialized_bom = Bom.from_xml(data=ElementTree.fromstring(input_xml.read()))
            self.assertEqual(bom, deserialized_bom)
