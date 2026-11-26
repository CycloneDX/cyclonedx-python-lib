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

from cyclonedx.exception.model import InvalidValueException, MutuallyExclusivePropertiesException
from cyclonedx.model import AttachedText, Property, XsUri
from cyclonedx.model.bom_ref import BomRef
from cyclonedx.model.contact import OrganizationalContact, OrganizationalEntity
from cyclonedx.model.data import (
    ComponentData,
    ComponentDataKind,
    DataContents,
    DataGovernance,
    DataGovernanceResponsibleParty,
    DatasetReference,
)
from cyclonedx.model.graphics import Graphic, GraphicsCollection
from tests import reorder


class TestComponentDataKind(TestCase):

    def test_all_values_exist(self) -> None:
        self.assertEqual(
            {
                ComponentDataKind.SOURCE_CODE.value,
                ComponentDataKind.CONFIGURATION.value,
                ComponentDataKind.DATASET.value,
                ComponentDataKind.DEFINITION.value,
                ComponentDataKind.OTHER.value,
            },
            {
                'source-code',
                'configuration',
                'dataset',
                'definition',
                'other',
            },
        )


class TestDataContents(TestCase):

    def test_defaults(self) -> None:
        obj = DataContents()

        self.assertIsNone(obj.attachment)
        self.assertIsNone(obj.url)
        self.assertEqual(len(obj.properties), 0)

    def test_constructor(self) -> None:
        attachment = AttachedText(content='dGVzdA==')
        url = XsUri('https://example.org/dataset.csv')
        prop = Property(name='format', value='csv')

        obj = DataContents(
            attachment=attachment,
            url=url,
            properties=[prop],
        )

        self.assertEqual(obj.attachment, attachment)
        self.assertEqual(obj.url, url)
        self.assertIn(prop, obj.properties)

    def test_property_setters(self) -> None:
        obj = DataContents()

        attachment = AttachedText(content='dGVzdA==')
        url = XsUri('https://example.org/dataset.csv')
        obj.attachment = attachment
        obj.url = url

        self.assertEqual(obj.attachment, attachment)
        self.assertEqual(obj.url, url)

    def test_sorted_properties(self) -> None:
        prop_a = Property(name='a', value='1')
        prop_b = Property(name='b', value='2')

        obj = DataContents(properties=[prop_b, prop_a])

        self.assertEqual(
            list(obj.properties),
            [prop_a, prop_b],
        )

    def test_equality(self) -> None:
        self.assertEqual(
            DataContents(url=XsUri('https://example.org/a.csv')),
            DataContents(url=XsUri('https://example.org/a.csv')),
        )

    def test_inequality(self) -> None:
        self.assertNotEqual(
            DataContents(url=XsUri('https://example.org/a.csv')),
            DataContents(url=XsUri('https://example.org/b.csv')),
        )

    def test_comparison(self) -> None:
        first = DataContents(url=XsUri('https://example.org/a.csv'))
        second = DataContents(url=XsUri('https://example.org/b.csv'))

        self.assertTrue(first < second)

    def test_hash(self) -> None:
        self.assertEqual(
            hash(DataContents(url=XsUri('https://example.org/a.csv'))),
            hash(DataContents(url=XsUri('https://example.org/a.csv'))),
        )

    def test_repr(self) -> None:
        self.assertEqual(
            repr(DataContents()),
            '<DataContents attachment=False url=False>',
        )


