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

import os
from unittest import TestCase

from cyclonedx.model.bom import Bom, ThisTool, Tool
from cyclonedx.model.component import Component
from cyclonedx.parser.requirements import RequirementsFileParser


class TestBom(TestCase):

    def test_bom_simple(self) -> None:
        parser = RequirementsFileParser(
            requirements_file=os.path.join(os.path.dirname(__file__), 'fixtures/requirements-simple.txt')
        )
        bom = Bom.from_parser(parser=parser)

        self.assertEqual(bom.component_count(), 1)
        self.assertTrue(bom.has_component(
            Component(name='setuptools', version='50.3.2')
        ))

    def test_bom_metadata_tool_this_tool(self) -> None:
        self.assertEqual(ThisTool.get_vendor(), 'CycloneDX')
        self.assertEqual(ThisTool.get_name(), 'cyclonedx-python-lib')
        self.assertNotEqual(ThisTool.get_version(), 'UNKNOWN')

    def test_bom_metadata_tool_multiple_tools(self) -> None:
        bom = Bom()
        self.assertEqual(len(bom.get_metadata().get_tools()), 1)

        bom.get_metadata().add_tool(Tool(
            vendor='TestVendor', name='TestTool', version='0.0.0'
        ))
        self.assertEqual(len(bom.get_metadata().get_tools()), 2)
