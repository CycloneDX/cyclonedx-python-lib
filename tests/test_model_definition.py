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

from ddt import ddt, named_data

from cyclonedx.exception.model import InvalidCreIdException
from cyclonedx.model.definition import CreId, Definitions, Level, Requirement, Standard


class TestModelDefinitions(TestCase):

    def test_init(self) -> Definitions:
        s = Standard(name='test-standard')
        dr = Definitions(
            standards=(s, ),
        )
        self.assertEqual(1, len(dr.standards))
        self.assertIs(s, tuple(dr.standards)[0])
        return dr

    def test_filled(self) -> None:
        dr = self.test_init()
        self.assertIsNotNone(dr.standards)
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


@ddt
class TestModelCreId(TestCase):

    def test_different(self) -> None:
        id1 = CreId('CRE:123-456')
        id2 = CreId('CRE:987-654')
        self.assertNotEqual(id(id1), id(id2))
        self.assertNotEqual(hash(id1), hash(id2))
        self.assertFalse(id1 == id2)

    def test_same(self) -> None:
        id1 = CreId('CRE:123-456')
        id2 = CreId('CRE:123-456')
        self.assertNotEqual(id(id1), id(id2))
        self.assertEqual(hash(id1), hash(id2))
        self.assertTrue(id1 == id2)

    def test_invalid_no_id(self) -> None:
        with self.assertRaises(TypeError):
            CreId()

    @named_data(
        ['empty', ''],
        ['arbitrary string', 'some string'],
        ['missing prefix', '123-456'],
        ['additional part', 'CRE:123-456-789'],
        ['no numbers', 'CRE:abc-def'],
        ['no delimiter', 'CRE:123456'],
    )
    def test_invalid_id(self, wrong_id: str) -> None:
        with self.assertRaises(InvalidCreIdException):
            CreId(wrong_id)


class TestModelRequirements(TestCase):

    def test_bom_ref_is_set_from_value(self) -> None:
        r = Requirement(bom_ref='123-456')
        self.assertIsNotNone(r.bom_ref)
        self.assertEqual('123-456', r.bom_ref.value)

    def test_bom_ref_is_set_if_none_given(self) -> None:
        r = Requirement()
        self.assertIsNotNone(r.bom_ref)


class TestModelLevel(TestCase):

    def test_bom_ref_is_set_from_value(self) -> None:
        r = Level(bom_ref='123-456')
        self.assertIsNotNone(r.bom_ref)
        self.assertEqual('123-456', r.bom_ref.value)

    def test_bom_ref_is_set_if_none_given(self) -> None:
        r = Level()
        self.assertIsNotNone(r.bom_ref)


class TestModelStandard(TestCase):

    def test_bom_ref_is_set_from_value(self) -> None:
        r = Standard(bom_ref='123-456')
        self.assertIsNotNone(r.bom_ref)
        self.assertEqual('123-456', r.bom_ref.value)

    def test_bom_ref_is_set_if_none_given(self) -> None:
        r = Standard()
        self.assertIsNotNone(r.bom_ref)
