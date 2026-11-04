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

from packageurl import PackageURL

from cyclonedx._internal.compare import ComparablePackageURL


class TestComparablePackageURL(TestCase):

    def test_differs_by_name(self) -> None:
        """
        regression for https://github.com/CycloneDX/cyclonedx-python-lib/issues/1021

        name was missing from the comparison tuple, so two purls that differ
        only by name compared equal
        """
        purl1 = ComparablePackageURL(PackageURL(type='pypi', name='foo', version='1.0.0'))
        purl2 = ComparablePackageURL(PackageURL(type='pypi', name='bar', version='1.0.0'))
        self.assertNotEqual(purl1, purl2)
        self.assertGreater(purl1, purl2)
        self.assertLess(purl2, purl1)

    def test_equal_same_purl(self) -> None:
        purl1 = ComparablePackageURL(PackageURL(type='pypi', name='foo', version='1.0.0'))
        purl2 = ComparablePackageURL(PackageURL(type='pypi', name='foo', version='1.0.0'))
        self.assertEqual(purl1, purl2)
