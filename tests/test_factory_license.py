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
import unittest.mock

from cyclonedx.exception.factory import InvalidLicenseExpressionException, InvalidSpdxLicenseException
from cyclonedx.factory.license import LicenseChoiceFactory, LicenseFactory
from cyclonedx.model import AttachedText, License, LicenseChoice, XsUri


class TestFactoryLicense(unittest.TestCase):

    def test_make_from_string_with_id(self) -> None:
        text = unittest.mock.NonCallableMock(spec=AttachedText)
        url = unittest.mock.NonCallableMock(spec=XsUri)
        expected = License(id_='bar', text=text, url=url)

        with unittest.mock.patch('cyclonedx.factory.license.spdx_fixup', return_value='bar'):
            actual = LicenseFactory.make_from_string('foo', license_text=text, license_url=url)

        self.assertEqual(expected, actual)

    def test_make_from_string_with_name(self) -> None:
        text = unittest.mock.NonCallableMock(spec=AttachedText)
        url = unittest.mock.NonCallableMock(spec=XsUri)
        expected = License(name='foo', text=text, url=url)

        with unittest.mock.patch('cyclonedx.factory.license.spdx_fixup', return_value=None):
            actual = LicenseFactory.make_from_string('foo', license_text=text, license_url=url)

        self.assertEqual(expected, actual)

    def test_make_with_id(self) -> None:
        text = unittest.mock.NonCallableMock(spec=AttachedText)
        url = unittest.mock.NonCallableMock(spec=XsUri)
        expected = License(id_='bar', text=text, url=url)

        with unittest.mock.patch('cyclonedx.factory.license.spdx_fixup', return_value='bar'):
            actual = LicenseFactory.make_with_id('foo', text=text, url=url)

        self.assertEqual(expected, actual)

    def test_make_with_id_raises(self) -> None:
        with self.assertRaises(InvalidSpdxLicenseException, msg='foo'):
            with unittest.mock.patch('cyclonedx.factory.license.spdx_fixup', return_value=None):
                LicenseFactory.make_with_id('foo')

    def test_make_with_name(self) -> None:
        text = unittest.mock.NonCallableMock(spec=AttachedText)
        url = unittest.mock.NonCallableMock(spec=XsUri)
        expected = License(name='foo', text=text, url=url)
        actual = LicenseFactory.make_with_name('foo', text=text, url=url)
        self.assertEqual(expected, actual)


class TestFactoryLicenseChoice(unittest.TestCase):

    def test_make_from_string_with_compound_expression(self) -> None:
        expected = LicenseChoice(expression='foo')
        factory = LicenseChoiceFactory(license_factory=unittest.mock.MagicMock(spec=LicenseFactory))

        with unittest.mock.patch('cyclonedx.factory.license.is_spdx_compound_expression', return_value=True):
            actual = factory.make_from_string('foo')

        self.assertEqual(expected, actual)

    def test_make_from_string_with_license(self) -> None:
        license_ = unittest.mock.NonCallableMock(spec=License)
        expected = LicenseChoice(license_=license_)
        license_factory = unittest.mock.MagicMock(spec=LicenseFactory)
        license_factory.make_from_string.return_value = license_
        factory = LicenseChoiceFactory(license_factory=license_factory)

        with unittest.mock.patch('cyclonedx.factory.license.is_spdx_compound_expression', return_value=False):
            actual = factory.make_from_string('foo')

        self.assertEqual(expected, actual)
        self.assertIs(license_, actual.license_)
        license_factory.make_from_string.assert_called_once_with('foo', license_text=None, license_url=None)

    def test_make_with_compound_expression(self) -> None:
        expected = LicenseChoice(expression='foo')
        factory = LicenseChoiceFactory(license_factory=unittest.mock.MagicMock(spec=LicenseFactory))

        with unittest.mock.patch('cyclonedx.factory.license.is_spdx_compound_expression', return_value=True):
            actual = factory.make_with_compound_expression('foo')

        self.assertEqual(expected, actual)

    def test_make_with_compound_expression_raises(self) -> None:
        factory = LicenseChoiceFactory(license_factory=unittest.mock.MagicMock(spec=LicenseFactory))
        with unittest.mock.patch('cyclonedx.factory.license.is_spdx_compound_expression', return_value=False):
            with self.assertRaises(InvalidLicenseExpressionException, msg='foo'):
                factory.make_with_compound_expression('foo')

    def test_make_with_license(self) -> None:
        text = unittest.mock.NonCallableMock(spec=AttachedText)
        url = unittest.mock.NonCallableMock(spec=XsUri)
        license_ = unittest.mock.NonCallableMock(spec=License)
        expected = LicenseChoice(license_=license_)
        license_factory = unittest.mock.MagicMock(spec=LicenseFactory)
        license_factory.make_from_string.return_value = license_
        factory = LicenseChoiceFactory(license_factory=license_factory)

        with unittest.mock.patch('cyclonedx.factory.license.is_spdx_compound_expression', return_value=False):
            actual = factory.make_with_license('foo', license_text=text, license_url=url)

        self.assertEqual(expected, actual)
        self.assertIs(license_, actual.license_)
        license_factory.make_from_string.assert_called_once_with('foo', license_text=text, license_url=url)
