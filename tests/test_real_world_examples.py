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
import unittest
from datetime import datetime
from os.path import dirname, join
from typing import cast
from unittest.mock import patch
from xml.etree import ElementTree

from cyclonedx.model.bom import Bom
from cyclonedx.schema import SchemaVersion


def fixed_date_time() -> datetime:
    return datetime.fromisoformat('2023-01-07 13:44:32.312678+00:00')


@patch('cyclonedx.model.ThisTool._version', 'TESTING')
@patch('cyclonedx.model.bom.get_now_utc', fixed_date_time)
class TestDeserializeeRealWorldExamples(unittest.TestCase):

    def test_webgoat_6_1(self) -> None:
        self._attempt_load_example(
            schema_version=SchemaVersion.V1_4, fixture='webgoat-6.1.xml'
        )

    def _attempt_load_example(self, schema_version: SchemaVersion, fixture: str) -> None:
        with open(join(dirname(__file__), f'fixtures/xml/{schema_version.to_version()}/{fixture}')) as input_xml:
            xml = input_xml.read()
            cast(Bom, Bom.from_xml(data=ElementTree.fromstring(xml)))
