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

from os.path import dirname, join

from cyclonedx.model import ExternalReference, ExternalReferenceType, HashType
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component
from cyclonedx.model.vulnerability import Vulnerability, VulnerabilityRating, VulnerabilitySeverity, \
    VulnerabilitySourceType
from cyclonedx.output import get_instance, SchemaVersion
from cyclonedx.output.xml import XmlV1Dot4, XmlV1Dot3, XmlV1Dot2, XmlV1Dot1, XmlV1Dot0, Xml
from tests.base import BaseXmlTestCase


class TestOutputXml(BaseXmlTestCase):

    def test_simple_bom_v1_4(self) -> None:
        bom = Bom()
        bom.add_component(Component(name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'))
        outputter: Xml = get_instance(bom=bom, schema_version=SchemaVersion.V1_4)
        self.assertIsInstance(outputter, XmlV1Dot4)
        with open(join(dirname(__file__), 'fixtures/bom_v1.4_setuptools.xml')) as expected_xml:
            self.assertValidAgainstSchema(bom_xml=outputter.output_as_string(), schema_version=SchemaVersion.V1_4)
            self.assertEqualXmlBom(a=outputter.output_as_string(), b=expected_xml.read(),
                                   namespace=outputter.get_target_namespace())
            expected_xml.close()

    def test_simple_bom_v1_3(self) -> None:
        bom = Bom()
        bom.add_component(Component(name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'))
        outputter: Xml = get_instance(bom=bom)
        self.assertIsInstance(outputter, XmlV1Dot3)
        with open(join(dirname(__file__), 'fixtures/bom_v1.3_setuptools.xml')) as expected_xml:
            self.assertValidAgainstSchema(bom_xml=outputter.output_as_string(), schema_version=SchemaVersion.V1_3)
            self.assertEqualXmlBom(a=outputter.output_as_string(), b=expected_xml.read(),
                                   namespace=outputter.get_target_namespace())
            expected_xml.close()

    def test_simple_bom_v1_2(self) -> None:
        bom = Bom()
        bom.add_component(Component(name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'))
        outputter = get_instance(bom=bom, schema_version=SchemaVersion.V1_2)
        self.assertIsInstance(outputter, XmlV1Dot2)
        with open(join(dirname(__file__), 'fixtures/bom_v1.2_setuptools.xml')) as expected_xml:
            self.assertValidAgainstSchema(bom_xml=outputter.output_as_string(), schema_version=SchemaVersion.V1_2)
            self.assertEqualXmlBom(outputter.output_as_string(), expected_xml.read(),
                                   namespace=outputter.get_target_namespace())
            expected_xml.close()

    def test_simple_bom_v1_1(self) -> None:
        bom = Bom()
        bom.add_component(Component(name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'))
        outputter = get_instance(bom=bom, schema_version=SchemaVersion.V1_1)
        self.assertIsInstance(outputter, XmlV1Dot1)
        with open(join(dirname(__file__), 'fixtures/bom_v1.1_setuptools.xml')) as expected_xml:
            self.assertValidAgainstSchema(bom_xml=outputter.output_as_string(), schema_version=SchemaVersion.V1_1)
            self.assertEqualXmlBom(outputter.output_as_string(), expected_xml.read(),
                                   namespace=outputter.get_target_namespace())
            expected_xml.close()

    def test_simple_bom_v1_0(self) -> None:
        bom = Bom()
        bom.add_component(Component(name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'))
        self.assertEqual(len(bom.get_components()), 1)
        outputter = get_instance(bom=bom, schema_version=SchemaVersion.V1_0)
        self.assertIsInstance(outputter, XmlV1Dot0)
        with open(join(dirname(__file__), 'fixtures/bom_v1.0_setuptools.xml')) as expected_xml:
            self.assertValidAgainstSchema(bom_xml=outputter.output_as_string(), schema_version=SchemaVersion.V1_0)
            self.assertEqualXmlBom(outputter.output_as_string(), expected_xml.read(),
                                   namespace=outputter.get_target_namespace())
            expected_xml.close()

    def test_simple_bom_v1_3_with_vulnerabilities(self) -> None:
        bom = Bom()
        c = Component(name='setuptools', version='50.3.2', qualifiers='extension=tar.gz')
        c.add_vulnerability(Vulnerability(
            id='CVE-2018-7489', source_name='NVD', source_url='https://nvd.nist.gov/vuln/detail/CVE-2018-7489',
            ratings=[
                VulnerabilityRating(score_base=9.8, score_impact=5.9, score_exploitability=3.0,
                                    severity=VulnerabilitySeverity.CRITICAL, method=VulnerabilitySourceType.CVSS_V3,
                                    vector='AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H'),
                VulnerabilityRating(severity=VulnerabilitySeverity.LOW, method=VulnerabilitySourceType.OWASP,
                                    vector='OWASP/K9:M1:O0:Z2/D1:X1:W1:L3/C2:I1:A1:T1/F1:R1:S2:P3/50', )
            ],
            cwes=[123, 456], description='A description here', recommendations=['Upgrade'],
            advisories=[
                'http://www.securityfocus.com/bid/103203',
                'http://www.securitytracker.com/id/1040693'
            ]
        ))
        bom.add_component(c)
        outputter: Xml = get_instance(bom=bom)
        self.assertIsInstance(outputter, XmlV1Dot3)
        with open(join(dirname(__file__), 'fixtures/bom_v1.3_setuptools_with_vulnerabilities.xml')) as expected_xml:
            self.assertValidAgainstSchema(bom_xml=outputter.output_as_string(), schema_version=SchemaVersion.V1_3)
            self.assertEqualXmlBom(a=outputter.output_as_string(), b=expected_xml.read(),
                                   namespace=outputter.get_target_namespace())

            expected_xml.close()

    def test_simple_bom_v1_0_with_vulnerabilities(self) -> None:
        bom = Bom()
        c = Component(name='setuptools', version='50.3.2', qualifiers='extension=tar.gz')
        c.add_vulnerability(Vulnerability(
            id='CVE-2018-7489', source_name='NVD', source_url='https://nvd.nist.gov/vuln/detail/CVE-2018-7489',
            ratings=[
                VulnerabilityRating(score_base=9.8, score_impact=5.9, score_exploitability=3.0,
                                    severity=VulnerabilitySeverity.CRITICAL, method=VulnerabilitySourceType.CVSS_V3,
                                    vector='AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H'),
                VulnerabilityRating(severity=VulnerabilitySeverity.LOW, method=VulnerabilitySourceType.OWASP,
                                    vector='OWASP/K9:M1:O0:Z2/D1:X1:W1:L3/C2:I1:A1:T1/F1:R1:S2:P3/50', )
            ],
            cwes=[123, 456], description='A description here', recommendations=['Upgrade'],
            advisories=[
                'http://www.securityfocus.com/bid/103203',
                'http://www.securitytracker.com/id/1040693'
            ]
        ))
        bom.add_component(c)
        outputter: Xml = get_instance(bom=bom, schema_version=SchemaVersion.V1_0)
        self.assertIsInstance(outputter, XmlV1Dot0)
        with open(join(dirname(__file__), 'fixtures/bom_v1.0_setuptools.xml')) as expected_xml:
            self.assertValidAgainstSchema(bom_xml=outputter.output_as_string(), schema_version=SchemaVersion.V1_0)
            self.assertEqualXmlBom(a=outputter.output_as_string(), b=expected_xml.read(),
                                   namespace=outputter.get_target_namespace())

            expected_xml.close()

    def test_bom_v1_3_with_component_hashes(self) -> None:
        bom = Bom()
        c = Component(name='toml', version='0.10.2', qualifiers='extension=tar.gz')
        c.add_hash(
            HashType.from_composite_str('sha256:806143ae5bfb6a3c6e736a764057db0e6a0e05e338b5630894a5f779cabb4f9b')
        )
        bom.add_component(c)
        outputter: Xml = get_instance(bom=bom)
        self.assertIsInstance(outputter, XmlV1Dot3)
        with open(join(dirname(__file__), 'fixtures/bom_v1.3_toml_with_component_hashes.xml')) as expected_xml:
            self.assertValidAgainstSchema(bom_xml=outputter.output_as_string(), schema_version=SchemaVersion.V1_3)
            self.assertEqualXmlBom(a=outputter.output_as_string(), b=expected_xml.read(),
                                   namespace=outputter.get_target_namespace())
            expected_xml.close()

    def test_bom_v1_3_with_component_external_references(self) -> None:
        bom = Bom()
        c = Component(name='toml', version='0.10.2', qualifiers='extension=tar.gz')
        c.add_hash(
            HashType.from_composite_str('sha256:806143ae5bfb6a3c6e736a764057db0e6a0e05e338b5630894a5f779cabb4f9b')
        )
        c.add_external_reference(
            ExternalReference(
                reference_type=ExternalReferenceType.DISTRIBUTION,
                url='https://cyclonedx.org',
                comment='No comment',
                hashes=[
                    HashType.from_composite_str(
                        'sha256:806143ae5bfb6a3c6e736a764057db0e6a0e05e338b5630894a5f779cabb4f9b')
                ]
            )
        )
        bom.add_component(c)
        outputter: Xml = get_instance(bom=bom)
        self.assertIsInstance(outputter, XmlV1Dot3)
        with open(join(dirname(__file__),
                       'fixtures/bom_v1.3_toml_with_component_external_references.xml')) as expected_xml:
            self.assertValidAgainstSchema(bom_xml=outputter.output_as_string(), schema_version=SchemaVersion.V1_3)
            self.assertEqualXmlBom(a=outputter.output_as_string(), b=expected_xml.read(),
                                   namespace=outputter.get_target_namespace())
            expected_xml.close()

    def test_with_component_license(self) -> None:
        bom = Bom()
        c = Component(name='toml', version='0.10.2', qualifiers='extension=tar.gz')
        c.set_license('MIT License')
        bom.add_component(c)
        outputter: Xml = get_instance(bom=bom)
        self.assertIsInstance(outputter, XmlV1Dot3)
        with open(join(dirname(__file__),
                       'fixtures/bom_v1.3_toml_with_component_license.xml')) as expected_xml:
            self.assertValidAgainstSchema(bom_xml=outputter.output_as_string(), schema_version=SchemaVersion.V1_3)
            self.assertEqualXmlBom(a=outputter.output_as_string(), b=expected_xml.read(),
                                   namespace=outputter.get_target_namespace())
            expected_xml.close()

    def test_with_no_component_version_1_4(self) -> None:
        bom = Bom()
        bom.add_component(Component(name='setuptools', qualifiers='extension=tar.gz'))
        outputter: Xml = get_instance(bom=bom, schema_version=SchemaVersion.V1_4)
        self.assertIsInstance(outputter, XmlV1Dot4)
        with open(join(dirname(__file__),
                       'fixtures/bom_v1.4_setuptools_no_version.xml')) as expected_xml:
            self.assertValidAgainstSchema(bom_xml=outputter.output_as_string(), schema_version=SchemaVersion.V1_4)
            self.assertEqualXmlBom(a=outputter.output_as_string(), b=expected_xml.read(),
                                   namespace=outputter.get_target_namespace())
            expected_xml.close()
