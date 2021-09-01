from os.path import dirname, join

from cyclonedx.model.bom import Bom
from cyclonedx.model.cyclonedx import Component
from cyclonedx.output import get_instance, SchemaVersion
from cyclonedx.output.xml import XmlV1Dot3, XmlV1Dot2, Xml

from tests.base import BaseXmlTestCase


class TestOutputXml(BaseXmlTestCase):

    def test_simple_bom_v1_3(self):
        bom = Bom()
        bom.add_component(Component(name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'))
        outputter: Xml = get_instance(bom=bom)
        self.assertIsInstance(outputter, XmlV1Dot3)
        with open(join(dirname(__file__), 'fixtures/bom_v1.3_setuptools.xml')) as expected_xml:
            self.assertEqualXmlBom(a=outputter.output_as_string(), b=expected_xml.read(),
                                   namespace=outputter.get_target_namespace())
            expected_xml.close()

    def test_simple_bom_v1_2(self):
        bom = Bom()
        bom.add_component(Component(name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'))
        outputter = get_instance(bom=bom, schema_version=SchemaVersion.V1_2)
        self.assertIsInstance(outputter, XmlV1Dot2)
        with open(join(dirname(__file__), 'fixtures/bom_v1.2_setuptools.xml')) as expected_xml:
            self.assertEqualXmlBom(outputter.output_as_string(), expected_xml.read(),
                                   namespace=outputter.get_target_namespace())
            expected_xml.close()
