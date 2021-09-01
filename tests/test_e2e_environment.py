import json
from unittest import TestCase
from xml.etree import ElementTree

from cyclonedx.model.bom import Bom
from cyclonedx.output import get_instance, OutputFormat
from cyclonedx.output.json import Json
from cyclonedx.output.xml import Xml
from cyclonedx.parser.environment import EnvironmentParser


class TestE2EEnvironment(TestCase):

    def test_json_defaults(self):
        outputter: Json = get_instance(bom=Bom.from_parser(EnvironmentParser()), output_format=OutputFormat.JSON)
        bom_json = json.loads(outputter.output_as_string())
        component_this_library = next(
            (x for x in bom_json['components'] if x['purl'] == 'pkg:pypi/cyclonedx-python-lib@0.0.1'), None
        )

        self.assertTrue('author' in component_this_library.keys(), 'author is missing from JSON BOM')
        self.assertEqual(component_this_library['author'], 'Sonatype Community')
        self.assertEqual(component_this_library['name'], 'cyclonedx-python-lib')
        self.assertEqual(component_this_library['version'], '0.0.1')

    def test_xml_defaults(self):
        outputter: Xml = get_instance(bom=Bom.from_parser(EnvironmentParser()))

        # Check we have cyclonedx-python-lib version 0.0.1 with Author, Name and Version
        bom_xml_e = ElementTree.fromstring(outputter.output_as_string())
        component_this_library = bom_xml_e.find('./{{{}}}components/{{{}}}component[@bom-ref=\'pkg:pypi/{}\']'.format(
            outputter.get_target_namespace(), outputter.get_target_namespace(), 'cyclonedx-python-lib@0.0.1'
        ))

        author = component_this_library.find('./{{{}}}author'.format(outputter.get_target_namespace()))
        self.assertIsNotNone(author, 'No author element but one was expected.')
        self.assertEqual(author.text, 'Sonatype Community')

        name = component_this_library.find('./{{{}}}name'.format(outputter.get_target_namespace()))
        self.assertIsNotNone(name, 'No name element but one was expected.')
        self.assertEqual(name.text, 'cyclonedx-python-lib')

        version = component_this_library.find('./{{{}}}version'.format(outputter.get_target_namespace()))
        self.assertIsNotNone(version, 'No version element but one was expected.')
        self.assertEqual(version.text, '0.0.1')
