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
from os.path import dirname, join
from typing import cast
from unittest.mock import Mock, patch
from uuid import UUID
from xml.etree import ElementTree

from cyclonedx.model.bom import Bom
from cyclonedx.output import LATEST_SUPPORTED_SCHEMA_VERSION, SchemaVersion, get_instance
from cyclonedx.schema import OutputFormat
from tests.base import BaseXmlTestCase
from tests.data import (
    MOCK_BOM_UUID_1,
    MOCK_UUID_2,
    MOCK_UUID_3,
    MOCK_UUID_4,
    MOCK_UUID_5,
    MOCK_UUID_6,
    TEST_UUIDS,
    get_bom_for_issue_275_components,
    get_bom_just_complete_metadata,
    get_bom_with_component_setuptools_basic,
    get_bom_with_component_setuptools_complete,
    get_bom_with_component_setuptools_no_component_version,
    get_bom_with_component_setuptools_with_cpe,
    get_bom_with_component_setuptools_with_release_notes,
    get_bom_with_component_setuptools_with_vulnerability,
    get_bom_with_component_toml_1,
    get_bom_with_dependencies_valid,
    get_bom_with_external_references,
    get_bom_with_metadata_component_and_dependencies,
    get_bom_with_nested_services,
    get_bom_with_services_complex,
    get_bom_with_services_simple,
)


def fixed_date_time() -> datetime:
    return datetime.fromisoformat('2023-01-07 13:44:32.312678+00:00')


