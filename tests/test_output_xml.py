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


from typing import Callable
from unittest import TestCase
from unittest.mock import Mock, patch

from ddt import ddt, idata, named_data, unpack

from cyclonedx.model.bom import Bom
from cyclonedx.output.xml import BY_SCHEMA_VERSION, Xml
from cyclonedx.schema import SchemaVersion, OutputFormat

from tests import SnapshotCompareMixin
from tests._data.models import all_get_bom_funct_valid, uuid_generator

from cyclonedx.validation.xml import XmlValidator


@ddt
@patch('cyclonedx.model.ThisTool._version', 'TESTING')
@patch('cyclonedx.model.component.uuid4', side_effect=uuid_generator(0))
@patch('cyclonedx.model.service.uuid4', side_effect=uuid_generator(2 ** 32))
class TestOutputXml(TestCase, SnapshotCompareMixin):

    @named_data(*(
        (f'{n}-{sv.to_version()}', gb, sv) for n, gb in all_get_bom_funct_valid for sv in SchemaVersion
    ))
    @unpack
    def test(self, get_bom: Callable[[], Bom], sv: SchemaVersion, *_, **__) -> None:
        bom = get_bom()
        xml = BY_SCHEMA_VERSION[sv](bom).output_as_string(indent=2)
        errors = XmlValidator(sv).validate_str(xml)
        self.assertIsNone(errors)
        self.assertEqualSnapshot(xml, f'{self.__class__.__name__}-{get_bom.__name__}-{sv.to_version()}.xml')




@ddt
class TestFunctionalBySchemaVersion(TestCase):

    @idata(SchemaVersion)
    def test_get_outputter_expected(self, sv: SchemaVersion) -> None:
        outputterClass = BY_SCHEMA_VERSION[sv]
        self.assertTrue(issubclass(outputterClass, Xml))
        outputter = outputterClass(Mock(spec=Bom))
        self.assertIs(outputter.schema_version, sv)
        self.assertIs(outputter.output_format, OutputFormat.XML)