class TestDataGovernanceResponsibleParty(TestCase):

    def test_requires_organization_or_contact(self) -> None:
        with self.assertRaises(MutuallyExclusivePropertiesException):
            DataGovernanceResponsibleParty()

    def test_organization_and_contact_are_mutually_exclusive(self) -> None:
        with self.assertRaises(MutuallyExclusivePropertiesException):
            DataGovernanceResponsibleParty(
                organization=OrganizationalEntity(name='DataCorp'),
                contact=OrganizationalContact(name='Jane Doe'),
            )

    def test_constructor_organization(self) -> None:
        org = OrganizationalEntity(name='DataCorp')

        obj = DataGovernanceResponsibleParty(organization=org)

        self.assertEqual(obj.organization, org)
        self.assertIsNone(obj.contact)

    def test_constructor_contact(self) -> None:
        contact = OrganizationalContact(name='Jane Doe')

        obj = DataGovernanceResponsibleParty(contact=contact)

        self.assertEqual(obj.contact, contact)
        self.assertIsNone(obj.organization)

    def test_property_setters(self) -> None:
        org = OrganizationalEntity(name='DataCorp')
        contact = OrganizationalContact(name='Jane Doe')
        obj = DataGovernanceResponsibleParty(organization=org)

        with self.assertRaises(MutuallyExclusivePropertiesException):
            obj.contact = contact
        self.assertIsNone(obj.contact)

        # switching is possible by unsetting first
        obj.organization = None
        obj.contact = contact
        self.assertIsNone(obj.organization)
        self.assertEqual(obj.contact, contact)

    def test_equality(self) -> None:
        org = OrganizationalEntity(name='DataCorp')

        self.assertEqual(
            DataGovernanceResponsibleParty(organization=org),
            DataGovernanceResponsibleParty(organization=OrganizationalEntity(name='DataCorp')),
        )

    def test_inequality(self) -> None:
        self.assertNotEqual(
            DataGovernanceResponsibleParty(organization=OrganizationalEntity(name='DataCorp')),
            DataGovernanceResponsibleParty(contact=OrganizationalContact(name='Jane Doe')),
        )

    def test_comparison(self) -> None:
        first = DataGovernanceResponsibleParty(organization=OrganizationalEntity(name='A'))
        second = DataGovernanceResponsibleParty(organization=OrganizationalEntity(name='B'))

        self.assertTrue(first < second)

    def test_hash(self) -> None:
        org = OrganizationalEntity(name='DataCorp')

        self.assertEqual(
            hash(DataGovernanceResponsibleParty(organization=org)),
            hash(DataGovernanceResponsibleParty(organization=OrganizationalEntity(name='DataCorp'))),
        )

    def test_repr(self) -> None:
        self.assertEqual(
            repr(DataGovernanceResponsibleParty(organization=OrganizationalEntity(name='DataCorp'))),
            '<DataGovernanceResponsibleParty organization=True contact=False>',
        )


class TestDataGovernance(TestCase):

    def test_defaults(self) -> None:
        obj = DataGovernance()

        self.assertEqual(len(obj.custodians), 0)
        self.assertEqual(len(obj.stewards), 0)
        self.assertEqual(len(obj.owners), 0)

    def test_constructor(self) -> None:
        custodian = DataGovernanceResponsibleParty(organization=OrganizationalEntity(name='Custodian'))
        steward = DataGovernanceResponsibleParty(organization=OrganizationalEntity(name='Steward'))
        owner = DataGovernanceResponsibleParty(organization=OrganizationalEntity(name='Owner'))

        obj = DataGovernance(
            custodians=[custodian],
            stewards=[steward],
            owners=[owner],
        )

        self.assertIn(custodian, obj.custodians)
        self.assertIn(steward, obj.stewards)
        self.assertIn(owner, obj.owners)

    def test_sorted_owners(self) -> None:
        owner_a = DataGovernanceResponsibleParty(organization=OrganizationalEntity(name='A'))
        owner_b = DataGovernanceResponsibleParty(organization=OrganizationalEntity(name='B'))

        obj = DataGovernance(owners=[owner_b, owner_a])

        self.assertEqual(
            list(obj.owners),
            [owner_a, owner_b],
        )

    def test_equality(self) -> None:
        self.assertEqual(
            DataGovernance(),
            DataGovernance(),
        )

    def test_comparison(self) -> None:
        self.assertTrue(
            DataGovernance() <= DataGovernance()
        )

    def test_hash(self) -> None:
        self.assertEqual(
            hash(DataGovernance()),
            hash(DataGovernance()),
        )

    def test_repr(self) -> None:
        self.assertEqual(
            repr(DataGovernance()),
            '<DataGovernance custodians=0 stewards=0 owners=0>',
        )


