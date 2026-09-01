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

from cyclonedx.model.bom_ref import BomRef
from cyclonedx.model.dependency import Dependency
from tests import reorder


class TestDependency(TestCase):

    def test_sort(self) -> None:
        # expected sort order: (value)
        expected_order = [3, 2, 0, 1]
        deps = [
            Dependency(ref=BomRef(value='be2c6502-7e9a-47db-9a66-e34f729810a3'), dependencies=[
                Dependency(ref=BomRef(value='0b049d09-64c0-4490-a0f5-c84d9aacf857')),
                Dependency(ref=BomRef(value='17e3b199-dc0b-42ef-bfdd-1fa81a1e3eda'))
            ]),
            Dependency(ref=BomRef(value='cd3e9c95-9d41-49e7-9924-8cf0465ae789')),
            Dependency(ref=BomRef(value='17e3b199-dc0b-42ef-bfdd-1fa81a1e3eda')),
            Dependency(ref=BomRef(value='0b049d09-64c0-4490-a0f5-c84d9aacf857'), dependencies=[
                Dependency(ref=BomRef(value='cd3e9c95-9d41-49e7-9924-8cf0465ae789'))
            ])
        ]
        sorted_deps = sorted(deps)
        expected_deps = reorder(deps, expected_order)
        self.assertEqual(sorted_deps, expected_deps)

    def test_provides_default_empty(self) -> None:
        dep = Dependency(ref=BomRef(value='a'))
        self.assertEqual(len(dep.provides), 0)
        self.assertEqual(dep.provides_as_bom_refs(), set())

    def test_provides_set_and_retrieved(self) -> None:
        ref_b = BomRef(value='B')
        ref_c = BomRef(value='C')
        dep = Dependency(ref=ref_b, provides=[Dependency(ref=ref_c)])
        self.assertEqual(len(dep.provides), 1)
        self.assertEqual(dep.provides_as_bom_refs(), {ref_c})

    def test_provides_included_in_hash_and_equality(self) -> None:
        ref_b = BomRef(value='B')
        ref_c = BomRef(value='C')
        dep_with = Dependency(ref=ref_b, provides=[Dependency(ref=ref_c)])
        dep_without = Dependency(ref=ref_b)
        self.assertNotEqual(dep_with, dep_without)
        self.assertNotEqual(hash(dep_with), hash(dep_without))

    def test_sort_with_provides(self) -> None:
        # Deps with different provides should sort deterministically
        ref_a = BomRef(value='0b049d09-64c0-4490-a0f5-c84d9aacf857')
        ref_b = BomRef(value='be2c6502-7e9a-47db-9a66-e34f729810a3')
        dep_a = Dependency(ref=ref_a, provides=[Dependency(ref=ref_b)])
        dep_b = Dependency(ref=ref_b)
        sorted_result = sorted([dep_b, dep_a])
        self.assertEqual(sorted_result[0].ref, ref_a)
        self.assertEqual(sorted_result[1].ref, ref_b)
