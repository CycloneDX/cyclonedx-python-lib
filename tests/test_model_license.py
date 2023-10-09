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
from random import shuffle
from unittest import TestCase

from cyclonedx.model.license import DisjunctiveLicense, LicenseExpression
from tests import reorder


class TestModelLicense(TestCase):

    def test_sort_mixed(self) -> None:
        expected_order = [1, 2, 0]
        licenses = [
            DisjunctiveLicense(name='my license'),
            LicenseExpression(value='MIT or Apache-2.0'),
            DisjunctiveLicense(id='MIT'),
        ]
        expected_licenses = reorder(licenses, expected_order)
        shuffle(licenses)
        sorted_licenses = sorted(licenses)
        self.assertListEqual(sorted_licenses, expected_licenses)