class TestComponentData(TestCase):

    def test_defaults(self) -> None:
        obj = ComponentData(type=ComponentDataKind.DATASET)

        self.assertEqual(obj.type, ComponentDataKind.DATASET)
        self.assertIsNone(obj.name)
        self.assertIsNone(obj.contents)
        self.assertIsNone(obj.classification)
        self.assertEqual(len(obj.sensitive_data), 0)
        self.assertIsNone(obj.graphics)
        self.assertIsNone(obj.description)
        self.assertIsNone(obj.governance)
        self.assertIsNone(obj.bom_ref.value)

    def test_constructor(self) -> None:
        contents = DataContents(url=XsUri('https://example.org/dataset.csv'))
        graphics = GraphicsCollection(collection=[Graphic(name='chart')])
        governance = DataGovernance(
            owners=[DataGovernanceResponsibleParty(organization=OrganizationalEntity(name='DataCorp'))]
        )

        obj = ComponentData(
            type=ComponentDataKind.DATASET,
            name='example-dataset',
            contents=contents,
            classification='public',
            sensitive_data=['PII'],
            graphics=graphics,
            description='Sample dataset',
            governance=governance,
            bom_ref='data-1',
        )

        self.assertEqual(obj.type, ComponentDataKind.DATASET)
        self.assertEqual(obj.name, 'example-dataset')
        self.assertEqual(obj.contents, contents)
        self.assertEqual(obj.classification, 'public')
        self.assertIn('PII', obj.sensitive_data)
        self.assertEqual(obj.graphics, graphics)
        self.assertEqual(obj.description, 'Sample dataset')
        self.assertEqual(obj.governance, governance)
        self.assertEqual(obj.bom_ref.value, 'data-1')

    def test_property_setters(self) -> None:
        obj = ComponentData(type=ComponentDataKind.DATASET)

        obj.type = ComponentDataKind.CONFIGURATION
        obj.name = 'renamed'
        obj.classification = 'internal'
        obj.description = 'updated description'

        self.assertEqual(obj.type, ComponentDataKind.CONFIGURATION)
        self.assertEqual(obj.name, 'renamed')
        self.assertEqual(obj.classification, 'internal')
        self.assertEqual(obj.description, 'updated description')

    def test_sorted_sensitive_data(self) -> None:
        obj = ComponentData(type=ComponentDataKind.DATASET, sensitive_data=['PII', 'PHI'])

        self.assertEqual(
            list(obj.sensitive_data),
            sorted(['PII', 'PHI']),
        )

    def test_sort(self) -> None:
        expected_order = [1, 0]
        items = [
            ComponentData(type=ComponentDataKind.DATASET, name='b'),
            ComponentData(type=ComponentDataKind.DATASET, name='a'),
        ]
        expected_items = reorder(items, expected_order)
        sorted_items = sorted(items)
        self.assertListEqual(sorted_items, expected_items)

    def test_equality(self) -> None:
        self.assertEqual(
            ComponentData(type=ComponentDataKind.DATASET, name='a'),
            ComponentData(type=ComponentDataKind.DATASET, name='a'),
        )

    def test_inequality(self) -> None:
        self.assertNotEqual(
            ComponentData(type=ComponentDataKind.DATASET, name='a'),
            ComponentData(type=ComponentDataKind.DATASET, name='b'),
        )

    def test_comparison(self) -> None:
        first = ComponentData(type=ComponentDataKind.DATASET, name='a')
        second = ComponentData(type=ComponentDataKind.DATASET, name='b')

        self.assertTrue(first < second)
        self.assertTrue(first <= second)
        self.assertTrue(second >= first)

    def test_hash(self) -> None:
        self.assertEqual(
            hash(ComponentData(type=ComponentDataKind.DATASET, name='a')),
            hash(ComponentData(type=ComponentDataKind.DATASET, name='a')),
        )

    def test_bom_ref(self) -> None:
        self.assertEqual('data-1', ComponentData(type=ComponentDataKind.DATASET, bom_ref='data-1').bom_ref.value)
        bom_ref = BomRef('data-2')
        self.assertIs(bom_ref, ComponentData(type=ComponentDataKind.DATASET, bom_ref=bom_ref).bom_ref)

    def test_inequality_bom_ref(self) -> None:
        self.assertNotEqual(
            ComponentData(type=ComponentDataKind.DATASET, bom_ref='a'),
            ComponentData(type=ComponentDataKind.DATASET, bom_ref='b'),
        )

    def test_repr(self) -> None:
        self.assertEqual(
            repr(ComponentData(type=ComponentDataKind.DATASET, name='example', bom_ref='data-1')),
            "<ComponentData bom-ref='data-1' type=<ComponentDataKind.DATASET: 'dataset'> name='example'>",
        )


