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
# Copyright (C) Siemens 2026. All Rights Reserved.


from unittest import TestCase

from cyclonedx.model import XsUri
from cyclonedx.model.bom_ref import BomRef
from cyclonedx.model.composition import AggregateType, Composition


class TestModelComposition(TestCase):
    def test_create_default_aggregate(self) -> None:
        composition = Composition()
        self.assertIs(AggregateType.NOT_SPECIFIED, composition.aggregate)
        self.assertIsNone(composition.bom_ref)
        self.assertEqual(0, len(composition.assemblies))
        self.assertEqual(0, len(composition.dependencies))
        self.assertEqual(0, len(composition.vulnerabilities))

    def test_create_full(self) -> None:
        composition = Composition(
            aggregate=AggregateType.INCOMPLETE,
            assemblies=[BomRef('assembly-a'), XsUri('urn:cdx:xyz/1#ref-b')],
            dependencies=[BomRef('dep-a')],
            vulnerabilities=[BomRef('CVE-1')],
            bom_ref='comp-1',
        )
        self.assertIs(AggregateType.INCOMPLETE, composition.aggregate)
        self.assertEqual('comp-1', str(composition.bom_ref))
        self.assertEqual(2, len(composition.assemblies))
        self.assertEqual(1, len(composition.dependencies))
        self.assertEqual(1, len(composition.vulnerabilities))

    def test_update_aggregate(self) -> None:
        composition = Composition(aggregate=AggregateType.COMPLETE)
        composition.aggregate = AggregateType.UNKNOWN
        self.assertIs(AggregateType.UNKNOWN, composition.aggregate)

    def test_equal(self) -> None:
        a = Composition(aggregate=AggregateType.COMPLETE, dependencies=[BomRef('x')])
        b = Composition(aggregate=AggregateType.COMPLETE, dependencies=[BomRef('x')])
        c = Composition(aggregate=AggregateType.INCOMPLETE, dependencies=[BomRef('x')])
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(a, 'not-a-composition')

    def test_equal_ignores_bom_ref(self) -> None:
        # bom-ref is an identity-only attribute; it does not affect equality
        a = Composition(aggregate=AggregateType.COMPLETE, bom_ref='one')
        b = Composition(aggregate=AggregateType.COMPLETE, bom_ref='two')
        self.assertEqual(a, b)

    def test_hashable(self) -> None:
        composition = Composition(aggregate=AggregateType.COMPLETE)
        self.assertIsInstance(hash(composition), int)

    def test_sort(self) -> None:
        compositions = [
            Composition(aggregate=AggregateType.INCOMPLETE),
            Composition(aggregate=AggregateType.COMPLETE),
        ]
        sorted_compositions = sorted(compositions)
        self.assertIs(AggregateType.COMPLETE, sorted_compositions[0].aggregate)
        self.assertIs(AggregateType.INCOMPLETE, sorted_compositions[1].aggregate)

    def test_assemblies_distinguishes_ref_and_bom_link(self) -> None:
        composition = Composition(
            assemblies=[BomRef('plain-ref'), XsUri('urn:cdx:xyz/1#ref-b')],
        )
        kinds = {type(a) for a in composition.assemblies}
        self.assertIn(BomRef, kinds)
        self.assertIn(XsUri, kinds)
