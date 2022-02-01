# encoding: utf-8

# This file is part of CycloneDX Python Lib
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
from cyclonedx.model.issue import IssueTypeSource

from data import get_issue_1, get_issue_2


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


class TestModelIssueTypeSource(TestCase):

    def test_no_params(self) -> None:
        with self.assertRaises(NoPropertiesProvidedException):
            IssueTypeSource()

    def test_same(self) -> None:
        its_1 = IssueTypeSource(name="The Source", url=XsUri('https://cyclonedx.org'))
        its_2 = IssueTypeSource(name="The Source", url=XsUri('https://cyclonedx.org'))
        self.assertNotEqual(id(its_1), id(its_2))
        self.assertEqual(hash(its_1), hash(its_2))
        self.assertTrue(its_1 == its_2)

    def test_not_same(self) -> None:
        its_1 = IssueTypeSource(name="The Source", url=XsUri('https://cyclonedx.org'))
        its_2 = IssueTypeSource(name="Not the Source", url=XsUri('https://cyclonedx.org'))
        self.assertNotEqual(id(its_1), id(its_2))
        self.assertNotEqual(hash(its_1), hash(its_2))
        self.assertFalse(its_1 == its_2)