class TestDatasetReference(TestCase):

    def test_constructor(self) -> None:
        bom_ref = BomRef('data-1')
        uri = XsUri('urn:cdx:3e671687-395b-41f5-a30f-a58921a69b79/1#data-1')

        self.assertEqual('data-1', DatasetReference(ref='data-1').ref)
        self.assertIs(bom_ref, DatasetReference(ref=bom_ref).ref)
        self.assertIs(uri, DatasetReference(ref=uri).ref)

    def test_property_setters(self) -> None:
        obj = DatasetReference(ref='a')
        obj.ref = 'b'
        self.assertEqual('b', obj.ref)

    def test_empty_ref_is_rejected(self) -> None:
        with self.assertRaises(InvalidValueException):
            DatasetReference(ref='')
        with self.assertRaises(InvalidValueException):
            DatasetReference(ref=XsUri(''))
        obj = DatasetReference(ref='a')
        with self.assertRaises(InvalidValueException):
            obj.ref = ''
        self.assertEqual('a', obj.ref)

    def test_bom_ref_without_value_is_accepted(self) -> None:
        # the value may be assigned later, when the BOM is serialized
        self.assertEqual('', str(DatasetReference(ref=BomRef()).ref))

    def test_equality(self) -> None:
        self.assertEqual(DatasetReference(ref='a'), DatasetReference(ref='a'))
        self.assertEqual(DatasetReference(ref='a'), DatasetReference(ref=BomRef('a')))
        self.assertNotEqual(DatasetReference(ref='a'), DatasetReference(ref='b'))
        self.assertNotEqual(DatasetReference(ref='a'), 'a')

    def test_comparison(self) -> None:
        first = DatasetReference(ref='a')
        second = DatasetReference(ref='b')

        self.assertTrue(first < second)
        self.assertTrue(first <= second)
        self.assertTrue(second >= first)

    def test_comparison_with_component_data(self) -> None:
        reference = DatasetReference(ref='a')
        data = ComponentData(type=ComponentDataKind.DATASET, name='z')

        # inline data sorts before references, regardless of operand order
        self.assertTrue(data < reference)
        self.assertTrue(data <= reference)
        self.assertTrue(reference >= data)
        self.assertFalse(reference < data)
        self.assertFalse(reference <= data)
        self.assertFalse(data >= reference)
        self.assertListEqual([data, reference], sorted([reference, data]))

    def test_hash(self) -> None:
        self.assertEqual(hash(DatasetReference(ref='a')), hash(DatasetReference(ref=BomRef('a'))))

    def test_repr(self) -> None:
        self.assertEqual("<DatasetReference ref='a'>", repr(DatasetReference(ref='a')))
