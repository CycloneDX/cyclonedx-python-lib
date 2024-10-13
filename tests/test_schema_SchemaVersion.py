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

from unittest import TestCase

from ddt import ddt, idata, unpack

from cyclonedx.schema import SchemaVersion

SORTED_SV = (
    SchemaVersion.V1_6,
    SchemaVersion.V1_5,
    SchemaVersion.V1_4,
    SchemaVersion.V1_3,
    SchemaVersion.V1_2,
    SchemaVersion.V1_1,
    SchemaVersion.V1_0
)

# do not use any value-comparisons or implicit hash-functions here !
# just work with the position in tuple SORTED_SCHEMA_VERSIONS
td_gt = tuple((a, b) for i, a in enumerate(SORTED_SV) for b in SORTED_SV[i + 1:])
td_ge = tuple((a, b) for i, a in enumerate(SORTED_SV) for b in SORTED_SV[i:])
td_eq = tuple((v, v) for v in SORTED_SV)
td_le = tuple((b, a) for a, b in td_ge)
td_lt = tuple((b, a) for a, b in td_gt)
td_ne = tuple((a, b) for i, a in enumerate(SORTED_SV) for j, b in enumerate(SORTED_SV) if i != j)


@ddt
class TestSchemaVersion(TestCase):

    @idata(v for v in SchemaVersion)
    def test_version_roundtrip(self, v: SchemaVersion) -> None:
        v2 = SchemaVersion.from_version(v.to_version())
        self.assertIs(v, v2)

    @idata(td_ne)
    @unpack
    def test_ne(self, a: SchemaVersion, b: SchemaVersion) -> None:
        self.assertNotEqual(a, b)

    @idata(td_gt)
    @unpack
    def test_gt(self, a: SchemaVersion, b: SchemaVersion) -> None:
        self.assertGreater(a, b)

    @idata(td_ge)
    @unpack
    def test_ge(self, a: SchemaVersion, b: SchemaVersion) -> None:
        self.assertGreaterEqual(a, b)

    @idata(td_eq)
    @unpack
    def test_eq(self, a: SchemaVersion, b: SchemaVersion) -> None:
        self.assertEqual(a, b)

    @idata(td_lt)
    @unpack
    def test_lt(self, a: SchemaVersion, b: SchemaVersion) -> None:
        self.assertLess(a, b)

    @idata(td_le)
    @unpack
    def test_le(self, a: SchemaVersion, b: SchemaVersion) -> None:
        self.assertLessEqual(a, b)
