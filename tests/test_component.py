# encoding: utf-8

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

from unittest import TestCase

from packageurl import PackageURL

from cyclonedx.model.component import Component


class TestComponent(TestCase):
    _component: Component

    @classmethod
    def setUpClass(cls) -> None:
        cls._component = Component(name='setuptools', version='50.3.2').get_purl()
        cls._component_with_qualifiers = Component(name='setuptools', version='50.3.2',
                                                   qualifiers='extension=tar.gz').get_purl()

    def test_purl_correct(self):
        self.assertEqual(
            str(PackageURL(
                type='pypi', name='setuptools', version='50.3.2'
            )),
            TestComponent._component
        )

    def test_purl_incorrect_version(self):
        purl = PackageURL(
            type='pypi', name='setuptools', version='50.3.1'
        )
        self.assertNotEqual(
            str(purl),
            TestComponent._component
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
            TestComponent._component
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
            TestComponent._component_with_qualifiers
        )
        self.assertNotEqual(
            str(purl),
            TestComponent._component
        )
        self.assertEqual(purl.qualifiers, {'extension': 'tar.gz'})
