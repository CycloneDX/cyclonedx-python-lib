from os.path import dirname, join
from tests.base import BaseJsonTestCase

from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component
from cyclonedx.output import get_instance, OutputFormat, SchemaVersion
from cyclonedx.output.json import JsonV1Dot3, JsonV1Dot2


class TestOutputJson(BaseJsonTestCase):

    def test_simple_bom_v1_3(self):
        bom = Bom()
        bom.add_component(Component(name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'))
        outputter = get_instance(bom=bom, output_format=OutputFormat.JSON)
        self.assertIsInstance(outputter, JsonV1Dot3)
        with open(join(dirname(__file__), 'fixtures/bom_v1.3_setuptools.json')) as expected_json:
            self.assertEqualJsonBom(outputter.output_as_string(), expected_json.read())
            expected_json.close()

    def test_simple_bom_v1_2(self):
        bom = Bom()
        bom.add_component(Component(name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'))
        outputter = get_instance(bom=bom, output_format=OutputFormat.JSON, schema_version=SchemaVersion.V1_2)
        self.assertIsInstance(outputter, JsonV1Dot2)
        with open(join(dirname(__file__), 'fixtures/bom_v1.2_setuptools.json')) as expected_json:
            self.assertEqualJsonBom(outputter.output_as_string(), expected_json.read())
            expected_json.close()
