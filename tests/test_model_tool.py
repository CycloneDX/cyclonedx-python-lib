import io
from json import loads as json_loads
from unittest import TestCase

from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component, ComponentType
from cyclonedx.model.service import Service
from cyclonedx.model.tool import Tool
from cyclonedx.output.json import JsonV1Dot5
from cyclonedx.output.xml import XmlV1Dot5
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

    def test_tool_with_component_and_service_load_json(self) -> None:
        bom_json = """
            {
                "$schema": "http://cyclonedx.org/schema/bom-1.5.schema.json",
                "bomFormat": "CycloneDX",
                "specVersion": "1.5",
                "serialNumber": "urn:uuid:60bd7113-edac-4277-a518-88d84aef2399",
                "version": 1337,
                "metadata": {
                    "tools": {
                        "components": [
                            {
                                "type": "application",
                                "author": "anchore",
                                "name": "syft",
                                "version": "1.4.1"
                            }
                        ],
                        "services": [
                            {
                                "name": "testing-service"
                            }
                        ]
                    },
                    "component": {
                        "type": "file",
                        "name": "Testing tools with components and services"
                    }
                }
            }
        """
        bom = Bom.from_json(json_loads(bom_json))   # type: ignore[attr-defined]
        self.assertEqual(bom.metadata.tools.components[0].type, 'application')
        self.assertEqual(bom.metadata.tools.components[0].name, 'syft')
        self.assertEqual(bom.metadata.tools.services[0].name, 'testing-service')

    def test_tool_with_component_and_service_render_json(self) -> None:
        bom = Bom()
        bom.metadata.tools.components.add(Component(type=ComponentType.APPLICATION, author='adobe',
                                                    name='test-component', version='1.2.3'))
        bom.metadata.tools.services.add(Service(name='test-service'))
        out = json_loads(JsonV1Dot5(bom).output_as_string())
        self.assertEqual(out['metadata']['tools']['components'][0]['name'], 'test-component')
        self.assertEqual(out['metadata']['tools']['services'][0]['name'], 'test-service')

    def test_tool_with_component_and_service_load_xml(self) -> None:
        bom_xml = io.StringIO("""<?xml version="1.0" ?>
                    <bom xmlns="http://cyclonedx.org/schema/bom/1.5" serialNumber="urn:uuid:f9dbe3d0-53ee-485d-96ae-1d4dce7deea2" version="1">
                        <metadata>
                            <timestamp>2024-06-20T22:49:51.530453+00:00</timestamp>
                            <tools>
                                <components>
                                    <component type="application" bom-ref="None">
                                    <author>adobe</author>
                                    <name>test-component</name>
                                    <version>1.2.3</version>
                                    </component>
                                </components>
                                <services>
                                    <service bom-ref="None">
                                    <name>test-service</name>
                                    </service>
                                </services>
                            </tools>
                        </metadata>
                    </bom>
        """)  # noqa: E501
        bom = Bom.from_xml(bom_xml)   # type: ignore[attr-defined]
        self.assertEqual(bom.metadata.tools.components[0].type, 'application')
        self.assertEqual(bom.metadata.tools.components[0].name, 'test-component')
        self.assertEqual(bom.metadata.tools.services[0].name, 'test-service')

    def test_tool_with_componet_and_service_render_xml(self) -> None:
        bom = Bom()
        bom.metadata.tools.components.add(Component(type=ComponentType.APPLICATION, author='adobe',
                                                    name='test-component', version='1.2.3'))
        bom.metadata.tools.services.add(Service(name='test-service'))
        out = XmlV1Dot5(bom).output_as_string(indent=2)
        self.assertIn("""   <tools>
      <components>
        <component type="application" bom-ref="None">
          <author>adobe</author>
          <name>test-component</name>
          <version>1.2.3</version>
        </component>
      </components>
      <services>
        <service bom-ref="None">
          <name>test-service</name>
        </service>
      </services>
    </tools>""", out)
