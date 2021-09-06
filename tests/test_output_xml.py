# encoding: utf-8

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

from os.path import dirname, join

from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component
from cyclonedx.output import get_instance, SchemaVersion
from cyclonedx.output.xml import XmlV1Dot3, XmlV1Dot2, XmlV1Dot1, XmlV1Dot0, Xml
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

    def test_simple_bom_v1_1(self):
        bom = Bom()
        bom.add_component(Component(name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'))
        outputter = get_instance(bom=bom, schema_version=SchemaVersion.V1_1)
        self.assertIsInstance(outputter, XmlV1Dot1)
        with open(join(dirname(__file__), 'fixtures/bom_v1.1_setuptools.xml')) as expected_xml:
            self.assertEqualXmlBom(outputter.output_as_string(), expected_xml.read(),
                                   namespace=outputter.get_target_namespace())
            expected_xml.close()

    def test_simple_bom_v1_0(self):
        bom = Bom()
        bom.add_component(Component(name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'))
        outputter = get_instance(bom=bom, schema_version=SchemaVersion.V1_0)
        self.assertIsInstance(outputter, XmlV1Dot0)
        with open(join(dirname(__file__), 'fixtures/bom_v1.0_setuptools.xml')) as expected_xml:
            self.assertEqualXmlBom(outputter.output_as_string(), expected_xml.read(),
                                   namespace=outputter.get_target_namespace())
            expected_xml.close()
