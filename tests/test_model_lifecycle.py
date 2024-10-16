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

from cyclonedx.model.lifecycle import LifecyclePhase, NamedLifecycle, PredefinedLifecycle
from tests import reorder


class TestModelPredefinedLifecycle(TestCase):
    def test_create(self) -> None:
        lifecycle = PredefinedLifecycle(phase=LifecyclePhase.BUILD)
        self.assertIs(LifecyclePhase.BUILD, lifecycle.phase)

    def test_update(self) -> None:
        lifecycle = PredefinedLifecycle(phase=LifecyclePhase.DESIGN)
        lifecycle.phase = LifecyclePhase.DISCOVERY
        self.assertIs(LifecyclePhase.DISCOVERY, lifecycle.phase)

    def test_equal(self) -> None:
        a = PredefinedLifecycle(phase=LifecyclePhase.BUILD)
        b = PredefinedLifecycle(phase=LifecyclePhase.BUILD)
        c = PredefinedLifecycle(phase=LifecyclePhase.DESIGN)
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test_sort(self) -> None:
        expected_order = [3, 0, 2, 1]
        lifecycles = [
            NamedLifecycle(name='foo', description='baz'),
            NamedLifecycle(name='foo'),
            NamedLifecycle(name='foo', description='qux'),
            NamedLifecycle(name='bar'),
        ]
        expected_lifecycles = reorder(lifecycles, expected_order)
        shuffle(lifecycles)
        sorted_lifecycles = sorted(lifecycles)
        self.assertListEqual(sorted_lifecycles, expected_lifecycles)


class TestModelNamedLifecycle(TestCase):
    def test_create(self) -> None:
        lifecycle = NamedLifecycle(name='foo')
        self.assertEqual('foo', lifecycle.name)
        self.assertIsNone(lifecycle.description)

        lifecycle = NamedLifecycle(name='foo2n', description='foo2d')
        self.assertEqual('foo2n', lifecycle.name)
        self.assertEqual('foo2d', lifecycle.description)

    def test_update(self) -> None:
        lifecycle = NamedLifecycle(name='foo')
        self.assertEqual('foo', lifecycle.name)
        lifecycle.name = 'bar'
        self.assertEqual('bar', lifecycle.name)

    def test_equal(self) -> None:
        a = NamedLifecycle('foo')
        b = NamedLifecycle('foo')
        c = NamedLifecycle('bar')
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(a, 'foo')

    def test_sort(self) -> None:
        expected_order = [3, 0, 2, 1]
        lifecycles = [
            NamedLifecycle(name='foo', description='baz'),
            NamedLifecycle(name='foo'),
            NamedLifecycle(name='foo', description='qux'),
            NamedLifecycle(name='bar'),
        ]
        expected_lifecycles = reorder(lifecycles, expected_order)
        shuffle(lifecycles)
        sorted_lifecycles = sorted(lifecycles)
        self.assertListEqual(sorted_lifecycles, expected_lifecycles)


class TestModelLifecycle(TestCase):
    def test_sort_mixed(self) -> None:
        expected_order = [3, 0, 2, 1]
        lifecycles = [
            PredefinedLifecycle(phase=LifecyclePhase.DESIGN),
            NamedLifecycle(name='Example2'),
            NamedLifecycle(name='Example'),
            PredefinedLifecycle(phase=LifecyclePhase.BUILD),
        ]
        expected_lifecycles = reorder(lifecycles, expected_order)
        shuffle(lifecycles)
        sorted_lifecycles = sorted(lifecycles)
        self.assertListEqual(sorted_lifecycles, expected_lifecycles)
