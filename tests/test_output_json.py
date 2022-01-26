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
from decimal import Decimal
from datetime import datetime, timezone
from os.path import dirname, join
from typing import List

from packageurl import PackageURL
from unittest.mock import Mock, patch

from cyclonedx.model import Encoding, ExternalReference, ExternalReferenceType, HashType, LicenseChoice, Note, \
    NoteText, OrganizationalContact, OrganizationalEntity, Property, Tool, XsUri, DataClassification, DataFlow
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component, ComponentType
from cyclonedx.model.issue import IssueClassification, IssueType
from cyclonedx.model.release_note import ReleaseNotes
from cyclonedx.model.service import Service
from cyclonedx.model.vulnerability import ImpactAnalysisState, ImpactAnalysisJustification, ImpactAnalysisResponse, \
    ImpactAnalysisAffectedStatus, Vulnerability, VulnerabilityCredits, VulnerabilityRating, VulnerabilitySeverity, \
    VulnerabilitySource, VulnerabilityScoreSource, VulnerabilityAdvisory, VulnerabilityReference, \
    VulnerabilityAnalysis, BomTarget, BomTargetVersionRange
from cyclonedx.output import get_instance, OutputFormat, SchemaVersion
from cyclonedx.output.json import Json, JsonV1Dot4, JsonV1Dot3, JsonV1Dot2
from tests.base import BaseJsonTestCase


