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
import warnings
from typing import Callable, Tuple
from unittest import TestCase
from uuid import uuid4

from ddt import ddt, named_data

from cyclonedx.exception.model import LicenseExpressionAlongWithOthersException
from cyclonedx.model import Property
from cyclonedx.model.bom import Bom, BomMetaData
from cyclonedx.model.bom_ref import BomRef
from cyclonedx.model.component import Component, ComponentType
from cyclonedx.model.contact import OrganizationalContact, OrganizationalEntity
from cyclonedx.model.license import DisjunctiveLicense
from cyclonedx.model.lifecycle import LifecyclePhase, NamedLifecycle, PredefinedLifecycle
from cyclonedx.model.tool import Tool
from cyclonedx.output.json import JsonV1Dot6
from tests._data.models import (
    get_bom_component_licenses_invalid,
    get_bom_component_nested_licenses_invalid,
    get_bom_for_issue_275_components,
    get_bom_metadata_component_licenses_invalid,
    get_bom_metadata_component_nested_licenses_invalid,
    get_bom_metadata_licenses_invalid,
    get_bom_service_licenses_invalid,
    get_bom_with_component_setuptools_with_vulnerability,
    get_component_setuptools_simple,
    get_component_setuptools_simple_no_version,
)


class TestBomMetaData(TestCase):

    def test_empty_bom_metadata(self) -> None:
        metadata = BomMetaData()
        self.assertIsNotNone(metadata.timestamp)
        self.assertEqual(0, len(metadata.authors))
        self.assertIsNone(metadata.component)
        self.assertIsNone(metadata.manufacture)
        self.assertIsNone(metadata.supplier)
        self.assertEqual(0, len(metadata.licenses))
        self.assertEqual(0, len(metadata.lifecycles))
        self.assertEqual(0, len(metadata.properties))
        self.assertEqual(0, len(metadata.tools))

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
            DisjunctiveLicense(id='MIT'),
            DisjunctiveLicense(id='Apache-2.0'),
        ]
        lifecycles = [
            PredefinedLifecycle(phase=LifecyclePhase.BUILD),
            NamedLifecycle(name='named_lifecycle', description='test'),
        ]
        properties = [
            Property(name='property_1', value='value_1'),
            Property(name='property_2', value='value_2', )
        ]

        metadata = BomMetaData(tools=tools, authors=authors, component=component, lifecycles=lifecycles,
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
        self.assertIsNotNone(metadata.lifecycles)
        self.assertTrue(lifecycles[0] in metadata.lifecycles)
        self.assertTrue(lifecycles[1] in metadata.lifecycles)
        self.assertIsNotNone(metadata.properties)
        self.assertTrue(properties[0] in metadata.properties)
        self.assertTrue(properties[1] in metadata.properties)
        self.assertIsNotNone(metadata.tools)
        self.assertEqual(2, len(metadata.tools.tools))
        self.assertTrue(tools[0] in metadata.tools.tools)
        self.assertTrue(tools[1] in metadata.tools.tools)


@ddt
class TestBom(TestCase):

    def test_bom_metadata_tool_multiple_tools(self) -> None:
        bom = Bom()
        self.assertEqual(len(bom.metadata.tools), 0)
        bom.metadata.tools.tools.add(
            Tool(vendor='TestVendor', name='TestTool', version='0.0.0')
        )
        bom.metadata.tools.tools.add(
            Tool(vendor='TestVendor', name='TestTool-2', version='1.33.7')
        )
        self.assertEqual(len(bom.metadata.tools), 2)

    def test_metadata_component(self) -> None:
        metadata = Bom().metadata
        self.assertTrue(metadata.component is None)
        hextech = Component(name='Hextech', version='1.0.0', type=ComponentType.LIBRARY)
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

    def test_root_component_only_bom(self) -> None:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            bom = Bom(metadata=BomMetaData(component=Component(name='test', version='1.2')))
            _ = JsonV1Dot6(bom).output_as_string()
            self.assertEqual(len(w), 0)

    def test_warning_missing_dependency(self) -> None:
        with self.assertWarns(expected_warning=UserWarning) as w:
            bom = Bom(metadata=BomMetaData(component=Component(name='root_component', version='1.2')))
            bom.components.add(Component(name='test2', version='4.2'))
            _ = JsonV1Dot6(bom).output_as_string()
            self.assertEqual(len(w.warnings), 1)
            self.assertIn('has no defined dependencies ', str(w.warnings[0]))

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

    @named_data(
        ['metadata_licenses', get_bom_metadata_licenses_invalid],
        ['metadata_component_licenses', get_bom_metadata_component_licenses_invalid],
        ['metadata_component_nested_licenses', get_bom_metadata_component_nested_licenses_invalid],
        ['component_licenses', get_bom_component_licenses_invalid],
        ['component_nested_licenses', get_bom_component_nested_licenses_invalid],
        ['service_licenses', get_bom_service_licenses_invalid],
    )
    def test_validate_with_invalid_license_constellation_throws(self, get_bom: Callable[[], Bom]) -> None:
        bom = get_bom()
        with self.assertRaises(LicenseExpressionAlongWithOthersException):
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

    @named_data(
        ('none', tuple()),
        # a = anonymous - bom-ref auto-set
        # k = known - has bom-ref.value set
        # d = known duplicate - has bom-ref.value set same as another
        ('A(a), B(a)', ((Component(name='A'), tuple()),
                        (Component(name='B'), tuple()))),
        ('A(k), B(k)', ((Component(name='A', bom_ref='A'), tuple()),
                        (Component(name='B', bom_ref='B'), tuple()))),
        ('A(a) {A1(a)}, B(a) {B1(a)}', ((Component(name='A'), (Component(name='A1'),)),
                                        (Component(name='B'), (Component(name='B1'),)))),
        ('A(k) {A1(a)}', ((Component(name='A', bom_ref='A'), (Component(name='1'),)),)),
        ('A(a) {A1(a), A2(a)}', ((Component(name='A'), (Component(name='A1'), Component(name='A2'))),)),
        ('A(a) {A1(k)}', ((Component(name='A'), (Component(name='B', bom_ref='A1'),)),)),
        ('A(k) {A1(k)}', ((Component(name='A', bom_ref='A'), (Component(name='A1', bom_ref='A1'),)),)),
        ('A(d) {A1(d)}', ((Component(name='A', bom_ref='D'), (Component(name='B', bom_ref='D'),)),)),
        ('duplicate name(a)', ((Component(name='A'), tuple()),
                               (Component(name='A'), tuple()),)),
        ('duplicate name(k)', ((Component(name='A', bom_ref='A1'), tuple()),
                               (Component(name='A', bom_ref='A2'), tuple()))),
    )
    def test_register_dependency(self, dependencies: Tuple[Tuple[Component, Tuple[Component, ...]], ...]) -> None:
        bom = Bom()
        for d1, d2 in dependencies:
            bom.components.update((d1,), d2)
            bom.register_dependency(d1, d2)
        bom_deps = tuple(bom.dependencies)
        for d1, d2 in dependencies:
            bom_dep = next((bd for bd in bom_deps if bd.ref is d1.bom_ref), None)
            self.assertIsNotNone(bom_dep, f'missing {d1.bom_ref!r} in {bom_deps!r}')
            self.assertEqual(len(d2), len(bom_dep.dependencies))
            for dd in d2:
                self.assertIn(dd.bom_ref, bom_dep.dependencies_as_bom_refs())

    def test_regression_issue_539(self) -> None:
        """regression test for issue #539
        see https://github.com/CycloneDX/cyclonedx-python-lib/issues/539
        """
        # for showcasing purposes, bom-ref values MUST NOT be set
        bom = Bom()
        bom.metadata.component = root_component = Component(
            name='myApp',
            type=ComponentType.APPLICATION,
        )
        component1 = Component(
            type=ComponentType.LIBRARY,
            name='some-component',
        )
        component2 = Component(
            type=ComponentType.LIBRARY,
            name='some-library',
        )
        component3 = Component(
            type=ComponentType.LIBRARY,
            name='another-library',
        )
        bom.components.add(component1)
        bom.components.add(component2)
        bom.components.add(component3)
        bom.register_dependency(root_component, [component1])
        bom.register_dependency(component1, [component2])
        bom.register_dependency(root_component, [component3])
        # region assert root_component
        d = next((d for d in bom.dependencies if d.ref is root_component.bom_ref), None)
        self.assertIsNotNone(d, f'missing {root_component.bom_ref!r} in {bom.dependencies!r}')
        self.assertEqual(2, len(d.dependencies))
        self.assertIn(d.dependencies[0].ref, (component1.bom_ref, component3.bom_ref))
        self.assertIn(d.dependencies[1].ref, (component1.bom_ref, component3.bom_ref))
        # endregion assert root_component
        # region assert component1
        d = next((d for d in bom.dependencies if d.ref is component1.bom_ref), None)
        self.assertIsNotNone(d, f'missing {component1.bom_ref!r} in {bom.dependencies!r}')
        self.assertEqual(1, len(d.dependencies))
        self.assertIs(component2.bom_ref, d.dependencies[0].ref)
        # endregion assert component1
