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
from os.path import join
from unittest.mock import Mock, patch
from uuid import UUID

from cyclonedx.model.bom import Bom
from cyclonedx.output import get_instance
from cyclonedx.schema import SchemaVersion
from .base import BaseXmlTestCase, SnapshotCompareMixin
from .data import (
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
    get_bom_with_dependencies_hanging,
    get_bom_with_dependencies_valid,
    get_bom_with_external_references,
    get_bom_with_metadata_component_and_dependencies,
    get_bom_with_nested_services,
    get_bom_with_services_complex,
    get_bom_with_services_simple,
)

from . import SNAPSHOTS_DIRECTORY
from ddt import ddt, data, unpack

RELEVANT_TESTDATA_DIRECTORY = join(SNAPSHOTS_DIRECTORY, 'xml')

_RELEVANT_SCHEMA_VERSIONS = (SchemaVersion.V1_4,
                             SchemaVersion.V1_3,
                             SchemaVersion.V1_2,
                             SchemaVersion.V1_1,
                             SchemaVersion.V1_0)


@patch('cyclonedx.model.ThisTool._version', 'TESTING')
@ddt
class TestOutputXml(BaseXmlTestCase, SnapshotCompareMixin):

    @data(*_RELEVANT_SCHEMA_VERSIONS)
    def test_bom_external_references(self, schema_version: SchemaVersion) -> None:
        self._test_output_as_expected(get_bom_with_external_references(),
                                      schema_version,
                                      'bom_external_references')

    @data(*_RELEVANT_SCHEMA_VERSIONS)
    def test_bom_setuptools(self, schema_version: SchemaVersion) -> None:
        self._test_output_as_expected(get_bom_with_component_setuptools_basic(),
                                      schema_version,
                                      'bom_setuptools')

    @data(*_RELEVANT_SCHEMA_VERSIONS)
    def test_bom_setuptools_with_cpe(self, schema_version: SchemaVersion) -> None:
        self._test_output_as_expected(get_bom_with_component_setuptools_with_cpe(),
                                      schema_version,
                                      'bom_setuptools_with_cpe')

    @data(*_RELEVANT_SCHEMA_VERSIONS)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_4))
    def test_bom_setuptools_complete(self, schema_version: SchemaVersion, *_, **__) -> None:
        self._test_output_as_expected(get_bom_with_component_setuptools_complete(),
                                      schema_version,
                                      'bom_setuptools_complete')

    @data(*_RELEVANT_SCHEMA_VERSIONS)
    def test_bom_toml_hashes_and_references(self, schema_version: SchemaVersion) -> None:
        self._test_output_as_expected(get_bom_with_component_toml_1(),
                                      schema_version,
                                      'bom_toml_hashes_and_references')

    @data(*_RELEVANT_SCHEMA_VERSIONS)
    def test_bom_setuptools_no_version(self, schema_version: SchemaVersion) -> None:
        self._test_output_as_expected(get_bom_with_component_setuptools_no_component_version(),
                                      schema_version,
                                      'bom_setuptools_no_version')

    @data(*_RELEVANT_SCHEMA_VERSIONS)
    def test_bom_setuptools_with_release_notes(self, schema_version: SchemaVersion) -> None:
        self._test_output_as_expected(get_bom_with_component_setuptools_with_release_notes(),
                                      schema_version,
                                      'bom_setuptools_with_release_notes')

    @data(*_RELEVANT_SCHEMA_VERSIONS)
    def test_bom_setuptools_with_vulnerabilities(self, schema_version: SchemaVersion) -> None:
        self._test_output_as_expected(get_bom_with_component_setuptools_with_vulnerability(),
                                      schema_version,
                                      'bom_setuptools_with_vulnerabilities')

    @data(*_RELEVANT_SCHEMA_VERSIONS)
    def test_bom_with_component_setuptools_with_vulnerability(self, schema_version: SchemaVersion) -> None:
        self._test_output_as_expected(get_bom_with_component_setuptools_with_vulnerability(),
                                      schema_version,
                                      'bom_with_component_setuptools_with_vulnerability')

    @data(*_RELEVANT_SCHEMA_VERSIONS)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_6))
    def test_bom_with_full_metadata(self, schema_version: SchemaVersion, *_, **__) -> None:
        self._test_output_as_expected(get_bom_just_complete_metadata(),
                                      schema_version,
                                      'bom_with_full_metadata')

    @data(*_RELEVANT_SCHEMA_VERSIONS)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_3))
    @patch('cyclonedx.model.service.uuid4', side_effect=TEST_UUIDS)
    def test_bom_services_simple(self, schema_version: SchemaVersion,  *_, **__) -> None:
        with self.assertWarns(UserWarning):
            self._test_output_as_expected(get_bom_with_services_simple(),
                                          schema_version,
                                          'bom_services_simple')

    @data(*_RELEVANT_SCHEMA_VERSIONS)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_4))
    @patch('cyclonedx.model.service.uuid4', side_effect=TEST_UUIDS)
    def test_bom_services_complex(self, schema_version: SchemaVersion,  *_, **__) -> None:
        with self.assertWarns(UserWarning):
            self._test_output_as_expected(get_bom_with_services_complex(),
                                          schema_version,
                                          'bom_services_complex')

    @data(*_RELEVANT_SCHEMA_VERSIONS)
    @patch('cyclonedx.model.component.uuid4', return_value=UUID(MOCK_UUID_6))
    @patch('cyclonedx.model.service.uuid4', side_effect=TEST_UUIDS)
    def test_bom_services_nested(self, schema_version: SchemaVersion,  *_, **__) -> None:
        with self.assertWarns(UserWarning):
            self._test_output_as_expected(get_bom_with_nested_services(),
                                          schema_version,
                                          'bom_services_nested')

    @data(*_RELEVANT_SCHEMA_VERSIONS)
    def test_bom_dependencies(self, schema_version: SchemaVersion) -> None:
        self._test_output_as_expected(get_bom_with_dependencies_valid(),
                                      schema_version,
                                      'bom_dependencies')

    @data(*_RELEVANT_SCHEMA_VERSIONS)
    def test_bom_dependencies_component(self, schema_version: SchemaVersion) -> None:
        self._test_output_as_expected(get_bom_with_metadata_component_and_dependencies(),
                                      schema_version,
                                      'bom_dependencies_component')

    @data(*_RELEVANT_SCHEMA_VERSIONS)
    def test_bom_issue_275_components(self, schema_version: SchemaVersion) -> None:
        self._test_output_as_expected(get_bom_for_issue_275_components(),
                                      schema_version,
                                      'bom_issue_275_components')

    @data(*_RELEVANT_SCHEMA_VERSIONS)
    def test_bom_with_dependencies_hanging(self, schema_version: SchemaVersion) -> None:
        self._test_output_as_expected(get_bom_with_dependencies_hanging(),
                                      schema_version,
                                      'bom_with_dependencies_hanging')

    # region Helper methods

    def _test_output_as_expected(self, bom: Bom, schema_version: SchemaVersion, snapshot_name: str) -> None:
        outputter = get_instance(bom=bom, schema_version=schema_version)
        self.assertEqual(outputter.schema_version, schema_version)
        output_as_string = outputter.output_as_string()
        self.assertValidAgainstSchema(bom_xml=output_as_string, schema_version=schema_version)
        self.assertEqualSnapshot(output_as_string, f'xml_{snapshot_name}_{schema_version.to_version()}.xml')

    # endregion Helper methods