class TestOutputJson(BaseJsonTestCase):
    timestamp: datetime = datetime(2021, 12, 31, 10, 0, 0, 0).replace(tzinfo=timezone.utc)

    def test_simple_bom_v1_4(self) -> None:
        bom = Bom()
        c = Component(
            name='setuptools', version='50.3.2', bom_ref='pkg:pypi/setuptools@50.3.2?extension=tar.gz',
            purl=PackageURL(
                type='pypi', name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'
            )
        )
        bom.add_component(c)

        outputter = get_instance(bom=bom, output_format=OutputFormat.JSON, schema_version=SchemaVersion.V1_4)
        self.assertIsInstance(outputter, JsonV1Dot4)
        with open(join(dirname(__file__), 'fixtures/bom_v1.4_setuptools.json')) as expected_json:
            self.assertValidAgainstSchema(bom_json=outputter.output_as_string(), schema_version=SchemaVersion.V1_4)
            self.assertEqualJsonBom(expected_json.read(), outputter.output_as_string())
            expected_json.close()

    def test_simple_bom_v1_3(self) -> None:
        bom = Bom()
        c = Component(
            name='setuptools', version='50.3.2', bom_ref='pkg:pypi/setuptools@50.3.2?extension=tar.gz',
            purl=PackageURL(
                type='pypi', name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'
            ), license_str='MIT License'
        )
        bom.add_component(c)

        outputter = get_instance(bom=bom, output_format=OutputFormat.JSON)
        self.assertIsInstance(outputter, JsonV1Dot3)
        with open(join(dirname(__file__), 'fixtures/bom_v1.3_setuptools.json')) as expected_json:
            self.assertValidAgainstSchema(bom_json=outputter.output_as_string(), schema_version=SchemaVersion.V1_3)
            self.assertEqualJsonBom(expected_json.read(), outputter.output_as_string())
            expected_json.close()

    def test_simple_bom_v1_2(self) -> None:
        bom = Bom()
        bom.add_component(
            Component(
                name='setuptools', version='50.3.2', bom_ref='pkg:pypi/setuptools@50.3.2?extension=tar.gz',
                purl=PackageURL(
                    type='pypi', name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'
                ), author='Test Author'
            )
        )
        outputter = get_instance(bom=bom, output_format=OutputFormat.JSON, schema_version=SchemaVersion.V1_2)
        self.assertIsInstance(outputter, JsonV1Dot2)
        with open(join(dirname(__file__), 'fixtures/bom_v1.2_setuptools.json')) as expected_json:
            self.assertValidAgainstSchema(bom_json=outputter.output_as_string(), schema_version=SchemaVersion.V1_2)
            self.assertEqualJsonBom(expected_json.read(), outputter.output_as_string())
            expected_json.close()

    def test_simple_bom_v1_4_with_cpe(self) -> None:
        bom = Bom()
        c = Component(
            name='setuptools', version='50.3.2', bom_ref='pkg:pypi/setuptools@50.3.2?extension=tar.gz',
            cpe='cpe:2.3:a:python:setuptools:50.3.2:*:*:*:*:*:*:*',
            purl=PackageURL(
                type='pypi', name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'
            )
        )
        bom.add_component(c)

        outputter = get_instance(bom=bom, output_format=OutputFormat.JSON, schema_version=SchemaVersion.V1_4)
        self.assertIsInstance(outputter, JsonV1Dot4)
        with open(join(dirname(__file__), 'fixtures/bom_v1.4_setuptools_with_cpe.json')) as expected_json:
            self.assertValidAgainstSchema(bom_json=outputter.output_as_string(), schema_version=SchemaVersion.V1_4)
            self.assertEqualJsonBom(expected_json.read(), outputter.output_as_string())
            expected_json.close()

    def test_simple_bom_v1_3_with_cpe(self) -> None:
        bom = Bom()
        c = Component(
            name='setuptools', version='50.3.2', bom_ref='pkg:pypi/setuptools@50.3.2?extension=tar.gz',
            cpe='cpe:2.3:a:python:setuptools:50.3.2:*:*:*:*:*:*:*',
            purl=PackageURL(
                type='pypi', name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'
            ), license_str='MIT License'
        )
        bom.add_component(c)

        outputter = get_instance(bom=bom, output_format=OutputFormat.JSON)
        self.assertIsInstance(outputter, JsonV1Dot3)
        with open(join(dirname(__file__), 'fixtures/bom_v1.3_setuptools_with_cpe.json')) as expected_json:
            self.assertValidAgainstSchema(bom_json=outputter.output_as_string(), schema_version=SchemaVersion.V1_3)
            self.assertEqualJsonBom(expected_json.read(), outputter.output_as_string())
            expected_json.close()

    def test_simple_bom_v1_2_with_cpe(self) -> None:
        bom = Bom()
        bom.add_component(
            Component(
                name='setuptools', version='50.3.2', bom_ref='pkg:pypi/setuptools@50.3.2?extension=tar.gz',
                cpe='cpe:2.3:a:python:setuptools:50.3.2:*:*:*:*:*:*:*',
                purl=PackageURL(
                    type='pypi', name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'
                ), author='Test Author'
            )
        )
        outputter = get_instance(bom=bom, output_format=OutputFormat.JSON, schema_version=SchemaVersion.V1_2)
        self.assertIsInstance(outputter, JsonV1Dot2)
        with open(join(dirname(__file__), 'fixtures/bom_v1.2_setuptools_with_cpe.json')) as expected_json:
            self.assertValidAgainstSchema(bom_json=outputter.output_as_string(), schema_version=SchemaVersion.V1_2)
            self.assertEqualJsonBom(expected_json.read(), outputter.output_as_string())
            expected_json.close()

    def test_bom_v1_3_with_component_hashes(self) -> None:
        bom = Bom()
        c = Component(
            name='toml', version='0.10.2', bom_ref='pkg:pypi/toml@0.10.2?extension=tar.gz',
            purl=PackageURL(
                type='pypi', name='toml', version='0.10.2', qualifiers='extension=tar.gz'
            )
        )
        c.add_hash(
            HashType.from_composite_str('sha256:806143ae5bfb6a3c6e736a764057db0e6a0e05e338b5630894a5f779cabb4f9b')
        )
        bom.add_component(c)
        outputter: Json = get_instance(bom=bom, output_format=OutputFormat.JSON)
        self.assertIsInstance(outputter, JsonV1Dot3)
        with open(join(dirname(__file__), 'fixtures/bom_v1.3_toml_with_component_hashes.json')) as expected_json:
            self.assertValidAgainstSchema(bom_json=outputter.output_as_string(), schema_version=SchemaVersion.V1_3)
            self.assertEqualJsonBom(a=outputter.output_as_string(), b=expected_json.read())
            expected_json.close()

    def test_bom_v1_3_with_component_external_references(self) -> None:
        bom = Bom()
        c = Component(
            name='toml', version='0.10.2', bom_ref='pkg:pypi/toml@0.10.2?extension=tar.gz',
            purl=PackageURL(
                type='pypi', name='toml', version='0.10.2', qualifiers='extension=tar.gz'
            )
        )
        c.add_hash(
            HashType.from_composite_str('sha256:806143ae5bfb6a3c6e736a764057db0e6a0e05e338b5630894a5f779cabb4f9b')
        )
        c.add_external_reference(TestOutputJson._get_external_reference_1())
        bom.add_component(c)
        outputter: Json = get_instance(bom=bom, output_format=OutputFormat.JSON)
        self.assertIsInstance(outputter, JsonV1Dot3)
        with open(join(dirname(__file__),
                       'fixtures/bom_v1.3_toml_with_component_external_references.json')) as expected_json:
            self.assertValidAgainstSchema(bom_json=outputter.output_as_string(), schema_version=SchemaVersion.V1_3)
            self.assertEqualJsonBom(a=outputter.output_as_string(), b=expected_json.read())
            expected_json.close()

    def test_bom_v1_3_with_component_license(self) -> None:
        bom = Bom()
        c = Component(
            name='toml', version='0.10.2', bom_ref='pkg:pypi/toml@0.10.2?extension=tar.gz',
            purl=PackageURL(
                type='pypi', name='toml', version='0.10.2', qualifiers='extension=tar.gz'
            ), license_str='MIT License'
        )
        bom.add_component(c)
        outputter: Json = get_instance(bom=bom, output_format=OutputFormat.JSON)
        self.assertIsInstance(outputter, JsonV1Dot3)
        with open(join(dirname(__file__),
                       'fixtures/bom_v1.3_toml_with_component_license.json')) as expected_json:
            self.assertValidAgainstSchema(bom_json=outputter.output_as_string(), schema_version=SchemaVersion.V1_3)
            self.assertEqualJsonBom(a=outputter.output_as_string(), b=expected_json.read())
            expected_json.close()

    def test_bom_v1_4_no_component_version(self) -> None:
        bom = Bom()
        c = Component(
            name='setuptools', bom_ref='pkg:pypi/setuptools?extension=tar.gz',
            purl=PackageURL(
                type='pypi', name='setuptools', qualifiers='extension=tar.gz'
            )
        )
        bom.add_component(c)

        outputter = get_instance(bom=bom, output_format=OutputFormat.JSON, schema_version=SchemaVersion.V1_4)
        self.assertIsInstance(outputter, JsonV1Dot4)
        with open(join(dirname(__file__), 'fixtures/bom_v1.4_setuptools_no_version.json')) as expected_json:
            self.assertValidAgainstSchema(bom_json=outputter.output_as_string(), schema_version=SchemaVersion.V1_4)
            self.assertEqualJsonBom(expected_json.read(), outputter.output_as_string())
            expected_json.close()

    def test_with_component_release_notes_pre_1_4(self) -> None:
        bom = Bom()
        c = Component(
            name='setuptools', version='50.3.2', bom_ref='pkg:pypi/setuptools@50.3.2?extension=tar.gz',
            purl=PackageURL(
                type='pypi', name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'
            ), release_notes=ReleaseNotes(type='major'), licenses=[LicenseChoice(license_expression='MIT License')]
        )
        bom.add_component(c)
        outputter: Json = get_instance(bom=bom, output_format=OutputFormat.JSON, schema_version=SchemaVersion.V1_3)
        self.assertIsInstance(outputter, JsonV1Dot3)
        with open(join(dirname(__file__), 'fixtures/bom_v1.3_setuptools.json')) as expected_json:
            self.assertValidAgainstSchema(bom_json=outputter.output_as_string(), schema_version=SchemaVersion.V1_3)
            self.assertEqualJsonBom(expected_json.read(), outputter.output_as_string())
            expected_json.close()

    def test_with_component_release_notes_post_1_4(self) -> None:
        bom = Bom()
        c = Component(
            name='setuptools', version='50.3.2', bom_ref='pkg:pypi/setuptools@50.3.2?extension=tar.gz',
            purl=PackageURL(
                type='pypi', name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'
            ),
            release_notes=TestOutputJson._get_release_notes()
        )
        bom.add_component(c)
        outputter: Json = get_instance(bom=bom, output_format=OutputFormat.JSON, schema_version=SchemaVersion.V1_4)
        self.assertIsInstance(outputter, JsonV1Dot4)
        with open(join(dirname(__file__),
                       'fixtures/bom_v1.4_setuptools_with_release_notes.json')) as expected_json:
            self.assertValidAgainstSchema(bom_json=outputter.output_as_string(), schema_version=SchemaVersion.V1_3)
            self.assertEqualJsonBom(expected_json.read(), outputter.output_as_string())
            expected_json.close()

    def test_simple_bom_v1_4_with_vulnerabilities(self) -> None:
        bom = Bom()
        nvd = VulnerabilitySource(name='NVD', url=XsUri('https://nvd.nist.gov/vuln/detail/CVE-2018-7489'))
        owasp = VulnerabilitySource(name='OWASP', url=XsUri('https://owasp.org'))
        c = Component(
            name='setuptools', version='50.3.2', bom_ref='pkg:pypi/setuptools@50.3.2?extension=tar.gz',
            purl=PackageURL(
                type='pypi', name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'
            )
        )
        c.add_vulnerability(Vulnerability(
            bom_ref='my-vuln-ref-1', id='CVE-2018-7489', source=nvd,
            references=[
                VulnerabilityReference(id='SOME-OTHER-ID', source=VulnerabilitySource(
                    name='OSS Index', url=XsUri('https://ossindex.sonatype.org/component/pkg:pypi/setuptools')
                ))
            ],
            ratings=[
                VulnerabilityRating(
                    source=nvd, score=Decimal(9.8), severity=VulnerabilitySeverity.CRITICAL,
                    method=VulnerabilityScoreSource.CVSS_V3,
                    vector='AN/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H', justification='Some justification'
                ),
                VulnerabilityRating(
                    source=owasp, score=Decimal(2.7), severity=VulnerabilitySeverity.LOW,
                    method=VulnerabilityScoreSource.CVSS_V3,
                    vector='AV:L/AC:H/PR:N/UI:R/S:C/C:L/I:N/A:N', justification='Some other justification'
                )
            ],
            cwes=[22, 33], description='A description here', detail='Some detail here',
            recommendation='Upgrade',
            advisories=[
                VulnerabilityAdvisory(url=XsUri('https://nvd.nist.gov/vuln/detail/CVE-2018-7489')),
                VulnerabilityAdvisory(url=XsUri('http://www.securitytracker.com/id/1040693'))
            ],
            created=datetime(year=2021, month=9, day=1, hour=10, minute=50, second=42, microsecond=51979,
                             tzinfo=timezone.utc),
            published=datetime(year=2021, month=9, day=2, hour=10, minute=50, second=42, microsecond=51979,
                               tzinfo=timezone.utc),
            updated=datetime(year=2021, month=9, day=3, hour=10, minute=50, second=42, microsecond=51979,
                             tzinfo=timezone.utc),
            credits=VulnerabilityCredits(
                organizations=[
                    TestOutputJson._get_org_entity_1()
                ],
                individuals=[
                    OrganizationalContact(name='A N Other', email='someone@somewhere.tld', phone='+44 (0)1234 567890'),
                ]
            ),
            tools=[
                Tool(vendor='CycloneDX', name='cyclonedx-python-lib')
            ],
            analysis=VulnerabilityAnalysis(
                state=ImpactAnalysisState.EXPLOITABLE, justification=ImpactAnalysisJustification.REQUIRES_ENVIRONMENT,
                responses=[ImpactAnalysisResponse.CAN_NOT_FIX], detail='Some extra detail'
            ),
            affects_targets=[
                BomTarget(ref=c.purl or c.to_package_url().to_string(), versions=[
                    BomTargetVersionRange(version_range='49.0.0 - 54.0.0', status=ImpactAnalysisAffectedStatus.AFFECTED)
                ])
            ]
        ))
        bom.add_component(c)
        outputter: Json = get_instance(bom=bom, output_format=OutputFormat.JSON, schema_version=SchemaVersion.V1_4)
        self.assertIsInstance(outputter, JsonV1Dot4)
        with open(join(dirname(__file__), 'fixtures/bom_v1.4_setuptools_with_vulnerabilities.json')) as expected_json:
            self.assertValidAgainstSchema(bom_json=outputter.output_as_string(), schema_version=SchemaVersion.V1_4)
            self.assertEqualJsonBom(expected_json.read(), outputter.output_as_string())
            expected_json.close()

    @patch('cyclonedx.model.component.uuid4', return_value='be2c6502-7e9a-47db-9a66-e34f729810a3')
    def test_bom_v1_3_with_metadata_component(self, mock_uuid: Mock) -> None:
        bom = Bom()
        bom.metadata.component = Component(
            name='cyclonedx-python-lib', version='1.0.0', component_type=ComponentType.LIBRARY
        )
        mock_uuid.assert_called()
        outputter = get_instance(bom=bom, output_format=OutputFormat.JSON)
        self.assertIsInstance(outputter, JsonV1Dot3)
        with open(join(dirname(__file__), 'fixtures/bom_v1.3_with_metadata_component.json')) as expected_json:
            self.assertEqualJsonBom(outputter.output_as_string(), expected_json.read())

    @patch('cyclonedx.model.component.uuid4', return_value='17e3b199-dc0b-42ef-bfdd-1fa81a1e3eda')
    @patch('cyclonedx.model.service.uuid4', return_value='0b049d09-64c0-4490-a0f5-c84d9aacf857')
    def test_bom_v1_2_services(self, mock_uuid_c: Mock, mock_uuid_s: Mock) -> None:
        bom = Bom(services=[
            Service(name='my-first-service'),
            Service(name='my-second-service')
        ])
        bom.metadata.component = Component(
            name='cyclonedx-python-lib', version='1.0.0', component_type=ComponentType.LIBRARY
        )
        mock_uuid_c.assert_called()
        mock_uuid_s.assert_called()
        outputter = get_instance(bom=bom, output_format=OutputFormat.JSON, schema_version=SchemaVersion.V1_2)
        self.assertIsInstance(outputter, JsonV1Dot2)
        with open(join(dirname(__file__), 'fixtures/bom_v1.2_services_simple.json')) as expected_json:
            self.assertValidAgainstSchema(bom_json=outputter.output_as_string(), schema_version=SchemaVersion.V1_2)
            self.assertEqualJsonBom(outputter.output_as_string(), expected_json.read())

    @patch('cyclonedx.model.component.uuid4', return_value='17e3b199-dc0b-42ef-bfdd-1fa81a1e3eda')
    @patch('cyclonedx.model.service.uuid4', return_value='0b049d09-64c0-4490-a0f5-c84d9aacf857')
    def test_bom_v1_2_services_simple(self, mock_uuid_c: Mock, mock_uuid_s: Mock) -> None:
        bom = TestOutputJson._get_bom_with_services_simple()
        mock_uuid_c.assert_called()
        mock_uuid_s.assert_called()
        outputter = get_instance(bom=bom, output_format=OutputFormat.JSON, schema_version=SchemaVersion.V1_2)
        self.assertIsInstance(outputter, JsonV1Dot2)
        with open(join(dirname(__file__), 'fixtures/bom_v1.2_services_simple.json')) as expected_json:
            self.assertValidAgainstSchema(bom_json=outputter.output_as_string(), schema_version=SchemaVersion.V1_2)
            self.assertEqualJsonBom(outputter.output_as_string(), expected_json.read())

    @patch('cyclonedx.model.component.uuid4', return_value='17e3b199-dc0b-42ef-bfdd-1fa81a1e3eda')
    @patch('cyclonedx.model.service.uuid4', return_value='0b049d09-64c0-4490-a0f5-c84d9aacf857')
    def test_bom_v1_2_services_complex(self, mock_uuid_c: Mock, mock_uuid_s: Mock) -> None:
        bom = TestOutputJson._get_bom_with_services_complex()
        mock_uuid_c.assert_called()
        mock_uuid_s.assert_called()
        outputter = get_instance(bom=bom, output_format=OutputFormat.JSON, schema_version=SchemaVersion.V1_2)
        self.assertIsInstance(outputter, JsonV1Dot2)
        with open(join(dirname(__file__), 'fixtures/bom_v1.2_services_complex.json')) as expected_json:
            self.assertValidAgainstSchema(bom_json=outputter.output_as_string(), schema_version=SchemaVersion.V1_2)
            self.assertEqualJsonBom(outputter.output_as_string(), expected_json.read())

    @staticmethod
    def _get_bom_with_services_simple() -> Bom:
        bom = Bom(services=[
            Service(name='my-first-service'),
            Service(name='my-second-service')
        ])
        bom.metadata.component = Component(
            name='cyclonedx-python-lib', version='1.0.0', component_type=ComponentType.LIBRARY
        )
        return bom

    @staticmethod
    def _get_bom_with_services_complex() -> Bom:
        bom = Bom(services=[
            Service(
                name='my-first-service', bom_ref='my-specific-bom-ref-for-my-first-service',
                provider=TestOutputJson._get_org_entity_1(), group='a-group', version='1.2.3',
                description='Description goes here', endpoints=[
                    XsUri('/api/thing/1'),
                    XsUri('/api/thing/2')
                ],
                authenticated=False, x_trust_boundary=True, data=[
                    DataClassification(flow=DataFlow.OUTBOUND, classification='public')
                ],
                licenses=[
                    LicenseChoice(license_expression='Commercial')
                ],
                external_references=[
                    TestOutputJson._get_external_reference_1()
                ],
                properties=TestOutputJson._get_properties_1(),
                release_notes=TestOutputJson._get_release_notes()
            ),
            Service(name='my-second-service')
        ])
        bom.metadata.component = Component(
            name='cyclonedx-python-lib', version='1.0.0', component_type=ComponentType.LIBRARY
        )
        return bom

    @staticmethod
    def _get_external_reference_1() -> ExternalReference:
        return ExternalReference(
            reference_type=ExternalReferenceType.DISTRIBUTION,
            url='https://cyclonedx.org',
            comment='No comment',
            hashes=[
                HashType.from_composite_str(
                    'sha256:806143ae5bfb6a3c6e736a764057db0e6a0e05e338b5630894a5f779cabb4f9b')
            ]
        )

    @staticmethod
    def _get_org_entity_1() -> OrganizationalEntity:
        return OrganizationalEntity(
            name='CycloneDX', urls=[XsUri('https://cyclonedx.org')], contacts=[
                OrganizationalContact(name='Paul Horton', email='paul.horton@owasp.org'),
                OrganizationalContact(name='A N Other', email='someone@somewhere.tld',
                                      phone='+44 (0)1234 567890')
            ]
        )

    @staticmethod
    def _get_properties_1() -> List[Property]:
        return [
            Property(name='key1', value='val1'),
            Property(name='key2', value='val2')
        ]

    @staticmethod
    def _get_release_notes() -> ReleaseNotes:
        text_content: str = base64.b64encode(
            bytes('Some simple plain text', encoding='UTF-8')
        ).decode(encoding='UTF-8')

        return ReleaseNotes(
            type='major', title="Release Notes Title",
            featured_image=XsUri('https://cyclonedx.org/theme/assets/images/CycloneDX-Twitter-Card.png'),
            social_image=XsUri('https://cyclonedx.org/cyclonedx-icon.png'),
            description="This release is a test release", timestamp=TestOutputJson.timestamp,
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
                    text=NoteText(
                        content=text_content, content_type='text/plain; charset=UTF-8',
                        content_encoding=Encoding.BASE_64
                    ), locale='en-GB'
                ),
                Note(
                    text=NoteText(
                        content=text_content, content_type='text/plain; charset=UTF-8',
                        content_encoding=Encoding.BASE_64
                    ), locale='en-US'
                )
            ],
            properties=TestOutputJson._get_properties_1()
        )
