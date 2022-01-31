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
from typing import List
from unittest import TestCase
from unittest.mock import Mock, patch

from cyclonedx.model import ExternalReference, ExternalReferenceType, Property
from cyclonedx.model.component import Component, ComponentType


class TestModelComponent(TestCase):

    @patch('cyclonedx.model.component.uuid4', return_value='6f266d1c-760f-4552-ae3b-41a9b74232fa')
    def test_empty_basic_component(self, mock_uuid: Mock) -> None:
        c = Component(
            name='test-component', version='1.2.3'
        )
        mock_uuid.assert_called()
        self.assertEqual(c.name, 'test-component')
        self.assertEqual(c.type, ComponentType.LIBRARY)
        self.assertIsNone(c.mime_type)
        self.assertEqual(c.bom_ref, '6f266d1c-760f-4552-ae3b-41a9b74232fa')
        self.assertIsNone(c.supplier)
        self.assertIsNone(c.author)
        self.assertIsNone(c.publisher)
        self.assertIsNone(c.group)
        self.assertEqual(c.version, '1.2.3')
        self.assertIsNone(c.description)
        self.assertIsNone(c.scope)
        self.assertListEqual(c.hashes, [])
        self.assertListEqual(c.licenses, [])
        self.assertIsNone(c.copyright)
        self.assertIsNone(c.purl)
        self.assertListEqual(c.external_references, [])
        self.assertIsNone(c.properties)
        self.assertIsNone(c.release_notes)

        self.assertEqual(len(c.get_vulnerabilities()), 0)

    @patch('cyclonedx.model.component.uuid4', return_value='6f266d1c-760f-4552-ae3b-41a9b74232fa')
    def test_multiple_basic_components(self, mock_uuid: Mock) -> None:
        c1 = Component(
            name='test-component', version='1.2.3'
        )
        self.assertEqual(c1.name, 'test-component')
        self.assertEqual(c1.version, '1.2.3')
        self.assertEqual(c1.type, ComponentType.LIBRARY)
        self.assertEqual(len(c1.external_references), 0)
        self.assertEqual(len(c1.hashes), 0)
        self.assertEqual(len(c1.get_vulnerabilities()), 0)

        c2 = Component(
            name='test2-component', version='3.2.1'
        )
        self.assertEqual(c2.name, 'test2-component')
        self.assertEqual(c2.version, '3.2.1')
        self.assertEqual(c2.type, ComponentType.LIBRARY)
        self.assertEqual(len(c2.external_references), 0)
        self.assertEqual(len(c2.hashes), 0)
        self.assertEqual(len(c2.get_vulnerabilities()), 0)

        self.assertNotEqual(c1, c2)

        mock_uuid.assert_called()

    def test_external_references(self) -> None:
        c = Component(
            name='test-component', version='1.2.3'
        )
        c.add_external_reference(ExternalReference(
            reference_type=ExternalReferenceType.OTHER,
            url='https://cyclonedx.org',
            comment='No comment'
        ))
        self.assertEqual(c.name, 'test-component')
        self.assertEqual(c.version, '1.2.3')
        self.assertEqual(c.type, ComponentType.LIBRARY)
        self.assertEqual(len(c.external_references), 1)
        self.assertEqual(len(c.hashes), 0)
        self.assertEqual(len(c.get_vulnerabilities()), 0)

        c2 = Component(
            name='test2-component', version='3.2.1'
        )
        self.assertEqual(c2.name, 'test2-component')
        self.assertEqual(c2.version, '3.2.1')
        self.assertEqual(c2.type, ComponentType.LIBRARY)
        self.assertEqual(len(c2.external_references), 0)
        self.assertEqual(len(c2.hashes), 0)
        self.assertEqual(len(c2.get_vulnerabilities()), 0)

    def test_empty_basic_component_no_version(self) -> None:
        c = Component(
            name='test-component'
        )
        self.assertEqual(c.name, 'test-component')
        self.assertIsNone(c.version, None)
        self.assertEqual(c.type, ComponentType.LIBRARY)
        self.assertEqual(len(c.external_references), 0)
        self.assertEqual(len(c.hashes), 0)
        self.assertEqual(len(c.get_vulnerabilities()), 0)

    def test_component_equal_1(self) -> None:
        c = Component(
            name='test-component', version='1.2.3'
        )
        c.add_external_reference(ExternalReference(
            reference_type=ExternalReferenceType.OTHER,
            url='https://cyclonedx.org',
            comment='No comment'
        ))

        c2 = Component(
            name='test-component', version='1.2.3'
        )
        c2.add_external_reference(ExternalReference(
            reference_type=ExternalReferenceType.OTHER,
            url='https://cyclonedx.org',
            comment='No comment'
        ))

        self.assertEqual(c, c2)

    def test_component_equal_2(self) -> None:
        props: List[Property] = [
            Property(name='prop1', value='val1'),
            Property(name='prop2', value='val2')
        ]

        c = Component(
            name='test-component', version='1.2.3', properties=props
        )
        c2 = Component(
            name='test-component', version='1.2.3', properties=props
        )

        self.assertEqual(c, c2)

    def test_component_equal_3(self) -> None:
        c = Component(
            name='test-component', version='1.2.3', properties=[
                Property(name='prop1', value='val1'),
                Property(name='prop2', value='val2')
            ]
        )
        c2 = Component(
            name='test-component', version='1.2.3', properties=[
                Property(name='prop3', value='val3'),
                Property(name='prop4', value='val4')
            ]
        )

        self.assertNotEqual(c, c2)
