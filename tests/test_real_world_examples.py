# This file is part of CycloneDX Python Library
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
from json import loads as json_loads
from os.path import join
from typing import Any
from unittest.mock import patch

from cyclonedx.model.bom import Bom
from tests import OWN_DATA_DIRECTORY


@patch('cyclonedx.builder.this.__ThisVersion', 'TESTING')
@patch('cyclonedx.model.bom._get_now_utc', return_value=datetime.fromisoformat('2023-01-07 13:44:32.312678+00:00'))
class TestDeserializeRealWorldExamples(unittest.TestCase):

    def test_webgoat_6_1(self, *_: Any, **__: Any) -> None:
        with open(join(OWN_DATA_DIRECTORY, 'xml', '1.4', 'webgoat-6.1.xml')) as input_xml:
            Bom.from_xml(input_xml)

    def test_regression_issue_630(self, *_: Any, **__: Any) -> None:
        with open(join(OWN_DATA_DIRECTORY, 'xml', '1.6', 'regression_issue630.xml')) as input_xml:
            Bom.from_xml(input_xml)

    def test_regression_issue677(self, *_: Any, **__: Any) -> None:
        # tests https://github.com/CycloneDX/cyclonedx-python-lib/issues/677
        with open(join(OWN_DATA_DIRECTORY, 'json', '1.5', 'issue677.json')) as input_json:
            json = json_loads(input_json.read())
        bom = Bom.from_json(json)
        self.assertEqual(4, len(bom.components))
        bom.validate()

    def test_regression_issue753(self, *_: Any, **__: Any) -> None:
        # tests https://github.com/CycloneDX/cyclonedx-python-lib/issues/753
        with open(join(OWN_DATA_DIRECTORY, 'json', '1.5', 'issue753.json')) as input_json:
            json = json_loads(input_json.read())
        bom = Bom.from_json(json)
        self.assertEqual(2, len(bom.components))
        bom.validate()
