from unittest import TestCase

from cyclonedx.output import get_instance, OutputFormat, SchemaVersion
from cyclonedx.output.xml import XmlV1Dot3


class TestOutputGeneric(TestCase):

    def test_get_instance_default(self):
        i = get_instance()
        self.assertIsInstance(i, XmlV1Dot3)

    def test_get_instance_xml(self):
        i = get_instance(output_format=OutputFormat.XML)
        self.assertIsInstance(i, XmlV1Dot3)

    def test_get_instance_xml_v1_3(self):
        i = get_instance(output_format=OutputFormat.XML, schema_version=SchemaVersion.V1_3)
        self.assertIsInstance(i, XmlV1Dot3)