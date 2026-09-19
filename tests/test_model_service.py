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


from unittest import TestCase

from defusedxml.ElementTree import fromstring as xml_fromstring  # type:ignore[import-untyped]
from sortedcontainers import SortedSet

from cyclonedx.model import DataFlow, XsUri
from cyclonedx.model.contact import OrganizationalContact, OrganizationalEntity
from cyclonedx.model.service import (
    Data,
    DataGovernance,
    OrganizationOrIndividualType,
    Service,
    _DataRepositorySerializationHelper,
)
from tests import reorder


class TestModelService(TestCase):

    def test_minimal_service(self) -> None:
        s = Service(name='my-test-service')
        self.assertEqual(s.name, 'my-test-service')
        self.assertIsNone(s.bom_ref.value)
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

    def test_service_with_services(self) -> None:
        parent_service = Service(name='parent-service')
        parent_service.services = [
            Service(name='child-service-1'),
            Service(name='child-service-2'),
        ]
        self.assertEqual(parent_service.name, 'parent-service')
        self.assertIsNone(parent_service.bom_ref.value)
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

    def test_service_eq_non_service(self) -> None:
        """Service.__eq__ returns False when compared to a non-Service."""
        s = Service(name='svc')
        self.assertNotEqual(s, 'not-a-service')
        self.assertNotEqual(s, 42)
        self.assertNotEqual(s, None)

    def test_service_lt_non_service(self) -> None:
        """Service.__lt__ returns NotImplemented for incompatible types."""
        s = Service(name='svc')
        result = s.__lt__('not-a-service')  # type: ignore[arg-type]
        self.assertIs(result, NotImplemented)

    def test_service_repr(self) -> None:
        s = Service(name='my-svc', group='my-group', version='1.0')
        self.assertIn('my-svc', repr(s))
        self.assertIn('my-group', repr(s))
        self.assertIn('1.0', repr(s))


class TestModelOrganizationOrIndividualType(TestCase):

    def _make_org(self) -> OrganizationalEntity:
        return OrganizationalEntity(name='Acme Corp')

    def _make_contact(self) -> OrganizationalContact:
        return OrganizationalContact(name='Jane Doe')

    def test_with_organization(self) -> None:
        org = self._make_org()
        t = OrganizationOrIndividualType(organization=org)
        self.assertEqual(t.organization, org)
        self.assertIsNone(t.individual)

    def test_with_individual(self) -> None:
        contact = self._make_contact()
        t = OrganizationOrIndividualType(individual=contact)
        self.assertIsNone(t.organization)
        self.assertEqual(t.individual, contact)

    def test_empty(self) -> None:
        t = OrganizationOrIndividualType()
        self.assertIsNone(t.organization)
        self.assertIsNone(t.individual)

    def test_eq_same(self) -> None:
        org = self._make_org()
        a = OrganizationOrIndividualType(organization=org)
        b = OrganizationOrIndividualType(organization=org)
        self.assertEqual(a, b)

    def test_eq_different(self) -> None:
        a = OrganizationOrIndividualType(organization=self._make_org())
        b = OrganizationOrIndividualType(individual=self._make_contact())
        self.assertNotEqual(a, b)

    def test_eq_non_type(self) -> None:
        """__eq__ returns False for non-OrganizationOrIndividualType objects."""
        t = OrganizationOrIndividualType(organization=self._make_org())
        self.assertNotEqual(t, 'not-an-org')
        self.assertNotEqual(t, None)

    def test_lt(self) -> None:
        """OrganizationOrIndividualType.__lt__ orders by comparable tuple."""
        a = OrganizationOrIndividualType(organization=OrganizationalEntity(name='AAA'))
        b = OrganizationOrIndividualType(organization=OrganizationalEntity(name='ZZZ'))
        self.assertLess(a, b)

    def test_lt_non_type(self) -> None:
        """__lt__ returns NotImplemented for incompatible types."""
        t = OrganizationOrIndividualType(organization=self._make_org())
        result = t.__lt__('not-an-org')  # type: ignore[arg-type]
        self.assertIs(result, NotImplemented)

    def test_hash_consistency(self) -> None:
        """Equal objects must have equal hashes."""
        org = self._make_org()
        a = OrganizationOrIndividualType(organization=org)
        b = OrganizationOrIndividualType(organization=org)
        self.assertEqual(hash(a), hash(b))

    def test_sort(self) -> None:
        items = [
            OrganizationOrIndividualType(organization=OrganizationalEntity(name='ZZZ')),
            OrganizationOrIndividualType(organization=OrganizationalEntity(name='AAA')),
        ]
        self.assertEqual(sorted(items)[0].organization.name, 'AAA')  # type: ignore[union-attr]


