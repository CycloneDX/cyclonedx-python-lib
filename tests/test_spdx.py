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
from os.path import dirname, join as path_join
from unittest import TestCase

from ddt import data, ddt, idata, unpack

from cyclonedx.spdx import fixup_id, is_supported_id

with open(path_join(dirname(__file__), '..', 'cyclonedx', 'schema', 'spdx.schema.json')) as spdx_schema:
    SPDX_IDS = json_load(spdx_schema)['enum']


@ddt
class TestSpdx(TestCase):

    @data(
        'something unsupported',
        # somehow case-twisted values
        'MiT',
        'mit',
    )
    def test_not_supported(self, unsupported_value: str) -> None:
        actual = is_supported_id(unsupported_value)
        self.assertFalse(actual)

    @idata(SPDX_IDS)
    def test_is_supported(self, supported_value: str) -> None:
        actual = is_supported_id(supported_value)
        self.assertTrue(actual)

    @idata(chain(
        # original value
        ((v, v) for v in SPDX_IDS),
        # somehow case-twisted values
        ((v.lower(), v) for v in SPDX_IDS),
        ((v.upper(), v) for v in SPDX_IDS)
    ))
    @unpack
    def test_fixup(self, fixable: str, expected_fixed: str) -> None:
        actual = fixup_id(fixable)
        self.assertEqual(expected_fixed, actual)

    @data(
        'something unfixable',
    )
    def test_not_fixup(self, unfixable: str) -> None:
        actual = fixup_id(unfixable)
        self.assertIsNone(actual)
