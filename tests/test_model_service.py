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
from tests.data import MOCK_UUID_8, MOCK_UUID_9, reorder


class TestModelService(TestCase):

    @patch('cyclonedx.model.service.uuid4', return_value=MOCK_UUID_8)
    def test_minimal_service(self, mock_uuid: Mock) -> None:
        s = Service(name='my-test-service')
        mock_uuid.assert_called()
        self.assertEqual(s.name, 'my-test-service')
        self.assertEqual(str(s.bom_ref), str(MOCK_UUID_8))
        self.assertIsNone(s.provider)
        self.assertIsNone(s.group)
        self.assertIsNone(s.version)
        self.assertIsNone(s.description)
        self.assertFalse(s.endpoints)
        self.assertIsNone(s.authenticated)
        self.assertIsNone(s.x_trust_boundary)
        self.assertFalse(s.data)
        self.assertFalse(s.licenses)
        self.assertFalse(s.external_references)
        self.assertFalse(s.services)
        self.assertFalse(s.release_notes)
        self.assertFalse(s.properties)

    @patch('cyclonedx.model.service.uuid4', return_value=MOCK_UUID_9)
    def test_service_with_services(self, mock_uuid: Mock) -> None:
        parent_service = Service(name='parent-service')
        parent_service.services = [
            Service(name='child-service-1'),
            Service(name='child-service-2')
        ]
        mock_uuid.assert_called()
        self.assertEqual(parent_service.name, 'parent-service')
        self.assertEqual(str(parent_service.bom_ref), str(MOCK_UUID_9))
        self.assertIsNone(parent_service.provider)
        self.assertIsNone(parent_service.group)
        self.assertIsNone(parent_service.version)
        self.assertIsNone(parent_service.description)
        self.assertFalse(parent_service.endpoints)
        self.assertIsNone(parent_service.authenticated)
        self.assertIsNone(parent_service.x_trust_boundary)
        self.assertFalse(parent_service.data)
        self.assertFalse(parent_service.licenses)
        self.assertFalse(parent_service.external_references)
        self.assertIsNotNone(parent_service.services)
        self.assertEqual(len(parent_service.services), 2)
        self.assertIsNone(parent_service.release_notes)
        self.assertFalse(parent_service.properties)
        self.assertTrue(Service(name='child-service-1') in parent_service.services)

    def test_sort(self) -> None:
        # expected sort order: ([group], name, [version])
        expected_order = [0, 1, 3, 4, 2, 5]
        services = [
            Service(name='service-a', group='group-a'),
            Service(name='service-b', group='group-a', version='1.0.0'),
            Service(name='service-c', version='2.0.0'),
            Service(name='service-b', group='group-a'),
            Service(name='service-c', version='1.0.0'),
            Service(name='service-d', ),
        ]
        sorted_services = sorted(services)
        expected_services = reorder(services, expected_order)
        self.assertListEqual(sorted_services, expected_services)
