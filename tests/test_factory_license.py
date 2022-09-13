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

import itertools
import unittest
import unittest.mock
from typing import Optional

from ddt import data, ddt, idata, unpack

from cyclonedx.exception.factory import InvalidLicenseExpressionException, InvalidSpdxLicenseException
from cyclonedx.factory.license import LicenseChoiceFactory, LicenseFactory
from cyclonedx.model import AttachedText, License, LicenseChoice, XsUri


@ddt
class TestFactoryLicense(unittest.TestCase):

    @idata(itertools.product(
        ['MIT'],
        ['MIT', 'mit', 'MiT'],
        [None, unittest.mock.NonCallableMock(spec=AttachedText)],
        [None, unittest.mock.NonCallableMock(spec=XsUri)],
    ))
    @unpack
    def test_make_from_string_with_id(self, expected_id: str,
                                      id_: str, text: Optional[AttachedText], url: Optional[XsUri]) -> None:
        expected = License(spdx_license_id=expected_id, license_text=text, license_url=url)
        actual = LicenseFactory().make_from_string(id_, license_text=text, license_url=url)
        self.assertEqual(expected, actual)

    @idata(itertools.product(
        ['foo bar'],
        [None, unittest.mock.NonCallableMock(spec=AttachedText)],
        [None, unittest.mock.NonCallableMock(spec=XsUri)],
    ))
    @unpack
    def test_make_from_string_with_name(self, name: str, text: Optional[AttachedText], url: Optional[XsUri]) -> None:
        expected = License(license_name=name, license_text=text, license_url=url)
        actual = LicenseFactory().make_from_string(name, license_text=text, license_url=url)
        self.assertEqual(expected, actual)

    @idata(itertools.product(
        ['MIT'],
        ['MIT', 'mit', 'MiT'],
        [None, unittest.mock.NonCallableMock(spec=AttachedText)],
        [None, unittest.mock.NonCallableMock(spec=XsUri)],
    ))
    @unpack
    def test_make_with_id(self, expected_id: str,
                          id_: str, text: Optional[AttachedText], url: Optional[XsUri]) -> None:
        expected = License(spdx_license_id=expected_id, license_text=text, license_url=url)
        actual = LicenseFactory().make_with_id(id_, license_text=text, license_url=url)
        self.assertEqual(expected, actual)

    @data(
        'FOO BaR',
    )
    def test_make_with_id_raises(self, invalid_id: str) -> None:
        factory = LicenseFactory()
        with self.assertRaises(InvalidSpdxLicenseException, msg=invalid_id):
            factory.make_with_id(invalid_id)

    @idata(itertools.product(
        ['foo'],
        [None, unittest.mock.NonCallableMock(spec=AttachedText)],
        [None, unittest.mock.NonCallableMock(spec=XsUri)],
    ))
    @unpack
    def test_make_with_name(self, name: str, text: Optional[AttachedText], url: Optional[XsUri]) -> None:
        expected = License(license_name=name, license_text=text, license_url=url)
        actual = LicenseFactory().make_with_name(name, license_text=text, license_url=url)
        self.assertEqual(expected, actual)


VALID_EXPRESSIONS = {
    # for valid test data see the spec: https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/
    '(MIT WITH Apache-2.0)',
    '(BSD-2-Clause OR Apache-2.0)',
}


@ddt
class TestFactoryLicenseChoice(unittest.TestCase):

    @idata(VALID_EXPRESSIONS)
    def test_make_from_string_with_compound_expression(self, compound_expression: str) -> None:
        expected = LicenseChoice(license_expression=compound_expression)
        license_factory = unittest.mock.MagicMock(spec=LicenseFactory)
        actual = LicenseChoiceFactory(license_factory=license_factory).make_from_string(
            compound_expression)
        self.assertEqual(expected, actual)

    def test_make_from_string_with_license(self) -> None:
        license_ = unittest.mock.NonCallableMock(spec=License)
        expected = LicenseChoice(license_=license_)
        license_factory = unittest.mock.MagicMock(spec=LicenseFactory)
        license_factory.make_from_string.return_value = license_
        actual = LicenseChoiceFactory(license_factory=license_factory).make_from_string('foo')
        self.assertEqual(expected, actual)
        self.assertIs(license_, actual.license)
        license_factory.make_from_string.assert_called_once_with('foo', license_text=None, license_url=None)

    @idata(VALID_EXPRESSIONS)
    def test_make_with_compound_expression(self, compound_expression: str) -> None:
        expected = LicenseChoice(license_expression=compound_expression)
        license_factory = unittest.mock.MagicMock(spec=LicenseFactory)
        actual = LicenseChoiceFactory(license_factory=license_factory).make_with_compound_expression(
            compound_expression)
        self.assertEqual(expected, actual)

    @data(
        'Foo Bar',
    )
    def test_make_with_compound_expression_raises(self, invalid_expression: str) -> None:
        factory = LicenseChoiceFactory(license_factory=unittest.mock.MagicMock(spec=LicenseFactory))
        with self.assertRaises(InvalidLicenseExpressionException, msg=invalid_expression):
            factory.make_with_compound_expression(invalid_expression)

    @idata(itertools.product(
        ['foo'],
        [None, unittest.mock.NonCallableMock(spec=AttachedText)],
        [None, unittest.mock.NonCallableMock(spec=XsUri)],
    ))
    @unpack
    def test_make_with_license(self, name_or_spdx: str, text: Optional[AttachedText], url: Optional[XsUri]) -> None:
        license_ = unittest.mock.NonCallableMock(spec=License)
        expected = LicenseChoice(license_=license_)
        license_factory = unittest.mock.MagicMock(spec=LicenseFactory)
        license_factory.make_from_string.return_value = license_
        actual = LicenseChoiceFactory(license_factory=license_factory).make_with_license(
            name_or_spdx, license_text=text, license_url=url)
        self.assertEqual(expected, actual)
        self.assertIs(license_, actual.license)
        license_factory.make_from_string.assert_called_once_with(name_or_spdx, license_text=text, license_url=url)
