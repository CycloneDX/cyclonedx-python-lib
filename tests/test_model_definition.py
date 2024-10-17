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

from cyclonedx.model.definition import CreId, InvalidCreIdException


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

    def test_invalid_id(self) -> None:
        with self.assertRaises(TypeError):
            CreId()
        with self.assertRaises(InvalidCreIdException):
            CreId('')
        with self.assertRaises(InvalidCreIdException):
            CreId('some string')
        with self.assertRaises(InvalidCreIdException):
            CreId('123-456')
        with self.assertRaises(InvalidCreIdException):
            CreId('CRE:123-456-789')
        with self.assertRaises(InvalidCreIdException):
            CreId('CRE:abc-def')
        with self.assertRaises(InvalidCreIdException):
            CreId('CRE:123456')
