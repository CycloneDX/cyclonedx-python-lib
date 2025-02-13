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
from json import load as json_load
from unittest import TestCase

from ddt import ddt, idata, unpack

from cyclonedx import spdx
from cyclonedx.schema._res import SPDX_JSON

# rework access
with open(SPDX_JSON) as spdx_schema:
    KNOWN_SPDX_IDS = set(json_load(spdx_schema)['enum'])

# for valid test data see the spec: https://spdx.github.io/spdx-spec/v3.0.1/annexes/spdx-license-expressions/
VALID_EXPRESSIONS = {
    # region Simple license expressions
    'CDDL-1.0',
    # region not supported yet #110 - https://github.com/aboutcode-org/license-expression/issues/110
    # 'CDDL-1.0+',
    # endregion region not supported yet #110
    # region not supported yet #109 - https://github.com/aboutcode-org/license-expression/issues/109
    # 'LicenseRef-23',
    # 'LicenseRef-MIT-Style-1',
    # 'DocumentRef-spdx-tool-1.2:LicenseRef-MIT-Style-2',
    # endregion region not supported yet #109
    # endregion Simple license expressions
    # region Composite license expressions
    'LGPL-2.1-only OR MIT',
    'MIT or LGPL-2.1-only',
    '(MIT OR LGPL-2.1-only)',
    'LGPL-2.1-only OR MIT OR BSD-3-Clause',
    'LGPL-2.1-only AND MIT',
    'MIT AND LGPL-2.1-only',
    'MIT and LGPL-2.1-only',
    '(MIT AND LGPL-2.1-only)',
    'LGPL-2.1-only AND MIT AND BSD-2-Clause',
    'GPL-2.0-or-later WITH Bison-exception-2.2',
    'LGPL-2.1-only OR BSD-3-Clause AND MIT',
    'MIT AND (LGPL-2.1-or-later OR BSD-3-Clause)',
    # endregion Composite license expressions
    # region examples from CDX spec
    'Apache-2.0 AND (MIT OR GPL-2.0-only)',
    'GPL-3.0-only WITH Classpath-exception-2.0',
    # endregion examples from CDX spec
}

INVALID_EXPRESSIONS = {
    'MIT AND Apache-2.0 OR something-unknown'
    'something invalid',
    '(c) John Doe',
    'Apache License, Version 2.0',
}

UNKNOWN_SPDX_IDS = {
    '',
    'something unsupported', 'something unfixable',
    'Apache 2.0',
    'LicenseRef-custom-identifier',
    *(VALID_EXPRESSIONS - KNOWN_SPDX_IDS),
    *INVALID_EXPRESSIONS,
}


@ddt
class TestSpdxIsSupported(TestCase):

    @idata(KNOWN_SPDX_IDS)
    def test_positive(self, supported_value: str) -> None:
        actual = spdx.is_supported_id(supported_value)
        self.assertTrue(actual)

    @idata(chain(UNKNOWN_SPDX_IDS, (
        # region somehow case-twisted values
        'MiT', 'mit',
        # endregion somehow case-twisted values
    )))
    def test_negative(self, unsupported_value: str) -> None:
        actual = spdx.is_supported_id(unsupported_value)
        self.assertFalse(actual)


@ddt
class TestSpdxFixup(TestCase):

    @idata(chain(
        # original value
        ((v, v) for v in KNOWN_SPDX_IDS),
        # region somehow case-twisted values
        ((v.lower(), v) for v in KNOWN_SPDX_IDS),
        ((v.upper(), v) for v in KNOWN_SPDX_IDS)
        # endregion somehow case-twisted values
    ))
    @unpack
    def test_positive(self, fixable: str, expected_fixed: str) -> None:
        actual = spdx.fixup_id(fixable)
        self.assertEqual(expected_fixed, actual)

    @idata(UNKNOWN_SPDX_IDS)
    def test_negative(self, unfixable: str) -> None:
        actual = spdx.fixup_id(unfixable)
        self.assertIsNone(actual)


@ddt
class TestSpdxIsExpression(TestCase):

    @idata(VALID_EXPRESSIONS)
    def test_positive(self, valid_expression: str) -> None:
        actual = spdx.is_expression(valid_expression)
        self.assertTrue(actual)

    @idata(INVALID_EXPRESSIONS)
    def test_negative(self, invalid_expression: str) -> None:
        actual = spdx.is_expression(invalid_expression)
        self.assertFalse(actual)
