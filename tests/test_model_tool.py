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

from cyclonedx.model.tool import Tool
from tests import reorder


class TestModelTool(TestCase):

    def test_sort(self) -> None:
        # expected sort order: (vendor, name, version)
        expected_order = [0, 1, 2, 3, 4, 5, 6]
        tools = [
            Tool(vendor='a', name='a', version='1.0.0'),
            Tool(vendor='a', name='a', version='2.0.0'),
            Tool(vendor='a', name='b', version='1.0.0'),
            Tool(vendor='a', name='b'),
            Tool(vendor='b', name='a'),
            Tool(vendor='b', name='b', version='1.0.0'),
            Tool(name='b'),
        ]
        sorted_tools = sorted(tools)
        expected_tools = reorder(tools, expected_order)
        self.assertListEqual(sorted_tools, expected_tools)

    def test_non_equal_tool_and_invalid(self) -> None:
        t = Tool(vendor='VendorA')
        self.assertFalse(t == 'INVALID')

    def test_invalid_tool_compare(self) -> None:
        t = Tool(vendor='VendorA')
        with self.assertRaises(TypeError):
            r = t < 'INVALID'  # pylint: disable=unused-variable # noqa: disable=E841

    def test_tool_repr(self) -> None:
        t = Tool(name='test-tool', version='1.2.3', vendor='test-vendor')
        self.assertEqual(repr(t), '<Tool name=test-tool, version=1.2.3, vendor=test-vendor>')

    def test_tool_equals(self) -> None:
        t = Tool()
        self.assertEqual(t, t)
