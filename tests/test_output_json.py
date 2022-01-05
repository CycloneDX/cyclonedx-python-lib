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
    IssueType, LicenseChoice, Note, NoteText, Property, XsUri
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component
from cyclonedx.model.release_note import ReleaseNotes
from cyclonedx.output import get_instance, OutputFormat, SchemaVersion
from cyclonedx.output.json import Json, JsonV1Dot4, JsonV1Dot3, JsonV1Dot2
from tests.base import BaseJsonTestCase


class TestOutputJson(BaseJsonTestCase):

    def test_simple_bom_v1_4(self) -> None:
        bom = Bom()
        c = Component(name='setuptools', version='50.3.2', package_url_qualifiers='extension=tar.gz')
        bom.add_component(c)

        outputter = get_instance(bom=bom, output_format=OutputFormat.JSON, schema_version=SchemaVersion.V1_4)
        self.assertIsInstance(outputter, JsonV1Dot4)
        with open(join(dirname(__file__), 'fixtures/bom_v1.4_setuptools.json')) as expected_json:
            self.assertValidAgainstSchema(bom_json=outputter.output_as_string(), schema_version=SchemaVersion.V1_4)
            self.assertEqualJsonBom(expected_json.read(), outputter.output_as_string())
            expected_json.close()

    def test_simple_bom_v1_3(self) -> None:
        bom = Bom()
        c = Component(name='setuptools', version='50.3.2', qualifiers='extension=tar.gz', license_str='MIT License')
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
            Component(name='setuptools', version='50.3.2', qualifiers='extension=tar.gz', author='Test Author')
        )
        outputter = get_instance(bom=bom, output_format=OutputFormat.JSON, schema_version=SchemaVersion.V1_2)
        self.assertIsInstance(outputter, JsonV1Dot2)
        with open(join(dirname(__file__), 'fixtures/bom_v1.2_setuptools.json')) as expected_json:
            self.assertValidAgainstSchema(bom_json=outputter.output_as_string(), schema_version=SchemaVersion.V1_2)
            self.assertEqualJsonBom(expected_json.read(), outputter.output_as_string())
            expected_json.close()

    def test_bom_v1_3_with_component_hashes(self) -> None:
        bom = Bom()
        c = Component(name='toml', version='0.10.2', qualifiers='extension=tar.gz')
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
        outputter: Json = get_instance(bom=bom, output_format=OutputFormat.JSON)
        self.assertIsInstance(outputter, JsonV1Dot3)
        with open(join(dirname(__file__),
                       'fixtures/bom_v1.3_toml_with_component_external_references.json')) as expected_json:
            self.assertValidAgainstSchema(bom_json=outputter.output_as_string(), schema_version=SchemaVersion.V1_3)
            self.assertEqualJsonBom(a=outputter.output_as_string(), b=expected_json.read())
            expected_json.close()

    def test_bom_v1_3_with_component_license(self) -> None:
        bom = Bom()
        c = Component(name='toml', version='0.10.2', qualifiers='extension=tar.gz', license_str='MIT License')
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
        c = Component(name='setuptools', package_url_qualifiers='extension=tar.gz')
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
            name='setuptools', version='50.3.2', package_url_qualifiers='extension=tar.gz',
            release_notes=ReleaseNotes(type='major'), licenses=[LicenseChoice(license_expression='MIT License')]
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
                properties=[
                    Property(name='key1', value='val1'),
                    Property(name='key2', value='val2')
                ]
            )
        )
        bom.add_component(c)
        outputter: Json = get_instance(bom=bom, output_format=OutputFormat.JSON, schema_version=SchemaVersion.V1_4)
        self.assertIsInstance(outputter, JsonV1Dot4)
        with open(join(dirname(__file__),
                       'fixtures/bom_v1.4_setuptools_with_release_notes.json')) as expected_json:
            self.assertValidAgainstSchema(bom_json=outputter.output_as_string(), schema_version=SchemaVersion.V1_3)
            self.assertEqualJsonBom(expected_json.read(), outputter.output_as_string())
            expected_json.close()
