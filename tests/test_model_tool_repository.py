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


from json import loads as json_loads
from os.path import join
from unittest import TestCase

from sortedcontainers import SortedSet

from cyclonedx.exception.model import MutuallyExclusivePropertiesException
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component
from cyclonedx.model.contact import OrganizationalEntity
from cyclonedx.model.service import Service
from cyclonedx.model.tool import Tool, ToolsRepository, ToolsRepositoryHelper
from cyclonedx.output.json import JsonV1Dot5
from cyclonedx.output.xml import XmlV1Dot5
from tests import OWN_DATA_DIRECTORY
from tests._data.models import get_bom_with_tools_with_component_and_service_migrate


class TestModelToolRepository(TestCase):
    def test_tool_with_component_and_service_load_json(self) -> None:
        expected = get_bom_with_tools_with_component_and_service_migrate()
        test_file = join(OWN_DATA_DIRECTORY, 'json', '1.5',
                         'bom_with_tool_with_component_and_service.json')
        with open(test_file, encoding='UTF-8') as f:
            bom_json = json_loads(f.read())
        bom = Bom.from_json(bom_json)   # type: ignore[attr-defined]
        self.assertTupleEqual(
            tuple(bom.metadata.tools.components),
            tuple(expected.metadata.tools.components), 'components')
        self.assertTupleEqual(
            tuple(bom.metadata.tools.services),
            tuple(expected.metadata.tools.services), 'services')
        self.assertTupleEqual(
            tuple(bom.metadata.tools.tools),
            tuple(expected.metadata.tools.tools), 'tools')

    def test_tool_with_component_and_service_load_xml(self) -> None:
        expected = get_bom_with_tools_with_component_and_service_migrate()
        test_file = join(OWN_DATA_DIRECTORY, 'xml', '1.5',
                         'bom_with_tool_with_component_and_service.xml')
        with open(test_file, encoding='utf-8') as bom_xml:
            bom = Bom.from_xml(bom_xml)  # type: ignore[attr-defined]
        self.assertTupleEqual(
            tuple(bom.metadata.tools.components),
            tuple(expected.metadata.tools.components), 'components')
        self.assertTupleEqual(
            tuple(bom.metadata.tools.services),
            tuple(expected.metadata.tools.services), 'services')
        self.assertTupleEqual(
            tuple(bom.metadata.tools.tools),
            tuple(expected.metadata.tools.tools), 'tools')

    def test_assign_component(self) -> None:
        t = ToolsRepository()
        t.components = SortedSet([Component(name='test-component')])
        s = t.components.pop()
        self.assertEqual('test-component', s.name)

    def test_assign_service(self) -> None:
        t = ToolsRepository()
        t.services = SortedSet([Service(name='test-service')])
        s = t.services.pop()
        self.assertEqual('test-service', s.name)

    def test_invalid_tool_repo_properties(self) -> None:
        with self.assertRaises(MutuallyExclusivePropertiesException):
            ToolsRepository(
                components=[Component(name='test-component')],
                services=[Service(name='test-service')], tools=[Tool()])

    def test_assign_component_with_existing_tool(self) -> None:
        tr = ToolsRepository(tools=[Tool()])
        with self.assertRaises(MutuallyExclusivePropertiesException):
            tr.components = SortedSet([Component(name='test-component')])

    def test_assign_service_with_existing_tool(self) -> None:
        tr = ToolsRepository(tools=[Tool()])
        with self.assertRaises(MutuallyExclusivePropertiesException):
            tr.services = SortedSet([Service(name='test-service')])

    def test_equal_other_objectd(self) -> None:
        tr = ToolsRepository()
        self.assertFalse(tr == 'other')

    def test_equal_object(self) -> None:
        tr = ToolsRepository()
        self.assertTrue(tr == tr)

    def test_assign_tool_with_existing_component(self) -> None:
        tr = ToolsRepository(components=SortedSet([Component(name='test-component')]))
        with self.assertRaises(MutuallyExclusivePropertiesException):
            tr.tools = SortedSet([Tool()])

    def test_assign_tool(self) -> None:
        tr = ToolsRepository()
        tr.tools = SortedSet([Tool(name='test-tool')])
        t = tr.tools.pop()
        self.assertEqual('test-tool', t.name)

    def test_proper_service_provider_conversion(self) -> None:
        o = OrganizationalEntity(name='test-org')
        s = Service(name='test-service', provider=o)

        tools_to_render = ToolsRepositoryHelper.convert_new_to_old(components=[], services=[s])

        t = tools_to_render.pop()  # type: ignore[attr-defined]

        self.assertEqual('test-org', t.vendor)
