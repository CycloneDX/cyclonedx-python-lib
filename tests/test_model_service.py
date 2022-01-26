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
from unittest.mock import Mock, patch

from cyclonedx.model.service import Service


class TestModelService(TestCase):

    @patch('cyclonedx.model.service.uuid4', return_value='77d15ab9-5602-4cca-8ed2-59ae579aafd3')
    def test_minimal_service(self, mock_uuid: Mock) -> None:
        s = Service(name='my-test-service')
        mock_uuid.assert_called()
        self.assertEqual(s.name, 'my-test-service')
        self.assertEqual(s.bom_ref, '77d15ab9-5602-4cca-8ed2-59ae579aafd3')
        self.assertIsNone(s.provider)
        self.assertIsNone(s.group)
        self.assertIsNone(s.version)
        self.assertIsNone(s.description)
        self.assertIsNone(s.endpoints)
        self.assertIsNone(s.authenticated)
        self.assertIsNone(s.x_trust_boundary)
        self.assertIsNone(s.data)
        self.assertListEqual(s.licenses, [])
        self.assertListEqual(s.external_references, [])
        self.assertIsNone(s.release_notes)
        self.assertIsNone(s.properties)
