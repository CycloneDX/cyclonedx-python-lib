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

from cyclonedx.model import ExternalReference, ExternalReferenceType, HashType, LicenseChoice
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component
from cyclonedx.output import get_instance, OutputFormat, SchemaVersion
from cyclonedx.output.json import Json, JsonV1Dot3, JsonV1Dot2
from tests.base import BaseJsonTestCase


class TestOutputJson(BaseJsonTestCase):

    def test_simple_bom_v1_3(self) -> None:
        bom = Bom()
        c = Component(name='setuptools', version='50.3.2', qualifiers='extension=tar.gz')
        bom.add_component(c)

        outputter = get_instance(bom=bom, output_format=OutputFormat.JSON)
        self.assertIsInstance(outputter, JsonV1Dot3)
        with open(join(dirname(__file__), 'fixtures/bom_v1.3_setuptools.json')) as expected_json:
            self.assertValidAgainstSchema(bom_json=outputter.output_as_string(), schema_version=SchemaVersion.V1_3)
            self.assertEqualJsonBom(expected_json.read(), outputter.output_as_string())
            expected_json.close()

    def test_simple_bom_v1_2(self) -> None:
        bom = Bom()
        bom.add_component(Component(name='setuptools', version='50.3.2', qualifiers='extension=tar.gz'))
        outputter = get_instance(bom=bom, output_format=OutputFormat.JSON, schema_version=SchemaVersion.V1_2)
        self.assertIsInstance(outputter, JsonV1Dot2)
        with open(join(dirname(__file__), 'fixtures/bom_v1.2_setuptools.json')) as expected_json:
            self.assertValidAgainstSchema(bom_json=outputter.output_as_string(), schema_version=SchemaVersion.V1_2)
            self.assertEqualJsonBom(outputter.output_as_string(), expected_json.read())
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
