# This file is part of CycloneDX Python Library
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
from unittest import TestCase

from cyclonedx.contrib.component.builders import ComponentBuilder
from cyclonedx.model.component import Component
from tests import OWN_DATA_DIRECTORY
from tests._data.models import get_component_setuptools_simple


class TestComponent(TestCase):

    def test_purl_correct(self) -> None:
        self.assertEqual(
            'pkg:pypi/setuptools@50.3.2?extension=tar.gz',
            get_component_setuptools_simple().purl
        )

    def test_purl_incorrect_version(self) -> None:
        incorrect_purl = 'pkg:pypi/setuptools@50.3.1'
        self.assertNotEqual(
            incorrect_purl,
            get_component_setuptools_simple().purl
        )

    def test_purl_incorrect_name(self) -> None:
        incorrect_purl = 'pkg:pypi/setuptoolz@50.3.2?extension=tar.gz'
        self.assertNotEqual(
            incorrect_purl,
            get_component_setuptools_simple().purl
        )

    def test_from_xml_file_with_path_for_bom(self) -> None:
        test_file = join(OWN_DATA_DIRECTORY, 'xml', '1.4', 'bom_setuptools.xml')
        c = Component.for_file(absolute_file_path=test_file, path_for_bom='fixtures/bom_setuptools.xml')
        sha1_hash: str = ComponentBuilder._file_sha1sum(filename=test_file)
        expected_version = f'0.0.0-{sha1_hash[0:12]}'
        self.assertEqual(c.name, 'fixtures/bom_setuptools.xml')
        self.assertEqual(c.version, expected_version)
        expected_purl = f'pkg:generic/fixtures/bom_setuptools.xml@{expected_version}'
        self.assertEqual(c.purl, expected_purl)
        self.assertEqual(len(c.hashes), 1)
