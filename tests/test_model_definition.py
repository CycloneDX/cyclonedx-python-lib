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

from cyclonedx.model.definition import Definitions, Standard


class TestModelDefinitionRepository(TestCase):

    def test_init(self) -> Definitions:
        s = Standard(name='test-standard')
        dr = Definitions(
            standards=(s, ),
        )
        self.assertIs(s, tuple(dr.standards)[0])
        return dr

    def test_filled(self) -> None:
        dr = self.test_init()
        self.assertIsNotNone(dr.standards)
        self.assertEqual(1, len(dr.standards))
        self.assertTrue(dr)

    def test_empty(self) -> None:
        dr = Definitions()
        self.assertIsNotNone(dr.standards)
        self.assertEqual(0, len(dr.standards))
        self.assertFalse(dr)

    def test_unequal_different_type(self) -> None:
        dr = Definitions()
        self.assertFalse(dr == 'other')

    def test_equal_self(self) -> None:
        dr = Definitions()
        dr.standards.add(Standard(name='my-standard'))
        self.assertTrue(dr == dr)

    def test_unequal(self) -> None:
        dr1 = Definitions()
        dr1.standards.add(Standard(name='my-standard'))
        tr2 = Definitions()
        self.assertFalse(dr1 == tr2)

    def test_equal(self) -> None:
        s = Standard(name='my-standard')
        dr1 = Definitions()
        dr1.standards.add(s)
        tr2 = Definitions()
        tr2.standards.add(s)
        self.assertTrue(dr1 == tr2)
