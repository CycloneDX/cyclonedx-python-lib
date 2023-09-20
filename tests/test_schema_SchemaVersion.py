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

from unittest import TestCase

from ddt import ddt, idata, data, unpack

from cyclonedx.schema import SchemaVersion

from itertools import chain

SORTED_SCHEMA_VERSIONS = (SchemaVersion.V1_4,
                          SchemaVersion.V1_3,
                          SchemaVersion.V1_2,
                          SchemaVersion.V1_1,
                          SchemaVersion.V1_0)

td_gt = tuple((a, b) for i, a in enumerate(SORTED_SCHEMA_VERSIONS) for b in SORTED_SCHEMA_VERSIONS[i + 1:])
td_ge = tuple((a, b) for i, a in enumerate(SORTED_SCHEMA_VERSIONS) for b in SORTED_SCHEMA_VERSIONS[i:])
td_eq = tuple((a, b) for i, a in enumerate(SORTED_SCHEMA_VERSIONS) for b in SORTED_SCHEMA_VERSIONS[:])
td_le = tuple((a, b) for i, a in enumerate(SORTED_SCHEMA_VERSIONS) for b in SORTED_SCHEMA_VERSIONS[:i + 1])
td_lt = tuple((a, b) for i, a in enumerate(SORTED_SCHEMA_VERSIONS) for b in SORTED_SCHEMA_VERSIONS[:i])


@ddt
class TestSchemaVersion(TestCase):

    @idata(v for v in SchemaVersion)
    def test_version_roundtrip(self, v: SchemaVersion):
        v2 = SchemaVersion.from_version(v.to_version())
        self.assertIs(v, v2)

    @data(td_gt)
    @unpack
    def test_gt(self, a: SchemaVersion, b: SchemaVersion) -> None:
        self.assertGreater(a, b)

    @data(td_ge)
    @unpack
    def test_ge(self, a: SchemaVersion, b: SchemaVersion) -> None:
        self.assertGreaterEqual(a, b)

    @data(td_eq)
    @unpack
    def test_eq(self, a: SchemaVersion, b: SchemaVersion) -> None:
        self.assertEqual(a, b)

    @data(td_lt)
    @unpack
    def test_lt(self, a: SchemaVersion, b: SchemaVersion) -> None:
        self.assertLess(a, b)

    @data(td_le)
    @unpack
    def test_le(self, a: SchemaVersion, b: SchemaVersion) -> None:
        self.assertLessEqual(a, b)
