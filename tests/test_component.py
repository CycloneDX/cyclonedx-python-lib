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
from unittest import TestCase

from packageurl import PackageURL

from cyclonedx.model.component import Component


class TestComponent(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls._component: Component = Component(name='setuptools', version='50.3.2')
        cls._component_with_qualifiers: Component = Component(name='setuptools', version='50.3.2',
                                                              qualifiers='extension=tar.gz')
        cls._component_generic_file: Component = Component(
            name='/test.py', version='UNKNOWN', package_url_type='generic'
        )

    def test_purl_correct(self):
        self.assertEqual(
            str(PackageURL(
                type='pypi', name='setuptools', version='50.3.2'
            )),
            TestComponent._component.get_purl()
        )

    def test_purl_incorrect_version(self):
        purl = PackageURL(
            type='pypi', name='setuptools', version='50.3.1'
        )
        self.assertNotEqual(
            str(purl),
            TestComponent._component.get_purl()
        )
        self.assertEqual(purl.type, 'pypi')
        self.assertEqual(purl.name, 'setuptools')
        self.assertEqual(purl.version, '50.3.1')

    def test_purl_incorrect_name(self):
        purl = PackageURL(
            type='pypi', name='setuptoolz', version='50.3.2'
        )
        self.assertNotEqual(
            str(purl),
            TestComponent._component.get_purl()
        )
        self.assertEqual(purl.type, 'pypi')
        self.assertEqual(purl.name, 'setuptoolz')
        self.assertEqual(purl.version, '50.3.2')

    def test_purl_with_qualifiers(self):
        purl = PackageURL(
            type='pypi', name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'
        )
        self.assertEqual(
            str(purl),
            TestComponent._component_with_qualifiers.get_purl()
        )
        self.assertNotEqual(
            str(purl),
            TestComponent._component.get_purl()
        )
        self.assertEqual(purl.qualifiers, {'extension': 'tar.gz'})

    def test_as_package_url_1(self):
        purl = PackageURL(
            type='pypi', name='setuptools', version='50.3.2'
        )
        self.assertEqual(TestComponent._component.to_package_url(), purl)

    def test_as_package_url_2(self):
        purl = PackageURL(
            type='pypi', name='setuptools', version='50.3.1'
        )
        self.assertNotEqual(TestComponent._component.to_package_url(), purl)

    def test_as_package_url_3(self):
        purl = PackageURL(
            type='pypi', name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'
        )
        self.assertEqual(TestComponent._component_with_qualifiers.to_package_url(), purl)

    def test_custom_package_url_type(self):
        purl = PackageURL(
            type='generic', name='/test.py', version='UNKNOWN'
        )
        self.assertEqual(TestComponent._component_generic_file.to_package_url(), purl)

    def test_from_file_with_path_for_bom(self):
        test_file = join(dirname(__file__), 'fixtures/bom_v1.3_setuptools.xml')
        c = Component.for_file(absolute_file_path=test_file, path_for_bom='fixtures/bom_v1.3_setuptools.xml')
        self.assertEqual(c.get_name(), 'fixtures/bom_v1.3_setuptools.xml')
        self.assertEqual(c.get_version(), '0.0.0-16932e52ed1e')
        purl = PackageURL(
            type='generic', name='fixtures/bom_v1.3_setuptools.xml', version='0.0.0-16932e52ed1e'
        )
        self.assertEqual(c.to_package_url(), purl)
        self.assertEqual(len(c.get_hashes()), 1)