class TestModelDataGovernance(TestCase):

    def _make_party(self, name: str = 'Acme') -> OrganizationOrIndividualType:
        return OrganizationOrIndividualType(
            organization=OrganizationalEntity(name=name)
        )

    def test_empty(self) -> None:
        g = DataGovernance()
        self.assertFalse(g.custodians)
        self.assertFalse(g.stewards)
        self.assertFalse(g.owners)

    def test_with_all_roles(self) -> None:
        p = self._make_party()
        g = DataGovernance(custodians=[p], stewards=[p], owners=[p])
        self.assertEqual(len(g.custodians), 1)
        self.assertEqual(len(g.stewards), 1)
        self.assertEqual(len(g.owners), 1)

    def test_eq_same(self) -> None:
        p = self._make_party()
        a = DataGovernance(custodians=[p])
        b = DataGovernance(custodians=[p])
        self.assertEqual(a, b)

    def test_eq_different(self) -> None:
        a = DataGovernance(custodians=[self._make_party('A')])
        b = DataGovernance(custodians=[self._make_party('B')])
        self.assertNotEqual(a, b)

    def test_eq_non_type(self) -> None:
        """__eq__ returns False for non-DataGovernance objects."""
        g = DataGovernance(custodians=[self._make_party()])
        self.assertNotEqual(g, 'not-governance')
        self.assertNotEqual(g, None)

    def test_lt(self) -> None:
        """DataGovernance.__lt__ orders by comparable tuple."""
        a = DataGovernance(custodians=[self._make_party('AAA')])
        b = DataGovernance(custodians=[self._make_party('ZZZ')])
        self.assertLess(a, b)

    def test_lt_non_type(self) -> None:
        """__lt__ returns NotImplemented for incompatible types."""
        g = DataGovernance()
        result = g.__lt__('not-governance')  # type: ignore[arg-type]
        self.assertIs(result, NotImplemented)

    def test_hash_consistency(self) -> None:
        p = self._make_party()
        a = DataGovernance(custodians=[p])
        b = DataGovernance(custodians=[p])
        self.assertEqual(hash(a), hash(b))


