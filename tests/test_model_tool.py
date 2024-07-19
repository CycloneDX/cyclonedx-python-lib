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
from tests import OWN_DATA_DIRECTORY, reorder
from tests._data.models import get_bom_with_tools_with_component_and_service


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

    def test_tool_with_component_and_service_load_json(self) -> None:
        test_file = join(OWN_DATA_DIRECTORY, 'json', '1.5',
                         'bom_with_tool_with_component_and_service.json')
        with open(test_file, encoding='UTF-8') as f:
            bom_json = json_loads(f.read())
        bom = Bom.from_json(bom_json)   # type: ignore[attr-defined]
        good_bom = get_bom_with_tools_with_component_and_service()
        self.assertTrue(bom == good_bom)

    def test_tool_with_component_and_service_render_json(self) -> None:
        bom = get_bom_with_tools_with_component_and_service()
        test_file = join(OWN_DATA_DIRECTORY, 'json', '1.5',
                         'bom_with_tool_with_component_and_service.json')
        with open(test_file, encoding='utf-8') as f:
            self.assertEqual(JsonV1Dot5(bom).output_as_string(indent=2), f.read())

    def test_tool_with_component_and_service_load_xml(self) -> None:
        test_file = join(OWN_DATA_DIRECTORY, 'xml', '1.5',
                         'bom_with_tool_with_component_and_service.xml')
        with open(test_file, encoding='utf-8') as s:
            bom = Bom.from_xml(s)  # type: ignore[attr-defined]
        self.assertEqual(bom.metadata.tools.components[0].type, 'application')
        self.assertEqual(bom.metadata.tools.components[0].name, 'test-component')
        self.assertEqual(bom.metadata.tools.services[0].name, 'test-service')

    def test_tool_with_componet_and_service_render_xml(self) -> None:
        bom = get_bom_with_tools_with_component_and_service()
        test_file = join(OWN_DATA_DIRECTORY, 'xml', '1.5',
                         'bom_with_tool_with_component_and_service.xml')
        with open(test_file, encoding='UTF-8') as f:
            self.assertEqual(XmlV1Dot5(bom).output_as_string(indent=2), f.read())

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

    def test_invalid_tool_repo_properties(self) -> None:
        with self.assertRaises(MutuallyExclusivePropertiesException):
            tr = ToolsRepository(components=[Component(name='test-component')],  # pylint: disable=unused-variable # noqa: disable=E841
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

    def test_tool_equals(self) -> None:
        t = Tool()
        self.assertEqual(t, t)
