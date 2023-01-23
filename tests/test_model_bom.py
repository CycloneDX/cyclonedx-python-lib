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
from uuid import uuid4

from cyclonedx.model import License, LicenseChoice, OrganizationalContact, OrganizationalEntity, Property
from cyclonedx.model.bom import Bom, BomMetaData, ThisTool, Tool
from cyclonedx.model.bom_ref import BomRef
from cyclonedx.model.component import Component, ComponentType

from .data import (
    get_bom_for_issue_275_components,
    get_bom_with_component_setuptools_with_vulnerability,
    get_component_setuptools_simple,
    get_component_setuptools_simple_no_version,
)


class TestBomMetaData(TestCase):

    def test_empty_bom_metadata(self) -> None:
        metadata = BomMetaData()
        self.assertIsNotNone(metadata.timestamp)
        self.assertIsNotNone(metadata.authors)
        self.assertIsNone(metadata.component)
        self.assertIsNone(metadata.manufacture)
        self.assertIsNone(metadata.supplier)
        self.assertIsNotNone(metadata.licenses)
        self.assertIsNotNone(metadata.properties)
        self.assertIsNotNone(metadata.tools)
        self.assertTrue(ThisTool in metadata.tools)

    def test_basic_bom_metadata(self) -> None:
        tools = [
            Tool(name='tool_1'),
            Tool(name='tool_2'),
        ]
        authors = [
            OrganizationalContact(name='contact_1'),
            OrganizationalContact(name='contact_2'),
        ]
        component = Component(name='test_component')
        manufacturer = OrganizationalEntity(name='test_manufacturer')
        supplier = OrganizationalEntity(name='test_supplier')
        licenses = [
            LicenseChoice(license_=License(id_='MIT')),
            LicenseChoice(license_=License(id_='Apache-2.0')),
        ]
        properties = [
            Property(name='property_1', value='value_1'),
            Property(name='property_2', value='value_2',)
        ]

        metadata = BomMetaData(tools=tools, authors=authors, component=component,
                               manufacture=manufacturer, supplier=supplier, licenses=licenses, properties=properties)
        self.assertIsNotNone(metadata.timestamp)
        self.assertIsNotNone(metadata.authors)
        self.assertTrue(authors[0] in metadata.authors)
        self.assertTrue(authors[1] in metadata.authors)
        self.assertEqual(metadata.component, component)
        self.assertEqual(metadata.manufacture, manufacturer)
        self.assertEqual(metadata.supplier, supplier)
        self.assertIsNotNone(metadata.licenses)
        self.assertTrue(licenses[0] in metadata.licenses)
        self.assertTrue(licenses[1] in metadata.licenses)
        self.assertIsNotNone(metadata.properties)
        self.assertTrue(properties[0] in metadata.properties)
        self.assertTrue(properties[1] in metadata.properties)
        self.assertIsNotNone(metadata.tools)
        self.assertTrue(ThisTool not in metadata.tools)
        self.assertTrue(tools[0] in metadata.tools)
        self.assertTrue(tools[1] in metadata.tools)


