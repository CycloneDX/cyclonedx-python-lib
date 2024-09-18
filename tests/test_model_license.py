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


from random import shuffle
from unittest import TestCase
from unittest.mock import MagicMock

from cyclonedx.exception.model import MutuallyExclusivePropertiesException
from cyclonedx.model import AttachedText, XsUri
from cyclonedx.model.license import DisjunctiveLicense, LicenseExpression
from tests import reorder


class TestModelDisjunctiveLicense(TestCase):
    def test_create_complete_id(self) -> None:
        text = MagicMock(spec=AttachedText)
        url = MagicMock(spec=XsUri)
        license = DisjunctiveLicense(id='foo', text=text, url=url)
        self.assertEqual('foo', license.id)
        self.assertIsNone(license.name)
        self.assertIs(text, license.text)
        self.assertIs(url, license.url)

    def test_update_id_name(self) -> None:
        license = DisjunctiveLicense(id='foo')
        self.assertEqual('foo', license.id)
        self.assertIsNone(license.name)
        license.name = 'bar'
        self.assertIsNone(license.id)
        self.assertEqual('bar', license.name)

    def test_create_complete_named(self) -> None:
        text = MagicMock(spec=AttachedText)
        url = MagicMock(spec=XsUri)
        license = DisjunctiveLicense(name='foo', text=text, url=url)
        self.assertIsNone(license.id)
        self.assertEqual('foo', license.name)
        self.assertIs(text, license.text)
        self.assertIs(url, license.url)

    def test_update_name_id(self) -> None:
        license = DisjunctiveLicense(name='foo')
        self.assertEqual('foo', license.name)
        self.assertIsNone(license.id)
        license.id = 'bar'
        self.assertIsNone(license.name)
        self.assertEqual('bar', license.id)

    def test_throws_when_no_id_nor_name(self) -> None:
        with self.assertRaises(MutuallyExclusivePropertiesException):
            DisjunctiveLicense(id=None, name=None)

    def test_prefers_id_over_name(self) -> None:
        with self.assertWarnsRegex(
                RuntimeWarning,
                'Both `id` and `name` have been supplied - `name` will be ignored!'):
            license = DisjunctiveLicense(id='foo', name='bar')
        self.assertEqual('foo', license.id)
        self.assertEqual(None, license.name)

    def test_equal(self) -> None:
        a = DisjunctiveLicense(id='foo', name='bar')
        b = DisjunctiveLicense(id='foo', name='bar')
        c = DisjunctiveLicense(id='bar', name='foo')
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(a, 'foo')


class TestModelLicenseExpression(TestCase):
    def test_create(self) -> None:
        license = LicenseExpression('foo')
        self.assertEqual('foo', license.value)

    def test_update(self) -> None:
        license = LicenseExpression('foo')
        self.assertEqual('foo', license.value)
        license.value = 'bar'
        self.assertEqual('bar', license.value)

    def test_equal(self) -> None:
        a = LicenseExpression('foo')
        b = LicenseExpression('foo')
        c = LicenseExpression('bar')
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(a, 'foo')


class TestModelLicense(TestCase):

    def test_sort_mixed(self) -> None:
        expected_order = [1, 2, 0]
        licenses = [
            DisjunctiveLicense(name='my license'),
            LicenseExpression(value='MIT or Apache-2.0'),
            DisjunctiveLicense(id='MIT'),
        ]
        expected_licenses = reorder(licenses, expected_order)
        shuffle(licenses)
        sorted_licenses = sorted(licenses)
        self.assertListEqual(sorted_licenses, expected_licenses)
