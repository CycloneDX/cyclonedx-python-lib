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
from os.path import dirname, join
from unittest.mock import Mock, patch
from uuid import UUID

from cyclonedx.exception.output import FormatNotSupportedException
from cyclonedx.model.bom import Bom
from cyclonedx.output import get_instance
from cyclonedx.schema import OutputFormat, SchemaVersion
from tests.base import BaseJsonTestCase
from tests.data import (
    MOCK_UUID_1,
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


@patch('cyclonedx.model.ThisTool._version', 'TESTING')
class TestOutputJson(BaseJsonTestCase):

    def test_bom_external_references_v1_4(self) -> None:
        self._validate_json_bom(
            bom=get_bom_with_external_references(), schema_version=SchemaVersion.V1_4,
            fixture='bom_external_references.json'
        )

    def test_bom_external_references_v1_3(self) -> None:
        self._validate_json_bom(
            bom=get_bom_with_external_references(), schema_version=SchemaVersion.V1_3,
            fixture='bom_external_references.json'
        )

    def test_bom_external_references_v1_2(self) -> None:
        self._validate_json_bom(
            bom=get_bom_with_external_references(), schema_version=SchemaVersion.V1_2,
            fixture='bom_external_references.json'
        )

    def test_simple_bom_v1_4(self) -> None:
        self._validate_json_bom(
            bom=get_bom_with_component_setuptools_basic(), schema_version=SchemaVersion.V1_4,
            fixture='bom_setuptools.json'
        )

    def test_simple_bom_v1_3(self) -> None:
        self._validate_json_bom(
            bom=get_bom_with_component_setuptools_basic(), schema_version=SchemaVersion.V1_3,
            fixture='bom_setuptools.json'
        )

    def test_simple_bom_v1_2(self) -> None:
        self._validate_json_bom(
            bom=get_bom_with_component_setuptools_basic(), schema_version=SchemaVersion.V1_2,
            fixture='bom_setuptools.json'
        )

    def test_simple_bom_v1_1(self) -> None:
        self._validate_json_bom_not_supported(
            bom=get_bom_with_component_setuptools_basic(), schema_version=SchemaVersion.V1_1
        )

    def test_simple_bom_v1_0(self) -> None:
        self._validate_json_bom_not_supported(
            bom=get_bom_with_component_setuptools_basic(), schema_version=SchemaVersion.V1_0
        )

    def test_simple_bom_v1_4_with_cpe(self) -> None:
        self._validate_json_bom(
            bom=get_bom_with_component_setuptools_with_cpe(), schema_version=SchemaVersion.V1_4,
            fixture='bom_setuptools_with_cpe.json'
        )

    def test_simple_bom_v1_3_with_cpe(self) -> None:
        self._validate_json_bom(
            bom=get_bom_with_component_setuptools_with_cpe(), schema_version=SchemaVersion.V1_3,
            fixture='bom_setuptools_with_cpe.json'
        )

    def test_simple_bom_v1_2_with_cpe(self) -> None:
        self._validate_json_bom(
            bom=get_bom_with_component_setuptools_with_cpe(), schema_version=SchemaVersion.V1_2,
            fixture='bom_setuptools_with_cpe.json'
        )

    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_6))
    def test_bom_v1_4_full_component(self, mock: Mock) -> None:
        self.maxDiff = None
        self._validate_json_bom(
            bom=get_bom_with_component_setuptools_complete(), schema_version=SchemaVersion.V1_4,
            fixture='bom_setuptools_complete.json'
        )
        mock.assert_called()

    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_6))
    def test_bom_v1_3_full_component(self, mock: Mock) -> None:
        self._validate_json_bom(
            bom=get_bom_with_component_setuptools_complete(), schema_version=SchemaVersion.V1_3,
            fixture='bom_setuptools_complete.json'
        )
        mock.assert_called()

    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_6))
    def test_bom_v1_2_full_component(self, mock: Mock) -> None:
        self._validate_json_bom(
            bom=get_bom_with_component_setuptools_complete(), schema_version=SchemaVersion.V1_2,
            fixture='bom_setuptools_complete.json'
        )
        mock.assert_called()

    def test_bom_v1_4_component_hashes_external_references(self) -> None:
        self._validate_json_bom(
            bom=get_bom_with_component_toml_1(), schema_version=SchemaVersion.V1_4,
            fixture='bom_toml_1.json'
        )

    def test_bom_v1_3_component_hashes_external_references(self) -> None:
        self._validate_json_bom(
            bom=get_bom_with_component_toml_1(), schema_version=SchemaVersion.V1_3,
            fixture='bom_toml_1.json'
        )

    def test_bom_v1_2_component_hashes_external_references(self) -> None:
        self._validate_json_bom(
            bom=get_bom_with_component_toml_1(), schema_version=SchemaVersion.V1_2,
            fixture='bom_toml_1.json'
        )

    def test_bom_v1_1_component_hashes_external_references(self) -> None:
        self._validate_json_bom_not_supported(bom=get_bom_with_component_toml_1(), schema_version=SchemaVersion.V1_1)

    def test_bom_v1_0_component_hashes_external_references(self) -> None:
        self._validate_json_bom_not_supported(bom=get_bom_with_component_toml_1(), schema_version=SchemaVersion.V1_0)

    def test_bom_v1_4_no_component_version(self) -> None:
        self._validate_json_bom(
            bom=get_bom_with_component_setuptools_no_component_version(), schema_version=SchemaVersion.V1_4,
            fixture='bom_setuptools_no_version.json'
        )

    def test_bom_v1_3_no_component_version(self) -> None:
        self._validate_json_bom(
            bom=get_bom_with_component_setuptools_no_component_version(), schema_version=SchemaVersion.V1_3,
            fixture='bom_setuptools_no_version.json'
        )

    def test_bom_v1_4_component_with_release_notes(self) -> None:
        self._validate_json_bom(
            bom=get_bom_with_component_setuptools_with_release_notes(), schema_version=SchemaVersion.V1_4,
            fixture='bom_setuptools_with_release_notes.json'
        )

    def test_bom_v1_3_component_with_release_notes(self) -> None:
        self._validate_json_bom(
            bom=get_bom_with_component_setuptools_with_release_notes(), schema_version=SchemaVersion.V1_3,
            fixture='bom_setuptools.json'
        )

    def test_bom_v1_4_component_with_vulnerability(self) -> None:
        self._validate_json_bom(
            bom=get_bom_with_component_setuptools_with_vulnerability(), schema_version=SchemaVersion.V1_4,
            fixture='bom_setuptools_with_vulnerabilities.json'
        )

    def test_bom_v1_3_component_with_vulnerability(self) -> None:
        # Vulnerabilities not support in JSON < 1.4
        self._validate_json_bom(
            bom=get_bom_with_component_setuptools_with_vulnerability(), schema_version=SchemaVersion.V1_3,
            fixture='bom_setuptools.json'
        )

    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_1))
    def test_bom_v1_4_with_metadata_component(self, mock_uuid: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_json_bom(
                bom=get_bom_just_complete_metadata(), schema_version=SchemaVersion.V1_4,
                fixture='bom_with_full_metadata.json'
            )
            mock_uuid.assert_called()

    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_2))
    def test_bom_v1_3_with_metadata_component(self, mock_uuid: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_json_bom(
                bom=get_bom_just_complete_metadata(), schema_version=SchemaVersion.V1_3,
                fixture='bom_with_full_metadata.json'
            )
            mock_uuid.assert_called()

    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_3))
    def test_bom_v1_2_with_metadata_component(self, mock_uuid: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_json_bom(
                bom=get_bom_just_complete_metadata(), schema_version=SchemaVersion.V1_2,
                fixture='bom_with_full_metadata.json'
            )
            mock_uuid.assert_called()

    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_6))
    @patch('cyclonedx.model.service.uuid4', side_effect=TEST_UUIDS)
    def test_bom_v1_4_services_simple(self, mock_1: Mock, mock_2: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_json_bom(
                bom=get_bom_with_services_simple(), schema_version=SchemaVersion.V1_4,
                fixture='bom_services_simple.json'
            )
            mock_1.assert_called()
            mock_2.assert_called()

    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_6))
    @patch('cyclonedx.model.service.uuid4', side_effect=TEST_UUIDS)
    def test_bom_v1_3_services_simple(self, mock_1: Mock, mock_2: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_json_bom(
                bom=get_bom_with_services_simple(), schema_version=SchemaVersion.V1_3,
                fixture='bom_services_simple.json'
            )
            mock_1.assert_called()
            mock_2.assert_called()

    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_6))
    @patch('cyclonedx.model.service.uuid4', side_effect=TEST_UUIDS)
    def test_bom_v1_2_services_simple(self, mock_1: Mock, mock_2: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_json_bom(
                bom=get_bom_with_services_simple(), schema_version=SchemaVersion.V1_2,
                fixture='bom_services_simple.json'
            )
            mock_1.assert_called()
            mock_2.assert_called()

    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_5))
    @patch('cyclonedx.model.service.uuid4', side_effect=TEST_UUIDS)
    def test_bom_v1_4_services_complex(self, mock_1: Mock, mock_2: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_json_bom(
                bom=get_bom_with_services_complex(), schema_version=SchemaVersion.V1_4,
                fixture='bom_services_complex.json'
            )
            mock_1.assert_called()
            mock_2.assert_called()

    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_5))
    @patch('cyclonedx.model.service.uuid4', side_effect=TEST_UUIDS)
    def test_bom_v1_3_services_complex(self, mock_1: Mock, mock_2: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_json_bom(
                bom=get_bom_with_services_complex(), schema_version=SchemaVersion.V1_3,
                fixture='bom_services_complex.json'
            )
            mock_1.assert_called()
            mock_2.assert_called()

    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_5))
    @patch('cyclonedx.model.service.uuid4', side_effect=TEST_UUIDS)
    def test_bom_v1_2_services_complex(self, mock_1: Mock, mock_2: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_json_bom(
                bom=get_bom_with_services_complex(), schema_version=SchemaVersion.V1_2,
                fixture='bom_services_complex.json'
            )
            mock_1.assert_called()
            mock_2.assert_called()

    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_4))
    @patch('cyclonedx.model.service.uuid4', side_effect=TEST_UUIDS)
    def test_bom_v1_4_services_nested(self, mock_1: Mock, mock_2: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_json_bom(
                bom=get_bom_with_nested_services(), schema_version=SchemaVersion.V1_4,
                fixture='bom_services_nested.json'
            )
            mock_1.assert_called()
            mock_2.assert_called()

    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_4))
    @patch('cyclonedx.model.service.uuid4', side_effect=TEST_UUIDS)
    def test_bom_v1_3_services_nested(self, mock_1: Mock, mock_2: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_json_bom(
                bom=get_bom_with_nested_services(), schema_version=SchemaVersion.V1_3,
                fixture='bom_services_nested.json'
            )
            mock_1.assert_called()
            mock_2.assert_called()

    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_4))
    @patch('cyclonedx.model.service.uuid4', side_effect=TEST_UUIDS)
    def test_bom_v1_2_services_nested(self, mock_1: Mock, mock_2: Mock) -> None:
        with self.assertWarns(UserWarning):
            self._validate_json_bom(
                bom=get_bom_with_nested_services(), schema_version=SchemaVersion.V1_2,
                fixture='bom_services_nested.json'
            )
            mock_1.assert_called()
            mock_2.assert_called()

    def test_bom_v1_4_dependencies(self) -> None:
        self._validate_json_bom(
            bom=get_bom_with_dependencies_valid(), schema_version=SchemaVersion.V1_4,
            fixture='bom_dependencies.json'
        )

    def test_bom_v1_3_dependencies(self) -> None:
        self._validate_json_bom(
            bom=get_bom_with_dependencies_valid(), schema_version=SchemaVersion.V1_3,
            fixture='bom_dependencies.json'
        )

    def test_bom_v1_2_dependencies(self) -> None:
        self._validate_json_bom(
            bom=get_bom_with_dependencies_valid(), schema_version=SchemaVersion.V1_2,
            fixture='bom_dependencies.json'
        )

    def test_bom_v1_4_dependencies_for_bom_component(self) -> None:
        self._validate_json_bom(
            bom=get_bom_with_metadata_component_and_dependencies(), schema_version=SchemaVersion.V1_4,
            fixture='bom_dependencies_component.json'
        )

    def test_bom_v1_3_dependencies_for_bom_component(self) -> None:
        self._validate_json_bom(
            bom=get_bom_with_metadata_component_and_dependencies(), schema_version=SchemaVersion.V1_3,
            fixture='bom_dependencies_component.json'
        )

    def test_bom_v1_2_dependencies_for_bom_component(self) -> None:
        self._validate_json_bom(
            bom=get_bom_with_metadata_component_and_dependencies(), schema_version=SchemaVersion.V1_2,
            fixture='bom_dependencies_component.json'
        )

    def test_bom_v1_4_issue_275_components(self) -> None:
        self._validate_json_bom(
            bom=get_bom_for_issue_275_components(), schema_version=SchemaVersion.V1_4,
            fixture='bom_issue_275_components.json'
        )

    def test_bom_v1_3_issue_275_components(self) -> None:
        self._validate_json_bom(
            bom=get_bom_for_issue_275_components(), schema_version=SchemaVersion.V1_3,
            fixture='bom_issue_275_components.json'
        )

    def test_bom_v1_2_issue_275_components(self) -> None:
        self._validate_json_bom(
            bom=get_bom_for_issue_275_components(), schema_version=SchemaVersion.V1_2,
            fixture='bom_issue_275_components.json'
        )

    # Helper methods
    def _validate_json_bom(self, bom: Bom, schema_version: SchemaVersion, fixture: str) -> None:
        outputter = get_instance(bom=bom, output_format=OutputFormat.JSON, schema_version=schema_version)
        self.assertEqual(outputter.schema_version, schema_version)
        with open(
                join(dirname(__file__), f'fixtures/json/{schema_version.to_version()}/{fixture}')) as expected_json:
            self.assertValidAgainstSchema(bom_json=outputter.output_as_string(), schema_version=schema_version)
            self.assertEqualJsonBom(expected_json.read(), outputter.output_as_string())
            expected_json.close()

    def _validate_json_bom_not_supported(self, bom: Bom, schema_version: SchemaVersion) -> None:
        with self.assertRaises(FormatNotSupportedException):
            outputter = get_instance(bom=bom, output_format=OutputFormat.JSON, schema_version=schema_version)
            outputter.output_as_string()