class TestBom(TestCase):

    def test_bom_metadata_tool_this_tool(self) -> None:
        self.assertEqual(ThisTool.vendor, 'CycloneDX')
        self.assertEqual(ThisTool.name, 'cyclonedx-python-lib')
        self.assertNotEqual(ThisTool.version, 'UNKNOWN')

    def test_bom_metadata_tool_multiple_tools(self) -> None:
        bom = Bom()
        self.assertEqual(len(bom.metadata.tools), 1)
        bom.metadata.tools.add(
            Tool(vendor='TestVendor', name='TestTool', version='0.0.0')
        )
        self.assertEqual(bom.version, 1)
        self.assertEqual(len(bom.metadata.tools), 2)

    def test_metadata_component(self) -> None:
        metadata = Bom().metadata
        self.assertTrue(metadata.component is None)
        hextech = Component(name='Hextech', version='1.0.0', type_=ComponentType.LIBRARY)
        metadata.component = hextech
        self.assertFalse(metadata.component is None)
        self.assertEqual(metadata.component, hextech)

    def test_empty_bom(self) -> None:
        bom = Bom()
        self.assertEqual(bom.version, 1)
        self.assertIsNotNone(bom.serial_number)
        self.assertIsNotNone(bom.metadata)
        self.assertFalse(bom.components)
        self.assertFalse(bom.services)
        self.assertFalse(bom.external_references)

    def test_empty_bom_defined_serial(self) -> None:
        serial_number = uuid4()
        bom = Bom(serial_number=serial_number)
        self.assertEqual(bom.serial_number, serial_number)
        self.assertEqual(bom.get_urn_uuid(), serial_number.urn)
        self.assertEqual(bom.version, 1)
        self.assertEqual(bom.urn(), f'urn:cdx:{serial_number}/1')

    def test_empty_bom_defined_serial_and_version(self) -> None:
        serial_number = uuid4()
        bom = Bom(serial_number=serial_number, version=2)
        self.assertEqual(bom.serial_number, serial_number)
        self.assertEqual(bom.get_urn_uuid(), serial_number.urn)
        self.assertEqual(bom.version, 2)
        self.assertEqual(bom.urn(), f'urn:cdx:{serial_number}/2')

    def test_bom_with_vulnerabilities(self) -> None:
        bom = get_bom_with_component_setuptools_with_vulnerability()
        self.assertTrue(bom.has_vulnerabilities())

    def test_bom_get_vulnerabilities_by_bom_ref(self) -> None:
        bom = get_bom_with_component_setuptools_with_vulnerability()
        vulns = bom.get_vulnerabilities_for_bom_ref(bom_ref=BomRef(value='pkg:pypi/setuptools@50.3.2?extension=tar.gz'))
        self.assertEqual(len(vulns), 1)

    def test_bom_get_vulnerabilities_by_bom_ref_negative(self) -> None:
        bom = get_bom_with_component_setuptools_with_vulnerability()
        vulns = bom.get_vulnerabilities_for_bom_ref(bom_ref=BomRef(value='pkg:pypi/setuptools@50.3.1?extension=tar.gz'))
        self.assertEqual(len(vulns), 0)

    def test_bom_nested_components_issue_275(self) -> None:
        """regression test for issue #275
        see https://github.com/CycloneDX/cyclonedx-python-lib/issues/275
        """
        bom = get_bom_for_issue_275_components()
        self.assertIsInstance(bom.metadata.component, Component)
        self.assertEqual(2, len(bom.components))
        bom.validate()

    # def test_bom_nested_services_issue_275(self) -> None:
    #    """regression test for issue #275
    #    see https://github.com/CycloneDX/cyclonedx-python-lib/issues/275
    #    """
    #    bom = get_bom_for_issue_275_services()
    #    self.assertIsInstance(bom.metadata.component, Component)
    #    self.assertEqual(2, len(bom.services))
    #    bom.validate()

    def test_has_component_1(self) -> None:
        bom = Bom()
        bom.components.update([get_component_setuptools_simple(), get_component_setuptools_simple_no_version()])
        self.assertEqual(len(bom.components), 2)
        self.assertTrue(bom.has_component(component=get_component_setuptools_simple_no_version()))
        self.assertIsNot(get_component_setuptools_simple(), get_component_setuptools_simple_no_version())

    def test_get_component_by_purl(self) -> None:
        bom = Bom()
        setuptools_simple = get_component_setuptools_simple()
        bom.components.add(setuptools_simple)

        result = bom.get_component_by_purl(get_component_setuptools_simple().purl)

        self.assertIs(result, setuptools_simple)
        self.assertIsNone(bom.get_component_by_purl(get_component_setuptools_simple_no_version().purl))
