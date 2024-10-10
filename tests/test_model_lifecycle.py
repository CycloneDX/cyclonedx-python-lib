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


from random import shuffle
from unittest import TestCase

from cyclonedx.model.lifecycle import CustomPhase, Phase, PredefinedPhase
from tests import reorder


class TestModelPredefinedPhase(TestCase):
    def test_create(self) -> None:
        lifecycle = PredefinedPhase(phase=Phase.BUILD)
        self.assertIs(Phase.BUILD, lifecycle.phase)

    def test_update(self) -> None:
        lifecycle = PredefinedPhase(phase=Phase.DESIGN)
        lifecycle.phase = Phase.DISCOVERY
        self.assertIs(Phase.DISCOVERY, lifecycle.phase)

    def test_equal(self) -> None:
        a = PredefinedPhase(phase=Phase.BUILD)
        b = PredefinedPhase(phase=Phase.BUILD)
        c = PredefinedPhase(phase=Phase.DESIGN)
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test_sort(self) -> None:
        expected_order = [3, 0, 2, 1]
        lifecycles = [
            CustomPhase(name='foo', description='baz'),
            CustomPhase(name='foo'),
            CustomPhase(name='foo', description='qux'),
            CustomPhase(name='bar'),
        ]
        expected_lifecycles = reorder(lifecycles, expected_order)
        shuffle(lifecycles)
        sorted_lifecycles = sorted(lifecycles)
        self.assertListEqual(sorted_lifecycles, expected_lifecycles)


class TestModelCustomPhase(TestCase):
    def test_create(self) -> None:
        lifecycle = CustomPhase(name='foo')
        self.assertEqual('foo', lifecycle.name)
        self.assertIsNone(lifecycle.description)

        lifecycle = CustomPhase(name='foo2n', description='foo2d')
        self.assertEqual('foo2n', lifecycle.name)
        self.assertEqual('foo2d', lifecycle.description)

    def test_update(self) -> None:
        lifecycle = CustomPhase(name='foo')
        self.assertEqual('foo', lifecycle.name)
        lifecycle.name = 'bar'
        self.assertEqual('bar', lifecycle.name)

    def test_equal(self) -> None:
        a = CustomPhase('foo')
        b = CustomPhase('foo')
        c = CustomPhase('bar')
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(a, 'foo')

    def test_sort(self) -> None:
        expected_order = [3, 0, 2, 1]
        lifecycles = [
            CustomPhase(name='foo', description='baz'),
            CustomPhase(name='foo'),
            CustomPhase(name='foo', description='qux'),
            CustomPhase(name='bar'),
        ]
        expected_lifecycles = reorder(lifecycles, expected_order)
        shuffle(lifecycles)
        sorted_lifecycles = sorted(lifecycles)
        self.assertListEqual(sorted_lifecycles, expected_lifecycles)


class TestModelLifecycle(TestCase):
    def test_sort_mixed(self) -> None:
        expected_order = [3, 0, 2, 1]
        lifecycles = [
            PredefinedPhase(phase=Phase.DESIGN),
            CustomPhase(name='Example2'),
            CustomPhase(name='Example'),
            PredefinedPhase(phase=Phase.BUILD),
        ]
        expected_lifecycles = reorder(lifecycles, expected_order)
        shuffle(lifecycles)
        sorted_lifecycles = sorted(lifecycles)
        self.assertListEqual(sorted_lifecycles, expected_lifecycles)
