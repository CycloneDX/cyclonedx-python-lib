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


from datetime import datetime, timezone
from unittest import TestCase

from cyclonedx.exception.model import MutuallyExclusivePropertiesException, NoPropertiesProvidedException
from cyclonedx.model.bom_ref import BomRef
from cyclonedx.model.citation import Citation

_TS = datetime(2025, 10, 1, 12, 0, 0, tzinfo=timezone.utc)


class TestModelCitation(TestCase):

    def test_create_with_pointers(self) -> None:
        c = Citation(timestamp=_TS, pointers=['/b', '/a'], attributed_to='author', bom_ref='c1', note='n')
        self.assertListEqual(['/a', '/b'], list(c.pointers))
        self.assertEqual(0, len(c.expressions))
        self.assertEqual(_TS, c.timestamp)
        self.assertIsInstance(c.attributed_to, BomRef)
        self.assertEqual('author', c.attributed_to.value)
        self.assertIsNone(c.process)
        self.assertEqual('c1', c.bom_ref.value)
        self.assertEqual('n', c.note)

    def test_create_with_expressions_and_process(self) -> None:
        c = Citation(timestamp=_TS, expressions=['$.a'], process=BomRef('p1'))
        self.assertListEqual(['$.a'], list(c.expressions))
        self.assertIsNone(c.attributed_to)
        self.assertEqual('p1', c.process.value)
        self.assertIsNone(c.bom_ref.value)

    def test_requires_pointers_or_expressions(self) -> None:
        with self.assertRaises(NoPropertiesProvidedException):
            Citation(timestamp=_TS, attributed_to='a')

    def test_pointers_and_expressions_are_exclusive(self) -> None:
        with self.assertRaises(MutuallyExclusivePropertiesException):
            Citation(timestamp=_TS, pointers=['/a'], expressions=['$.a'], attributed_to='a')

    def test_requires_attributed_to_or_process(self) -> None:
        with self.assertRaises(NoPropertiesProvidedException):
            Citation(timestamp=_TS, pointers=['/a'])

    def test_equal(self) -> None:
        c1 = Citation(timestamp=_TS, pointers=['/a'], attributed_to='a', note='x')
        c2 = Citation(timestamp=_TS, pointers=['/a'], attributed_to='a', note='x')
        self.assertEqual(c1, c2)
        self.assertEqual(hash(c1), hash(c2))

    def test_not_equal(self) -> None:
        c1 = Citation(timestamp=_TS, pointers=['/a'], attributed_to='a')
        c2 = Citation(timestamp=_TS, pointers=['/a'], attributed_to='b')
        self.assertNotEqual(c1, c2)
        self.assertNotEqual(c1, 'foo')

    def test_sort(self) -> None:
        later = datetime(2025, 10, 2, tzinfo=timezone.utc)
        expected = [
            Citation(timestamp=_TS, pointers=['/a'], attributed_to='a'),
            Citation(timestamp=_TS, pointers=['/b'], attributed_to='a'),
            Citation(timestamp=later, expressions=['$.a'], process='p'),
        ]
        self.assertListEqual(expected, sorted(reversed(expected)))