@patch('cyclonedx.model.ThisTool._version', 'TESTING')
@patch('cyclonedx.model.bom.get_now_utc', fixed_date_time)
class TestDeserializeXml(BaseXmlTestCase):

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_external_references_v1_4(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_external_references(), schema_version=SchemaVersion.V1_4,
            fixture='bom_external_references.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_external_references_v1_3(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_external_references(), schema_version=SchemaVersion.V1_3,
            fixture='bom_external_references.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_external_references_v1_2(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_external_references(), schema_version=SchemaVersion.V1_2,
            fixture='bom_external_references.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_external_references_v1_1(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_external_references(), schema_version=SchemaVersion.V1_1,
            fixture='bom_external_references.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_external_references_v1_0(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_external_references(), schema_version=SchemaVersion.V1_0,
            fixture='bom_empty.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_simple_bom_v1_4(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_basic(), schema_version=SchemaVersion.V1_4,
            fixture='bom_setuptools.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_simple_bom_v1_3(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_basic(), schema_version=SchemaVersion.V1_3,
            fixture='bom_setuptools.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_simple_bom_v1_2(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_basic(), schema_version=SchemaVersion.V1_2,
            fixture='bom_setuptools.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_simple_bom_v1_1(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_basic(), schema_version=SchemaVersion.V1_1,
            fixture='bom_setuptools.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_simple_bom_v1_0(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_basic(), schema_version=SchemaVersion.V1_0,
            fixture='bom_setuptools.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_simple_bom_v1_4_with_cpe(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_with_cpe(), schema_version=SchemaVersion.V1_4,
            fixture='bom_setuptools_with_cpe.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_simple_bom_v1_3_with_cpe(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_with_cpe(), schema_version=SchemaVersion.V1_3,
            fixture='bom_setuptools_with_cpe.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_simple_bom_v1_2_with_cpe(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_with_cpe(), schema_version=SchemaVersion.V1_2,
            fixture='bom_setuptools_with_cpe.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_simple_bom_v1_1_with_cpe(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_with_cpe(), schema_version=SchemaVersion.V1_1,
            fixture='bom_setuptools_with_cpe.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_simple_bom_v1_0_with_cpe(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_with_cpe(), schema_version=SchemaVersion.V1_0,
            fixture='bom_setuptools_with_cpe.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_4))
    def test_bom_v1_4_full_component(self, mock_bom_uuid: Mock, mock_bom_ref_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_complete(), schema_version=SchemaVersion.V1_4,
            fixture='bom_setuptools_complete.xml'
        )
        mock_bom_uuid.assert_called()
        mock_bom_ref_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_3))
    def test_bom_v1_3_full_component(self, mock_bom_uuid: Mock, mock_bom_ref_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_complete(), schema_version=SchemaVersion.V1_3,
            fixture='bom_setuptools_complete.xml'
        )
        mock_bom_uuid.assert_called()
        mock_bom_ref_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_2))
    def test_bom_v1_2_full_component(self, mock_bom_uuid: Mock, mock_bom_ref_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_complete(), schema_version=SchemaVersion.V1_2,
            fixture='bom_setuptools_complete.xml'
        )
        mock_bom_uuid.assert_called()
        mock_bom_ref_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_4))
    def test_bom_v1_1_full_component(self, mock_bom_uuid: Mock, mock_bom_ref_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_complete(), schema_version=SchemaVersion.V1_1,
            fixture='bom_setuptools_complete.xml'
        )
        mock_bom_uuid.assert_called()
        mock_bom_ref_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_4))
    def test_bom_v1_0_full_component(self, mock_bom_uuid: Mock, mock_bom_ref_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_complete(), schema_version=SchemaVersion.V1_0,
            fixture='bom_setuptools_complete.xml'
        )
        mock_bom_uuid.assert_called()
        mock_bom_ref_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_4_component_hashes_external_references(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_toml_1(), schema_version=SchemaVersion.V1_4,
            fixture='bom_toml_hashes_and_references.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_3_component_hashes_external_references(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_toml_1(), schema_version=SchemaVersion.V1_3,
            fixture='bom_toml_hashes_and_references.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_2_component_hashes_external_references(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_toml_1(), schema_version=SchemaVersion.V1_2,
            fixture='bom_toml_hashes_and_references.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_1_component_hashes_external_references(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_toml_1(), schema_version=SchemaVersion.V1_1,
            fixture='bom_toml_hashes_and_references.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_0_component_hashes_external_references(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_toml_1(), schema_version=SchemaVersion.V1_0,
            fixture='bom_toml_hashes_and_references.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_4_no_component_version(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_no_component_version(), schema_version=SchemaVersion.V1_4,
            fixture='bom_setuptools_no_version.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_3_no_component_version(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_no_component_version(), schema_version=SchemaVersion.V1_3,
            fixture='bom_setuptools_no_version.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_2_no_component_version(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_no_component_version(), schema_version=SchemaVersion.V1_2,
            fixture='bom_setuptools_no_version.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_1_no_component_version(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_no_component_version(), schema_version=SchemaVersion.V1_1,
            fixture='bom_setuptools_no_version.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_0_no_component_version(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_no_component_version(), schema_version=SchemaVersion.V1_0,
            fixture='bom_setuptools_no_version.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_4_component_with_release_notes(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_with_release_notes(), schema_version=SchemaVersion.V1_4,
            fixture='bom_setuptools_with_release_notes.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_3_component_with_release_notes(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_with_release_notes(), schema_version=SchemaVersion.V1_3,
            fixture='bom_setuptools.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_4_component_with_vulnerability(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_with_vulnerability(), schema_version=SchemaVersion.V1_4,
            fixture='bom_setuptools_with_vulnerabilities.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_3_component_with_vulnerability(self, mock_uuid: Mock) -> None:
        with self.assertRaises(ValueError):
            self._validate_xml_bom(
                bom=get_bom_with_component_setuptools_with_vulnerability(), schema_version=SchemaVersion.V1_3,
                fixture='bom_setuptools_with_vulnerabilities.xml'
            )
            mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_2_component_with_vulnerability(self, mock_uuid: Mock) -> None:
        with self.assertRaises(ValueError):
            self._validate_xml_bom(
                bom=get_bom_with_component_setuptools_with_vulnerability(), schema_version=SchemaVersion.V1_2,
                fixture='bom_setuptools_with_vulnerabilities.xml'
            )
            mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_1_component_with_vulnerability(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_with_vulnerability(), schema_version=SchemaVersion.V1_1,
            fixture='bom_setuptools.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_0_component_with_vulnerability(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_component_setuptools_with_vulnerability(), schema_version=SchemaVersion.V1_0,
            fixture='bom_setuptools.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_6))
    def test_bom_v1_4_with_metadata_component(self, mock_bom_uuid: Mock, mock_bom_ref_uuid: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_xml_bom(
                bom=get_bom_just_complete_metadata(), schema_version=SchemaVersion.V1_4,
                fixture='bom_with_full_metadata.xml'
            )
            mock_bom_uuid.assert_called()
            mock_bom_ref_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_5))
    def test_bom_v1_3_with_metadata_component(self, mock_bom_uuid: Mock, mock_bom_ref_uuid: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_xml_bom(
                bom=get_bom_just_complete_metadata(), schema_version=SchemaVersion.V1_3,
                fixture='bom_with_full_metadata.xml'
            )
            mock_bom_uuid.assert_called()
            mock_bom_ref_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_4))
    def test_bom_v1_2_with_metadata_component(self, mock_bom_uuid: Mock, mock_bom_ref_uuid: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_xml_bom(
                bom=get_bom_just_complete_metadata(), schema_version=SchemaVersion.V1_2,
                fixture='bom_with_full_metadata.xml'
            )
            mock_bom_uuid.assert_called()
            mock_bom_ref_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_6))
    def test_bom_v1_1_with_metadata_component(self, mock_bom_uuid: Mock, mock_bom_ref_uuid: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_xml_bom(
                bom=get_bom_just_complete_metadata(), schema_version=SchemaVersion.V1_1,
                fixture='bom_empty.xml'
            )
            mock_bom_uuid.assert_called()
            mock_bom_ref_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_6))
    def test_bom_v1_0_with_metadata_component(self, mock_bom_uuid: Mock, mock_bom_ref_uuid: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_xml_bom(
                bom=get_bom_just_complete_metadata(), schema_version=SchemaVersion.V1_0,
                fixture='bom_empty.xml'
            )
            mock_bom_uuid.assert_called()
            mock_bom_ref_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_3))
    @patch('cyclonedx.model.service.uuid4', side_effect=TEST_UUIDS)
    def test_bom_v1_4_services_simple(self, mock_1: Mock, mock_2: Mock, mock_3: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_xml_bom(
                bom=get_bom_with_services_simple(), schema_version=SchemaVersion.V1_4,
                fixture='bom_services_simple.xml'
            )
            mock_1.assert_called()
            mock_2.assert_called()
            mock_3.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_3))
    @patch('cyclonedx.model.service.uuid4', side_effect=TEST_UUIDS)
    def test_bom_v1_3_services_simple(self, mock_1: Mock, mock_2: Mock, mock_3: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_xml_bom(
                bom=get_bom_with_services_simple(), schema_version=SchemaVersion.V1_3,
                fixture='bom_services_simple.xml'
            )
            mock_1.assert_called()
            mock_2.assert_called()
            mock_3.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_3))
    @patch('cyclonedx.model.service.uuid4', side_effect=TEST_UUIDS)
    def test_bom_v1_2_services_simple(self, mock_1: Mock, mock_2: Mock, mock_3: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_xml_bom(
                bom=get_bom_with_services_simple(), schema_version=SchemaVersion.V1_2,
                fixture='bom_services_simple.xml'
            )
            mock_1.assert_called()
            mock_2.assert_called()
            mock_3.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_3))
    @patch('cyclonedx.model.service.uuid4', side_effect=TEST_UUIDS)
    def test_bom_v1_1_services_simple(self, mock_1: Mock, mock_2: Mock, mock_3: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_xml_bom(
                bom=get_bom_with_services_simple(), schema_version=SchemaVersion.V1_1,
                fixture='bom_empty.xml'
            )
            mock_1.assert_called()
            mock_2.assert_called()
            mock_3.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_3))
    @patch('cyclonedx.model.service.uuid4', side_effect=TEST_UUIDS)
    def test_bom_v1_0_services_simple(self, mock_1: Mock, mock_2: Mock, mock_3: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_xml_bom(
                bom=get_bom_with_services_simple(), schema_version=SchemaVersion.V1_0,
                fixture='bom_empty.xml'
            )
            mock_1.assert_called()
            mock_2.assert_called()
            mock_3.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_4))
    @patch('cyclonedx.model.service.uuid4', side_effect=TEST_UUIDS)
    def test_bom_v1_4_services_complex(self, mock_1: Mock, mock_2: Mock, mock_3: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_xml_bom(
                bom=get_bom_with_services_complex(), schema_version=SchemaVersion.V1_4,
                fixture='bom_services_complex.xml'
            )
            mock_1.assert_called()
            mock_2.assert_called()
            mock_3.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_4))
    @patch('cyclonedx.model.service.uuid4', side_effect=TEST_UUIDS)
    def test_bom_v1_3_services_complex(self, mock_1: Mock, mock_2: Mock, mock_3: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_xml_bom(
                bom=get_bom_with_services_complex(), schema_version=SchemaVersion.V1_3,
                fixture='bom_services_complex.xml'
            )
            mock_1.assert_called()
            mock_2.assert_called()
            mock_3.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_4))
    @patch('cyclonedx.model.service.uuid4', side_effect=TEST_UUIDS)
    def test_bom_v1_2_services_complex(self, mock_1: Mock, mock_2: Mock, mock_3: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_xml_bom(
                bom=get_bom_with_services_complex(), schema_version=SchemaVersion.V1_2,
                fixture='bom_services_complex.xml'
            )
            mock_1.assert_called()
            mock_2.assert_called()
            mock_3.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_4))
    @patch('cyclonedx.model.service.uuid4', side_effect=TEST_UUIDS)
    def test_bom_v1_1_services_complex(self, mock_1: Mock, mock_2: Mock, mock_3: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_xml_bom(
                bom=get_bom_with_services_complex(), schema_version=SchemaVersion.V1_1,
                fixture='bom_empty.xml'
            )
            mock_1.assert_called()
            mock_2.assert_called()
            mock_3.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_6))
    @patch('cyclonedx.model.service.uuid4', side_effect=TEST_UUIDS)
    def test_bom_v1_4_services_nested(self, mock_1: Mock, mock_2: Mock, mock_3: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_xml_bom(
                bom=get_bom_with_nested_services(), schema_version=SchemaVersion.V1_4,
                fixture='bom_services_nested.xml'
            )
            mock_1.assert_called()
            mock_2.assert_called()
            mock_3.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_6))
    @patch('cyclonedx.model.service.uuid4', side_effect=TEST_UUIDS)
    def test_bom_v1_3_services_nested(self, mock_1: Mock, mock_2: Mock, mock_3: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_xml_bom(
                bom=get_bom_with_nested_services(), schema_version=SchemaVersion.V1_3,
                fixture='bom_services_nested.xml'
            )
            mock_1.assert_called()
            mock_2.assert_called()
            mock_3.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_6))
    @patch('cyclonedx.model.service.uuid4', side_effect=TEST_UUIDS)
    def test_bom_v1_2_services_nested(self, mock_1: Mock, mock_2: Mock, mock_3: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_xml_bom(
                bom=get_bom_with_nested_services(), schema_version=SchemaVersion.V1_2,
                fixture='bom_services_nested.xml'
            )
            mock_1.assert_called()
            mock_2.assert_called()
            mock_3.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_4_dependencies(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_dependencies_valid(), schema_version=SchemaVersion.V1_4,
            fixture='bom_dependencies.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_3_dependencies(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_dependencies_valid(), schema_version=SchemaVersion.V1_3,
            fixture='bom_dependencies.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_2_dependencies(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_dependencies_valid(), schema_version=SchemaVersion.V1_2,
            fixture='bom_dependencies.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_1_dependencies(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_dependencies_valid(), schema_version=SchemaVersion.V1_1,
            fixture='bom_dependencies.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_4_dependencies_for_bom_component(self, mock_uuid: Mock) -> None:
        self._validate_xml_bom(
            bom=get_bom_with_metadata_component_and_dependencies(), schema_version=SchemaVersion.V1_4,
            fixture='bom_dependencies_component.xml'
        )
        mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_3_dependencies_for_bom_component(self, mock_uuid: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_xml_bom(
                bom=get_bom_with_metadata_component_and_dependencies(), schema_version=SchemaVersion.V1_3,
                fixture='bom_dependencies_component.xml'
            )
            mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_2_dependencies_for_bom_component(self, mock_uuid: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_xml_bom(
                bom=get_bom_with_metadata_component_and_dependencies(), schema_version=SchemaVersion.V1_2,
                fixture='bom_dependencies_component.xml'
            )
            mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_4_issue_275_components(self, mock_uuid: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_xml_bom(
                bom=get_bom_for_issue_275_components(), schema_version=SchemaVersion.V1_4,
                fixture='bom_issue_275_components.xml'
            )
            mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_3_issue_275_components(self, mock_uuid: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_xml_bom(
                bom=get_bom_for_issue_275_components(), schema_version=SchemaVersion.V1_3,
                fixture='bom_issue_275_components.xml'
            )
            mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_2_issue_275_components(self, mock_uuid: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_xml_bom(
                bom=get_bom_for_issue_275_components(), schema_version=SchemaVersion.V1_2,
                fixture='bom_issue_275_components.xml'
            )
            mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_1_issue_275_components(self, mock_uuid: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_xml_bom(
                bom=get_bom_for_issue_275_components(), schema_version=SchemaVersion.V1_1,
                fixture='bom_issue_275_components.xml'
            )
            mock_uuid.assert_called()

    @patch('cyclonedx.model.bom.uuid4', return_value=MOCK_BOM_UUID_1)
    def test_bom_v1_0_issue_275_components(self, mock_uuid: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_xml_bom(
                bom=get_bom_for_issue_275_components(), schema_version=SchemaVersion.V1_0,
                fixture='bom_issue_275_components.xml'
            )
            mock_uuid.assert_called()

    # Helper methods
    def _validate_xml_bom(self, bom: Bom, schema_version: SchemaVersion, fixture: str) -> None:
        bom.metadata.timestamp = fixed_date_time()
        bom.validate()

        if schema_version != LATEST_SUPPORTED_SCHEMA_VERSION:
            # Rewind the BOM to only have data supported by the SchemaVersion in question
            outputter = get_instance(bom=bom, output_format=OutputFormat.XML, schema_version=schema_version)
            bom = cast(Bom, Bom.from_xml(data=ElementTree.fromstring(outputter.output_as_string())))

        with open(join(dirname(__file__), f'fixtures/xml/{schema_version.to_version()}/{fixture}')) as input_xml:
            xml = input_xml.read()
            deserialized_bom = cast(Bom, Bom.from_xml(data=ElementTree.fromstring(xml)))

            self.assertEqual(bom.metadata, deserialized_bom.metadata)

            # This comparison fails for Dependencies despite the SortedSet's being identical
            # print(bom.dependencies.difference(deserialized_bom.dependencies))
            # self.assertEqual(bom.dependencies, deserialized_bom.dependencies)
            # self.assertSetEqual(set(bom.dependencies), set(deserialized_bom.dependencies))

            self.assertEqual(bom.vulnerabilities, deserialized_bom.vulnerabilities)
            self.assertEqual(bom, deserialized_bom)
