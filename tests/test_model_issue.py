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

from cyclonedx.exception.model import NoPropertiesProvidedException
from cyclonedx.model import XsUri
from cyclonedx.model.issue import IssueClassification, IssueType, IssueTypeSource
from tests import reorder
from tests._data.models import get_issue_1, get_issue_2


class TestModelIssueType(TestCase):

    def test_same(self) -> None:
        i_1 = get_issue_1()
        i_2 = get_issue_1()
        self.assertNotEqual(id(i_1), id(i_2))
        self.assertEqual(hash(i_1), hash(i_2))
        self.assertTrue(i_1 == i_2)

    def test_not_same(self) -> None:
        i_1 = get_issue_1()
        i_2 = get_issue_2()
        self.assertNotEqual(id(i_1), id(i_2))
        self.assertNotEqual(hash(i_1), hash(i_2))
        self.assertFalse(i_1 == i_2)

    def test_sort(self) -> None:
        source_a = IssueTypeSource(name='a')
        source_b = IssueTypeSource(name='b')

        # expected sort order: (type/classification, id, name, description, source)
        expected_order = [6, 5, 0, 1, 2, 3, 4]
        issues = [
            IssueType(type=IssueClassification.SECURITY, id='a', name='a', description='a', source=source_a),
            IssueType(type=IssueClassification.SECURITY, id='a', name='a', description='a', source=source_b),
            IssueType(type=IssueClassification.SECURITY, id='a', name='a', description='a'),
            IssueType(type=IssueClassification.SECURITY, id='a', name='a'),
            IssueType(type=IssueClassification.SECURITY, id='a'),
            IssueType(type=IssueClassification.DEFECT, id='a', name='a', description='a', source=source_b),
            IssueType(type=IssueClassification.DEFECT, id='a', name='a', description='a', source=source_a),
        ]
        sorted_issues = sorted(issues)
        expected_issues = reorder(issues, expected_order)
        self.assertListEqual(sorted_issues, expected_issues)


class TestModelIssueTypeSource(TestCase):

    def test_no_params(self) -> None:
        with self.assertRaises(NoPropertiesProvidedException):
            IssueTypeSource()

    def test_same(self) -> None:
        its_1 = IssueTypeSource(name='The Source', url=XsUri('https://cyclonedx.org'))
        its_2 = IssueTypeSource(name='The Source', url=XsUri('https://cyclonedx.org'))
        self.assertNotEqual(id(its_1), id(its_2))
        self.assertEqual(hash(its_1), hash(its_2))
        self.assertTrue(its_1 == its_2)

    def test_not_same(self) -> None:
        its_1 = IssueTypeSource(name='The Source', url=XsUri('https://cyclonedx.org'))
        its_2 = IssueTypeSource(name='Not the Source', url=XsUri('https://cyclonedx.org'))
        self.assertNotEqual(id(its_1), id(its_2))
        self.assertNotEqual(hash(its_1), hash(its_2))
        self.assertFalse(its_1 == its_2)

    def test_sort(self) -> None:
        # expected sort order: ([name], [url])
        expected_order = [0, 1, 3, 2, 5, 4]
        sources = [
            IssueTypeSource(name='a', url=XsUri('a')),
            IssueTypeSource(name='a', url=XsUri('b')),
            IssueTypeSource(name='b'),
            IssueTypeSource(name='a'),
            IssueTypeSource(url=XsUri('b')),
            IssueTypeSource(url=XsUri('a')),
        ]
        sorted_sources = sorted(sources)
        expected_sources = reorder(sources, expected_order)
        self.assertListEqual(sorted_sources, expected_sources)
