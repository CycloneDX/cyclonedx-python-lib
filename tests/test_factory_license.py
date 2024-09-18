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

import unittest
import unittest.mock

from cyclonedx.exception.factory import InvalidLicenseExpressionException, InvalidSpdxLicenseException
from cyclonedx.factory.license import LicenseFactory
from cyclonedx.model import AttachedText, XsUri
from cyclonedx.model.license import DisjunctiveLicense, LicenseAcknowledgement, LicenseExpression


class TestFactoryLicense(unittest.TestCase):

    def test_make_from_string_with_id(self) -> None:
        text = unittest.mock.NonCallableMock(spec=AttachedText)
        url = unittest.mock.NonCallableMock(spec=XsUri)
        acknowledgement = unittest.mock.NonCallableMock(spec=LicenseAcknowledgement)
        expected = DisjunctiveLicense(id='bar', text=text, url=url, acknowledgement=acknowledgement)

        with unittest.mock.patch('cyclonedx.factory.license.spdx_fixup', return_value='bar'), \
                unittest.mock.patch('cyclonedx.factory.license.is_spdx_compound_expression', return_value=True):
            actual = LicenseFactory().make_from_string('foo',
                                                       license_text=text,
                                                       license_url=url,
                                                       license_acknowledgement=acknowledgement)

        self.assertEqual(expected, actual)

    def test_make_from_string_with_name(self) -> None:
        text = unittest.mock.NonCallableMock(spec=AttachedText)
        url = unittest.mock.NonCallableMock(spec=XsUri)
        acknowledgement = unittest.mock.NonCallableMock(spec=LicenseAcknowledgement)
        expected = DisjunctiveLicense(name='foo', text=text, url=url, acknowledgement=acknowledgement)

        with unittest.mock.patch('cyclonedx.factory.license.spdx_fixup', return_value=None), \
                unittest.mock.patch('cyclonedx.factory.license.is_spdx_compound_expression', return_value=False):
            actual = LicenseFactory().make_from_string('foo',
                                                       license_text=text,
                                                       license_url=url,
                                                       license_acknowledgement=acknowledgement)

        self.assertEqual(expected, actual)

    def test_make_from_string_with_expression(self) -> None:
        acknowledgement = unittest.mock.NonCallableMock(spec=LicenseAcknowledgement)
        expected = LicenseExpression('foo', acknowledgement=acknowledgement)

        with unittest.mock.patch('cyclonedx.factory.license.spdx_fixup', return_value=None), \
                unittest.mock.patch('cyclonedx.factory.license.is_spdx_compound_expression', return_value=True):
            actual = LicenseFactory().make_from_string('foo',
                                                       license_acknowledgement=acknowledgement)

        self.assertEqual(expected, actual)

    def test_make_with_id(self) -> None:
        text = unittest.mock.NonCallableMock(spec=AttachedText)
        url = unittest.mock.NonCallableMock(spec=XsUri)
        acknowledgement = unittest.mock.NonCallableMock(spec=LicenseAcknowledgement)
        expected = DisjunctiveLicense(id='bar', text=text, url=url, acknowledgement=acknowledgement)

        with unittest.mock.patch('cyclonedx.factory.license.spdx_fixup', return_value='bar'):
            actual = LicenseFactory().make_with_id(spdx_id='foo', text=text, url=url, acknowledgement=acknowledgement)

        self.assertEqual(expected, actual)

    def test_make_with_id_raises(self) -> None:
        with self.assertRaises(InvalidSpdxLicenseException, msg='foo'):
            with unittest.mock.patch('cyclonedx.factory.license.spdx_fixup', return_value=None):
                LicenseFactory().make_with_id(spdx_id='foo')

    def test_make_with_name(self) -> None:
        text = unittest.mock.NonCallableMock(spec=AttachedText)
        url = unittest.mock.NonCallableMock(spec=XsUri)
        acknowledgement = unittest.mock.NonCallableMock(spec=LicenseAcknowledgement)
        expected = DisjunctiveLicense(name='foo', text=text, url=url, acknowledgement=acknowledgement)
        actual = LicenseFactory().make_with_name(name='foo', text=text, url=url, acknowledgement=acknowledgement)
        self.assertEqual(expected, actual)

    def test_make_with_expression(self) -> None:
        acknowledgement = unittest.mock.NonCallableMock(spec=LicenseAcknowledgement)
        expected = LicenseExpression('foo', acknowledgement=acknowledgement)
        with unittest.mock.patch('cyclonedx.factory.license.is_spdx_compound_expression', return_value=True):
            actual = LicenseFactory().make_with_expression(expression='foo', acknowledgement=acknowledgement)
        self.assertEqual(expected, actual)

    def test_make_with_expression_raises(self) -> None:
        with self.assertRaises(InvalidLicenseExpressionException, msg='foo'):
            with unittest.mock.patch('cyclonedx.factory.license.is_spdx_compound_expression', return_value=False):
                LicenseFactory().make_with_expression('foo')
