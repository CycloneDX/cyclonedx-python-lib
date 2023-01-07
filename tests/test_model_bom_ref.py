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

from cyclonedx.model.bom_ref import BomRef

from .data import reorder


class TestBomRef(TestCase):

    def test_sort(self) -> None:
        # expected sort order: (value)
        expected_order = [0, 1, 2, 4, 3]
        refs = [
            BomRef(value='a'),
            BomRef(value='b'),
            BomRef(value='c'),
            BomRef(value='f'),
            BomRef(value='d'),
        ]
        sorted_refs = sorted(refs)
        expected_refs = reorder(refs, expected_order)
        self.assertListEqual(sorted_refs, expected_refs)
