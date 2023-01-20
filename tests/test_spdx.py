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

from itertools import chain
from json import load as json_load
from os.path import join as path_join
from unittest import TestCase

from ddt import data, ddt, idata, unpack

from cyclonedx import spdx

from . import CDX_SCHEMA_DIRECTORY

with open(path_join(CDX_SCHEMA_DIRECTORY, 'spdx.schema.json')) as spdx_schema:
    KNOWN_SPDX_IDS = json_load(spdx_schema)['enum']

VALID_COMPOUND_EXPRESSIONS = {
    # for valid test data see the spec: https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/
    '(MIT WITH Apache-2.0)',
    '(BSD-2-Clause OR Apache-2.0)',
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
        self.assertEqual(expected_fixed, actual)

    @data(
        'something unfixable',
    )
    def test_negative(self, unfixable: str) -> None:
        actual = spdx.fixup_id(unfixable)
        self.assertIsNone(actual)


@ddt
class TestSpdxIsCompoundExpression(TestCase):

    @idata(VALID_COMPOUND_EXPRESSIONS)
    def test_positive(self, valid_expression: str) -> None:
        actual = spdx.is_compound_expression(valid_expression)
        self.assertTrue(actual)

    @data(
        'something invalid',
        '(c) John Doe'
    )
    def test_negative(self, invalid_expression: str) -> None:
        actual = spdx.is_compound_expression(invalid_expression)
        self.assertFalse(actual)
