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

from unittest import TestCase

from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component
from cyclonedx.output import OutputFormat, SchemaVersion, get_instance
from cyclonedx.output.xml import XmlV1Dot3, XmlV1Dot4


class TestOutputGeneric(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls._bom = Bom()
        cls._bom.components.add(Component(name='setuptools'))

    def test_get_instance_default(self) -> None:
        i = get_instance(bom=TestOutputGeneric._bom)
        self.assertIsInstance(i, XmlV1Dot4)

    def test_get_instance_xml_default(self) -> None:
        i = get_instance(bom=TestOutputGeneric._bom, output_format=OutputFormat.XML)
        self.assertIsInstance(i, XmlV1Dot4)

    def test_get_instance_xml_v1_3(self) -> None:
        i = get_instance(bom=TestOutputGeneric._bom, output_format=OutputFormat.XML, schema_version=SchemaVersion.V1_3)
        self.assertIsInstance(i, XmlV1Dot3)

    def test_component_no_version_v1_3(self) -> None:
        i = get_instance(bom=TestOutputGeneric._bom, schema_version=SchemaVersion.V1_3)
        self.assertIsInstance(i, XmlV1Dot3)
