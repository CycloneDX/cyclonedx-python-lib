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
import base64
from datetime import datetime, timezone
from os.path import dirname, join

from cyclonedx.model import Encoding, ExternalReference, ExternalReferenceType, HashType, IssueClassification, \
    IssueType, Note, Properties, Property, XsUri
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component
from cyclonedx.model.release_note import ReleaseNotes
from cyclonedx.model.vulnerability import Vulnerability, VulnerabilityRating, VulnerabilitySeverity, \
    VulnerabilityScoreSourceType
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
                                    severity=VulnerabilitySeverity.CRITICAL, method=VulnerabilityScoreSourceType.CVSS_V3,
                                    vector='AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H'),
                VulnerabilityRating(severity=VulnerabilitySeverity.LOW, method=VulnerabilityScoreSourceType.OWASP,
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
                                    severity=VulnerabilitySeverity.CRITICAL, method=VulnerabilityScoreSourceType.CVSS_V3,
                                    vector='AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H'),
                VulnerabilityRating(severity=VulnerabilitySeverity.LOW, method=VulnerabilityScoreSourceType.OWASP,
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

    def test_with_component_release_notes_pre_1_4(self) -> None:
        bom = Bom()
        c = Component(
            name='toml', version='0.10.2', qualifiers='extension=tar.gz',
            release_notes=ReleaseNotes(type='major')
        )
        c.set_license('MIT License')
        bom.add_component(c)
        outputter: Xml = get_instance(bom=bom, schema_version=SchemaVersion.V1_3)
        self.assertIsInstance(outputter, XmlV1Dot3)
        with open(join(dirname(__file__),
                       'fixtures/bom_v1.3_toml_with_component_license.xml')) as expected_xml:
            self.assertValidAgainstSchema(bom_xml=outputter.output_as_string(), schema_version=SchemaVersion.V1_3)
            self.assertEqualXmlBom(a=outputter.output_as_string(), b=expected_xml.read(),
                                   namespace=outputter.get_target_namespace())
            expected_xml.close()

    def test_with_component_release_notes_post_1_4(self) -> None:
        bom = Bom()
        timestamp: datetime = datetime(2021, 12, 31, 10, 0, 0, 0).replace(tzinfo=timezone.utc)

        text_content: str = base64.b64encode(
            bytearray('Some simple plain text', encoding='UTF-8')
        ).decode(encoding='UTF-8')

        c = Component(
            name='setuptools', version='50.3.2', qualifiers='extension=tar.gz',
            release_notes=ReleaseNotes(
                type='major', title="Release Notes Title",
                featured_image=XsUri('https://cyclonedx.org/theme/assets/images/CycloneDX-Twitter-Card.png'),
                social_image=XsUri('https://cyclonedx.org/cyclonedx-icon.png'),
                description="This release is a test release", timestamp=timestamp,
                aliases=[
                    "First Test Release"
                ],
                tags=['test', 'alpha'],
                resolves=[
                    IssueType(
                        classification=IssueClassification.SECURITY, id='CVE-2021-44228', name='Apache Log3Shell',
                        description='Apache Log4j2 2.0-beta9 through 2.12.1 and 2.13.0 through 2.15.0 JNDI features...',
                        source_name='NVD', source_url=XsUri('https://nvd.nist.gov/vuln/detail/CVE-2021-44228'),
                        references=[
                            XsUri('https://logging.apache.org/log4j/2.x/security.html'),
                            XsUri('https://central.sonatype.org/news/20211213_log4shell_help')
                        ]
                    )
                ],
                notes=[
                    Note(
                        text=text_content, locale='en-GB', content_type='text/plain; charset=UTF-8',
                        content_encoding=Encoding.BASE_64
                    ),
                    Note(
                        text=text_content, locale='en-US', content_type='text/plain; charset=UTF-8',
                        content_encoding=Encoding.BASE_64
                    )
                ],
                properties=Properties(properties=[
                    Property(name='key1', value='val1'),
                    Property(name='key2', value='val2')
                ])
            )
        )
        bom.add_component(c)
        outputter: Xml = get_instance(bom=bom, schema_version=SchemaVersion.V1_4)
        self.assertIsInstance(outputter, XmlV1Dot4)
        with open(join(dirname(__file__),
                       'fixtures/bom_v1.4_setuptools_with_release_notes.xml')) as expected_xml:
            self.assertValidAgainstSchema(bom_xml=outputter.output_as_string(), schema_version=SchemaVersion.V1_4)
            self.assertEqualXmlBom(a=outputter.output_as_string(), b=expected_xml.read(),
                                   namespace=outputter.get_target_namespace())
            expected_xml.close()
