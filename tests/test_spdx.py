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

from itertools import chain
from unittest import TestCase

from ddt import data, ddt, idata, unpack
from license_expression import get_license_index

from cyclonedx import spdx

KNOWN_SPDX_IDS = ([entry['spdx_license_key'] for entry in get_license_index()
                   if entry['spdx_license_key'] and not entry['is_exception']]
                  + [item for license_entry in get_license_index()
                     for item in license_entry['other_spdx_license_keys'] if not license_entry['is_exception']])


VALID_SPDX_LICENSE_IDENTIFIERS = {
    # for valid SPDX license identifiers see spec: https://spdx.org/licenses/, list contained in license-expression
    'Apache-2.0',
    'MIT',
    # deprecated, but valid license identifier
    'AGPL-1.0'
}


VALID_SIMPLE_EXPRESSIONS = {
    # for valid test data see also spec: https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/
    # an SPDX license identifier
    'MIT',
    # a custom license identifier (from license-expression module)
    'LicenseRef-scancode-3com-microcode',
    # a custom license identifier (not from license expression module)
    'LicenseRef-my-own-license'
}


VALID_COMPOUND_EXPRESSIONS = {
    # for valid test data see the spec: https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/
    # for valid exceptions see the spec: https://spdx.org/licenses/exceptions-index.html
    '(MIT AND Apache-2.0)',
    'BSD-2-Clause OR Apache-2.0',
    'GPL-2.0 WITH Bison-exception-2.2'
}


INVALID_SPDX_LICENSE_IDENTIFIERS = {
    'MiT',
    '389-exception',
    '',
    'Apache 2.0',
    'MIT OR Apache-2.0',
    'LicenseRef-custom-identifier',
    None
}


INVALID_SIMPLE_EXPRESSIONS = {
    'something_invalid'
    'something invalid',
    'Apache License, Version 2.0',
    '',
    '.MIT',
    'MIT OR Apache-2.0',
    'LicenseRef-Invalid#ID',
    None
}


INVALID_COMPOUND_EXPRESSIONS = {
    'MIT AND Apache-2.0 OR something-unknown'
    'something invalid',
    '(c) John Doe',
    'Apache License, Version 2.0',
    '',
    'MIT',
    'MIT. OR Apache-2.0',
    'MIT WITH Apache-2.0',
    'MIT OR Apache-2.0)',
    '(MIT OR Apache-2.0',
    None
}


@ddt
class TestSpdxIsSupported(TestCase):

    @idata(KNOWN_SPDX_IDS)
    def test_positive(self, supported_value: str) -> None:
        actual = spdx.is_supported_id(supported_value)
        self.assertTrue(actual)

    @data(
        'something unsupported',
        # somehow case-twisted values
        'MiT',
        'mit',
    )
    def test_negative(self, unsupported_value: str) -> None:
        actual = spdx.is_supported_id(unsupported_value)
        self.assertFalse(actual)


@ddt
class TestSpdxFixup(TestCase):

    @idata(chain(
        # original value
        ((v, v) for v in KNOWN_SPDX_IDS),
        # somehow case-twisted values
        ((v.lower(), v) for v in KNOWN_SPDX_IDS),
        ((v.upper(), v) for v in KNOWN_SPDX_IDS)
    ))
    @unpack
    def test_positive(self, fixable: str, expected_fixed: str) -> None:
        actual = spdx.fixup_id(fixable)
        self.assertEqual(expected_fixed, actual,
                         f'<{fixable}> was expected to get <{expected_fixed}>, but it is <{actual}>')

    @data(
        'something unfixable',
    )
    def test_negative(self, unfixable: str) -> None:
        actual = spdx.fixup_id(unfixable)
        self.assertIsNone(actual)


@ddt
class TestSpdxIsSpdxLicenseIdentifier(TestCase):

    @idata(VALID_SPDX_LICENSE_IDENTIFIERS)
    def test_positive(self, valid_identifier: str) -> None:
        actual = spdx.is_spdx_license_id(valid_identifier)
        self.assertTrue(actual)

    @idata(INVALID_SPDX_LICENSE_IDENTIFIERS)
    def test_negative(self, invalid_identifier: str) -> None:
        actual = spdx.is_spdx_license_id(invalid_identifier)
        self.assertFalse(actual)


@ddt
class TestSpdxIsSimpleExpression(TestCase):

    @idata(VALID_SIMPLE_EXPRESSIONS)
    def test_positive(self, valid_simple_expression: str) -> None:
        actual = spdx.is_simple_expression(valid_simple_expression)
        self.assertTrue(actual)

    @idata(INVALID_SIMPLE_EXPRESSIONS)
    def test_negative(self, invalid_simple_expression: str) -> None:
        actual = spdx.is_simple_expression(invalid_simple_expression)
        self.assertFalse(actual)


@ddt
class TestSpdxIsCompoundExpression(TestCase):

    @idata(VALID_COMPOUND_EXPRESSIONS)
    def test_positive(self, valid_expression: str) -> None:
        actual = spdx.is_compound_expression(valid_expression)
        self.assertTrue(actual)

    @idata(INVALID_COMPOUND_EXPRESSIONS)
    def test_negative(self, invalid_expression: str) -> None:
        actual = spdx.is_compound_expression(invalid_expression)
        self.assertFalse(actual)