class TestModelData(TestCase):

    def test_minimal(self) -> None:
        d = Data(flow=DataFlow.INBOUND, classification='public')
        self.assertEqual(d.flow, DataFlow.INBOUND)
        self.assertEqual(d.classification, 'public')
        self.assertIsNone(d.name)
        self.assertIsNone(d.description)
        self.assertIsNone(d.governance)
        self.assertFalse(d.source)
        self.assertFalse(d.destination)

    def test_full(self) -> None:
        gov = DataGovernance(
            custodians=[OrganizationOrIndividualType(organization=OrganizationalEntity(name='Org'))]
        )
        d = Data(
            flow=DataFlow.OUTBOUND,
            classification='confidential',
            name='Credit cards',
            description='PCI data',
            governance=gov,
            source=[XsUri('https://source.example.com')],
            destination=[XsUri('https://dest.example.com')],
        )
        self.assertEqual(d.flow, DataFlow.OUTBOUND)
        self.assertEqual(d.classification, 'confidential')
        self.assertEqual(d.name, 'Credit cards')
        self.assertEqual(d.description, 'PCI data')
        self.assertEqual(d.governance, gov)
        self.assertEqual(len(d.source), 1)
        self.assertEqual(len(d.destination), 1)

    def test_eq_same(self) -> None:
        a = Data(flow=DataFlow.INBOUND, classification='public')
        b = Data(flow=DataFlow.INBOUND, classification='public')
        self.assertEqual(a, b)

    def test_eq_different_flow(self) -> None:
        a = Data(flow=DataFlow.INBOUND, classification='public')
        b = Data(flow=DataFlow.OUTBOUND, classification='public')
        self.assertNotEqual(a, b)

    def test_eq_non_type(self) -> None:
        """Data.__eq__ returns False for non-Data objects."""
        d = Data(flow=DataFlow.INBOUND, classification='public')
        self.assertNotEqual(d, 'not-data')
        self.assertNotEqual(d, None)

    def test_lt(self) -> None:
        a = Data(flow=DataFlow.INBOUND, classification='aaa')
        b = Data(flow=DataFlow.INBOUND, classification='zzz')
        self.assertLess(a, b)

    def test_lt_non_type(self) -> None:
        """Data.__lt__ returns NotImplemented for incompatible types."""
        d = Data(flow=DataFlow.INBOUND, classification='public')
        result = d.__lt__('not-data')  # type: ignore[arg-type]
        self.assertIs(result, NotImplemented)

    def test_hash_consistency(self) -> None:
        a = Data(flow=DataFlow.INBOUND, classification='public')
        b = Data(flow=DataFlow.INBOUND, classification='public')
        self.assertEqual(hash(a), hash(b))

    def test_repr(self) -> None:
        d = Data(flow=DataFlow.OUTBOUND, classification='restricted')
        r = repr(d)
        # The repr includes the flow enum and classification; the exact string for the enum
        # varies by Python version (e.g. 'outbound' on 3.9, 'DataFlow.OUTBOUND' on 3.12+),
        # but 'OUTBOUND' is always a substring of either representation.
        self.assertIn('OUTBOUND', r.upper())
        self.assertIn('restricted', r)

    def test_sort(self) -> None:
        items = [
            Data(flow=DataFlow.INBOUND, classification='zzz'),
            Data(flow=DataFlow.INBOUND, classification='aaa'),
        ]
        self.assertEqual(sorted(items)[0].classification, 'aaa')

    def test_setters(self) -> None:
        d = Data(flow=DataFlow.INBOUND, classification='public')
        gov = DataGovernance()
        d.flow = DataFlow.OUTBOUND
        d.classification = 'private'
        d.name = 'new name'
        d.description = 'new desc'
        d.governance = gov
        d.source = [XsUri('https://a.example.com')]
        d.destination = [XsUri('https://b.example.com')]
        self.assertEqual(d.flow, DataFlow.OUTBOUND)
        self.assertEqual(d.classification, 'private')
        self.assertEqual(d.name, 'new name')
        self.assertEqual(d.description, 'new desc')
        self.assertEqual(d.governance, gov)
        self.assertEqual(len(d.source), 1)
        self.assertEqual(len(d.destination), 1)


class TestDataRepositorySerializationHelper(TestCase):
    """Direct tests for the non-public serialization helper."""

    def test_json_normalize_empty_returns_none(self) -> None:
        """json_normalize returns None for an empty set (defensive early-exit)."""
        result = _DataRepositorySerializationHelper.json_normalize(SortedSet(), view=None)
        self.assertIsNone(result)

    def test_xml_normalize_empty_returns_none(self) -> None:
        """xml_normalize returns None for an empty set (defensive early-exit)."""
        result = _DataRepositorySerializationHelper.xml_normalize(
            SortedSet(), element_name='data', view=None, xmlns=None
        )
        self.assertIsNone(result)

    def test_xml_denormalize_legacy_classification_tag(self) -> None:
        """xml_denormalize handles CDX 1.2-1.4 flat <classification flow='...'> elements."""
        # CDX 1.2-1.4 format: <data><classification flow="outbound">public</classification></data>
        xml_str = '<data><classification flow="outbound">public</classification></data>'
        elem = xml_fromstring(xml_str)
        result = _DataRepositorySerializationHelper.xml_denormalize(elem, default_ns=None)
        self.assertEqual(len(result), 1)
        item = next(iter(result))
        self.assertEqual(item.flow, DataFlow.OUTBOUND)
        self.assertEqual(item.classification, 'public')

    def test_xml_denormalize_legacy_classification_tag_with_namespace(self) -> None:
        """xml_denormalize handles CDX 1.2-1.4 flat <classification> with namespace."""
        ns = 'http://cyclonedx.org/schema/bom/1.3'
        xml_str = (
            f'<data xmlns="{ns}">'
            f'<classification flow="outbound">confidential</classification>'
            f'</data>'
        )
        elem = xml_fromstring(xml_str)
        result = _DataRepositorySerializationHelper.xml_denormalize(elem, default_ns=ns)
        self.assertEqual(len(result), 1)
        item = next(iter(result))
        self.assertEqual(item.flow, DataFlow.OUTBOUND)
        self.assertEqual(item.classification, 'confidential')
