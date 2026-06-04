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


from datetime import datetime, timezone
from random import shuffle
from unittest import TestCase
from unittest.mock import MagicMock

from cyclonedx.exception.model import MutuallyExclusivePropertiesException
from cyclonedx.model import AttachedText, Property, XsUri
from cyclonedx.model.contact import OrganizationalContact, OrganizationalEntity
from cyclonedx.model.license import (
    DisjunctiveLicense,
    LicenseAcknowledgement,
    LicenseEntity,
    LicenseExpression,
    LicenseType,
    Licensing,
)
from tests import reorder


class TestModelDisjunctiveLicense(TestCase):
    def test_create_complete_id(self) -> None:
        text = MagicMock(spec=AttachedText)
        url = MagicMock(spec=XsUri)
        licensing = Licensing(purchase_order='PO-1')
        license = DisjunctiveLicense(id='foo', text=text, url=url, licensing=licensing)
        self.assertEqual('foo', license.id)
        self.assertIsNone(license.name)
        self.assertIs(text, license.text)
        self.assertIs(url, license.url)
        self.assertIs(licensing, license.licensing)

    def test_update_id_name(self) -> None:
        license = DisjunctiveLicense(id='foo')
        self.assertEqual('foo', license.id)
        self.assertIsNone(license.name)
        license.name = 'bar'
        self.assertIsNone(license.id)
        self.assertEqual('bar', license.name)

    def test_create_complete_named(self) -> None:
        text = MagicMock(spec=AttachedText)
        url = MagicMock(spec=XsUri)
        licensing = Licensing(purchase_order='PO-2')
        license = DisjunctiveLicense(name='foo', text=text, url=url, licensing=licensing)
        self.assertIsNone(license.id)
        self.assertEqual('foo', license.name)
        self.assertIs(text, license.text)
        self.assertIs(url, license.url)
        self.assertIs(licensing, license.licensing)

    def test_update_name_id(self) -> None:
        license = DisjunctiveLicense(name='foo')
        self.assertEqual('foo', license.name)
        self.assertIsNone(license.id)
        license.id = 'bar'
        self.assertIsNone(license.name)
        self.assertEqual('bar', license.id)

    def test_throws_when_no_id_nor_name(self) -> None:
        with self.assertRaises(MutuallyExclusivePropertiesException):
            DisjunctiveLicense(id=None, name=None)

    def test_prefers_id_over_name(self) -> None:
        with self.assertWarnsRegex(
                RuntimeWarning,
                'Both `id` and `name` have been supplied - `name` will be ignored!'):
            license = DisjunctiveLicense(id='foo', name='bar')
        self.assertEqual('foo', license.id)
        self.assertEqual(None, license.name)

    def test_licensing_none_by_default(self) -> None:
        license = DisjunctiveLicense(id='MIT')
        self.assertIsNone(license.licensing)

    def test_licensing_setter(self) -> None:
        license = DisjunctiveLicense(id='MIT')
        licensing = Licensing(
            purchase_order='PO-SET',
            licensor=LicenseEntity(organization=OrganizationalEntity(name='Vendor')),
        )
        license.licensing = licensing
        self.assertIs(licensing, license.licensing)
        license.licensing = None
        self.assertIsNone(license.licensing)

    def test_equal(self) -> None:
        a = DisjunctiveLicense(id='foo', name='bar')
        b = DisjunctiveLicense(id='foo', name='bar')
        c = DisjunctiveLicense(id='bar', name='foo')
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(a, 'foo')

    def test_equal_different_licensing(self) -> None:
        a = DisjunctiveLicense(id='MIT', licensing=Licensing(purchase_order='PO-1'))
        b = DisjunctiveLicense(id='MIT', licensing=Licensing(purchase_order='PO-2'))
        self.assertNotEqual(a, b)

    def test_equal_different_acknowledgement(self) -> None:
        a = DisjunctiveLicense(id='MIT', acknowledgement=LicenseAcknowledgement.DECLARED)
        b = DisjunctiveLicense(id='MIT', acknowledgement=LicenseAcknowledgement.CONCLUDED)
        self.assertNotEqual(a, b)

    def test_hash(self) -> None:
        text = MagicMock(spec=AttachedText)
        url = MagicMock(spec=XsUri)
        licensing = Licensing(purchase_order='PO-1')
        kwargs = dict(
            id='foo', text=text, url=url,
            licensing=licensing,
            acknowledgement=LicenseAcknowledgement.DECLARED,
            bom_ref='ref-hash',
        )
        a = DisjunctiveLicense(**kwargs)
        b = DisjunctiveLicense(**kwargs)
        self.assertEqual(hash(a), hash(b))

    def test_hash_different_licensing(self) -> None:
        a = DisjunctiveLicense(id='MIT', licensing=Licensing(purchase_order='PO-1'))
        b = DisjunctiveLicense(id='MIT', licensing=Licensing(purchase_order='PO-2'))
        self.assertNotEqual(hash(a), hash(b))

    def test_create_with_properties(self) -> None:
        properties = [Property(name='key1', value='value1')]
        license = DisjunctiveLicense(id='MIT', properties=properties)
        self.assertEqual(1, len(license.properties))

    def test_set_properties(self) -> None:
        license = DisjunctiveLicense(id='MIT')
        self.assertEqual(0, len(license.properties))
        license.properties = [Property(name='key1', value='value1')]
        self.assertEqual(1, len(license.properties))

    def test_equal_with_properties(self) -> None:
        a = DisjunctiveLicense(id='MIT', properties=[Property(name='key1', value='value1')])
        b = DisjunctiveLicense(id='MIT', properties=[Property(name='key1', value='value1')])
        c = DisjunctiveLicense(id='MIT')
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)


class TestModelLicenseExpression(TestCase):
    def test_create(self) -> None:
        license = LicenseExpression('foo')
        self.assertEqual('foo', license.value)

    def test_update(self) -> None:
        license = LicenseExpression('foo')
        self.assertEqual('foo', license.value)
        license.value = 'bar'
        self.assertEqual('bar', license.value)

    def test_equal(self) -> None:
        kwargs = dict(
            acknowledgement=LicenseAcknowledgement.DECLARED,
            bom_ref='ref-eq',
        )
        a = LicenseExpression('foo', **kwargs)
        b = LicenseExpression('foo', **kwargs)
        c = LicenseExpression('bar')
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(a, 'foo')

    def test_equal_different_acknowledgement(self) -> None:
        a = LicenseExpression('MIT', acknowledgement=LicenseAcknowledgement.DECLARED)
        b = LicenseExpression('MIT', acknowledgement=LicenseAcknowledgement.CONCLUDED)
        self.assertNotEqual(a, b)

    def test_hash(self) -> None:
        kwargs = dict(
            acknowledgement=LicenseAcknowledgement.DECLARED,
            bom_ref='ref-hash',
        )
        a = LicenseExpression('foo', **kwargs)
        b = LicenseExpression('foo', **kwargs)
        self.assertEqual(hash(a), hash(b))

    def test_hash_different_acknowledgement(self) -> None:
        a = LicenseExpression('MIT', acknowledgement=LicenseAcknowledgement.DECLARED)
        b = LicenseExpression('MIT', acknowledgement=LicenseAcknowledgement.CONCLUDED)
        self.assertNotEqual(hash(a), hash(b))


class TestModelLicenseEntity(TestCase):

    def test_create_with_organization(self) -> None:
        org = OrganizationalEntity(name='Acme Inc')
        holder = LicenseEntity(organization=org)
        self.assertIs(org, holder.organization)
        self.assertIsNone(holder.individual)

    def test_create_with_individual(self) -> None:
        contact = OrganizationalContact(name='John Doe', email='john@example.com')
        holder = LicenseEntity(individual=contact)
        self.assertIsNone(holder.organization)
        self.assertIs(contact, holder.individual)

    def test_throws_when_neither_provided(self) -> None:
        with self.assertRaises(MutuallyExclusivePropertiesException):
            LicenseEntity()

    def test_throws_when_both_provided(self) -> None:
        with self.assertRaises(MutuallyExclusivePropertiesException):
            LicenseEntity(
                organization=OrganizationalEntity(name='Acme'),
                individual=OrganizationalContact(name='John')
            )

    def test_setter_organization_clears_individual(self) -> None:
        contact = OrganizationalContact(name='John')
        holder = LicenseEntity(individual=contact)
        org = OrganizationalEntity(name='Acme')
        holder.organization = org
        self.assertIs(org, holder.organization)
        self.assertIsNone(holder.individual)

    def test_setter_individual_clears_organization(self) -> None:
        org = OrganizationalEntity(name='Acme')
        holder = LicenseEntity(organization=org)
        contact = OrganizationalContact(name='John')
        holder.individual = contact
        self.assertIs(contact, holder.individual)
        self.assertIsNone(holder.organization)

    def test_equal(self) -> None:
        a = LicenseEntity(organization=OrganizationalEntity(name='Acme'))
        b = LicenseEntity(organization=OrganizationalEntity(name='Acme'))
        c = LicenseEntity(individual=OrganizationalContact(name='John'))
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(a, 'foo')

    def test_hash(self) -> None:
        a = LicenseEntity(organization=OrganizationalEntity(name='Acme'))
        b = LicenseEntity(organization=OrganizationalEntity(name='Acme'))
        self.assertEqual(hash(a), hash(b))

    def test_hash_individual(self) -> None:
        a = LicenseEntity(individual=OrganizationalContact(name='John', email='john@example.com'))
        b = LicenseEntity(individual=OrganizationalContact(name='John', email='john@example.com'))
        self.assertEqual(hash(a), hash(b))

    def test_hash_different(self) -> None:
        a = LicenseEntity(organization=OrganizationalEntity(name='Acme'))
        b = LicenseEntity(individual=OrganizationalContact(name='John'))
        self.assertNotEqual(hash(a), hash(b))


class TestModelLicensing(TestCase):

    def test_create_minimal(self) -> None:
        licensing = Licensing()
        self.assertEqual(0, len(licensing.alt_ids))
        self.assertIsNone(licensing.licensor)
        self.assertIsNone(licensing.licensee)
        self.assertIsNone(licensing.purchaser)
        self.assertIsNone(licensing.purchase_order)
        self.assertEqual(0, len(licensing.license_types))
        self.assertIsNone(licensing.last_renewal)
        self.assertIsNone(licensing.expiration)

    def test_create_complete(self) -> None:
        licensor = LicenseEntity(organization=OrganizationalEntity(name='Acme Inc'))
        licensee = LicenseEntity(organization=OrganizationalEntity(name='Example Co.'))
        purchaser = LicenseEntity(individual=OrganizationalContact(
            name='Samantha Wright', email='samantha.wright@example.com', phone='800-555-1212'
        ))
        last_renewal = datetime(2022, 4, 13, 20, 20, 39, tzinfo=timezone.utc)
        expiration = datetime(2023, 4, 13, 20, 20, 39, tzinfo=timezone.utc)

        licensing = Licensing(
            alt_ids=['acme', 'acme-license'],
            licensor=licensor,
            licensee=licensee,
            purchaser=purchaser,
            purchase_order='PO-12345',
            license_types=[LicenseType.APPLIANCE],
            last_renewal=last_renewal,
            expiration=expiration,
        )
        self.assertEqual(2, len(licensing.alt_ids))
        self.assertIn('acme', licensing.alt_ids)
        self.assertIn('acme-license', licensing.alt_ids)
        self.assertIs(licensor, licensing.licensor)
        self.assertIs(licensee, licensing.licensee)
        self.assertIs(purchaser, licensing.purchaser)
        self.assertEqual('PO-12345', licensing.purchase_order)
        self.assertIn(LicenseType.APPLIANCE, licensing.license_types)
        self.assertEqual(last_renewal, licensing.last_renewal)
        self.assertEqual(expiration, licensing.expiration)

    def test_setters(self) -> None:
        licensing = Licensing()
        licensor = LicenseEntity(organization=OrganizationalEntity(name='Acme Inc'))
        licensee = LicenseEntity(individual=OrganizationalContact(name='Jane'))
        purchaser = LicenseEntity(organization=OrganizationalEntity(name='BuyCo'))
        last_renewal = datetime(2024, 1, 1, tzinfo=timezone.utc)
        expiration = datetime(2025, 1, 1, tzinfo=timezone.utc)

        licensing.licensor = licensor
        self.assertIs(licensor, licensing.licensor)
        licensing.licensee = licensee
        self.assertIs(licensee, licensing.licensee)
        licensing.purchaser = purchaser
        self.assertIs(purchaser, licensing.purchaser)
        licensing.purchase_order = 'PO-SET'
        self.assertEqual('PO-SET', licensing.purchase_order)
        licensing.license_types = [LicenseType.SUBSCRIPTION, LicenseType.NAMED_USER]
        self.assertIn(LicenseType.SUBSCRIPTION, licensing.license_types)
        self.assertIn(LicenseType.NAMED_USER, licensing.license_types)
        licensing.last_renewal = last_renewal
        self.assertEqual(last_renewal, licensing.last_renewal)
        licensing.expiration = expiration
        self.assertEqual(expiration, licensing.expiration)
        licensing.alt_ids = ['id-1', 'id-2']
        self.assertIn('id-1', licensing.alt_ids)
        self.assertIn('id-2', licensing.alt_ids)

    def test_equal(self) -> None:
        licensor = LicenseEntity(organization=OrganizationalEntity(name='Acme Inc'))
        licensee = LicenseEntity(individual=OrganizationalContact(name='Jane'))
        purchaser = LicenseEntity(organization=OrganizationalEntity(name='BuyCo'))
        last_renewal = datetime(2022, 4, 13, 20, 20, 39, tzinfo=timezone.utc)
        expiration = datetime(2023, 4, 13, 20, 20, 39, tzinfo=timezone.utc)
        kwargs = dict(
            alt_ids=['acme'],
            licensor=licensor,
            licensee=licensee,
            purchaser=purchaser,
            purchase_order='PO-1',
            license_types=[LicenseType.PERPETUAL],
            last_renewal=last_renewal,
            expiration=expiration,
        )
        a = Licensing(**kwargs)
        b = Licensing(**kwargs)
        c = Licensing(purchase_order='PO-2')
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(a, 'foo')

    def test_equal_different_licensor(self) -> None:
        a = Licensing(licensor=LicenseEntity(organization=OrganizationalEntity(name='Acme')))
        b = Licensing(licensor=LicenseEntity(organization=OrganizationalEntity(name='Other')))
        self.assertNotEqual(a, b)

    def test_equal_different_licensee(self) -> None:
        a = Licensing(licensee=LicenseEntity(individual=OrganizationalContact(name='Alice')))
        b = Licensing(licensee=LicenseEntity(individual=OrganizationalContact(name='Bob')))
        self.assertNotEqual(a, b)

    def test_equal_different_purchaser(self) -> None:
        a = Licensing(purchaser=LicenseEntity(organization=OrganizationalEntity(name='BuyCo')))
        b = Licensing(purchaser=LicenseEntity(organization=OrganizationalEntity(name='SellCo')))
        self.assertNotEqual(a, b)

    def test_equal_different_dates(self) -> None:
        a = Licensing(
            last_renewal=datetime(2022, 1, 1, tzinfo=timezone.utc),
            expiration=datetime(2023, 1, 1, tzinfo=timezone.utc),
        )
        b = Licensing(
            last_renewal=datetime(2024, 1, 1, tzinfo=timezone.utc),
            expiration=datetime(2025, 1, 1, tzinfo=timezone.utc),
        )
        self.assertNotEqual(a, b)

    def test_hash(self) -> None:
        licensor = LicenseEntity(organization=OrganizationalEntity(name='Acme Inc'))
        licensee = LicenseEntity(individual=OrganizationalContact(name='Jane'))
        purchaser = LicenseEntity(organization=OrganizationalEntity(name='BuyCo'))
        last_renewal = datetime(2022, 4, 13, 20, 20, 39, tzinfo=timezone.utc)
        expiration = datetime(2023, 4, 13, 20, 20, 39, tzinfo=timezone.utc)
        kwargs = dict(
            alt_ids=['acme'],
            licensor=licensor,
            licensee=licensee,
            purchaser=purchaser,
            purchase_order='PO-1',
            license_types=[LicenseType.PERPETUAL],
            last_renewal=last_renewal,
            expiration=expiration,
        )
        a = Licensing(**kwargs)
        b = Licensing(**kwargs)
        self.assertEqual(hash(a), hash(b))

    def test_hash_different_licensor(self) -> None:
        a = Licensing(licensor=LicenseEntity(organization=OrganizationalEntity(name='Acme')))
        b = Licensing(licensor=LicenseEntity(organization=OrganizationalEntity(name='Other')))
        self.assertNotEqual(hash(a), hash(b))

    def test_repr(self) -> None:
        licensing = Licensing(purchase_order='PO-REPR')
        r = repr(licensing)
        self.assertIn('Licensing', r)
        self.assertIn('PO-REPR', r)


class TestModelDisjunctiveLicenseWithLicensing(TestCase):

    def test_create_with_licensing(self) -> None:
        licensing = Licensing(
            purchase_order='PO-123',
            license_types=[LicenseType.SUBSCRIPTION],
            licensor=LicenseEntity(organization=OrganizationalEntity(name='Acme Inc')),
            licensee=LicenseEntity(individual=OrganizationalContact(name='Jane Doe')),
        )
        dl = DisjunctiveLicense(name='Commercial', licensing=licensing)
        self.assertIs(licensing, dl.licensing)

    def test_licensing_none_by_default(self) -> None:
        dl = DisjunctiveLicense(id='MIT')
        self.assertIsNone(dl.licensing)

    def test_setter(self) -> None:
        dl = DisjunctiveLicense(id='MIT')
        licensing = Licensing(
            purchase_order='PO-999',
            licensor=LicenseEntity(organization=OrganizationalEntity(name='Vendor')),
        )
        dl.licensing = licensing
        self.assertIs(licensing, dl.licensing)
        dl.licensing = None
        self.assertIsNone(dl.licensing)

    def test_equal_with_licensing(self) -> None:
        licensing = Licensing(
            purchase_order='PO-1',
            licensor=LicenseEntity(organization=OrganizationalEntity(name='Acme')),
            licensee=LicenseEntity(individual=OrganizationalContact(name='Bob')),
            purchaser=LicenseEntity(organization=OrganizationalEntity(name='BuyCo')),
            last_renewal=datetime(2022, 1, 1, tzinfo=timezone.utc),
            expiration=datetime(2023, 1, 1, tzinfo=timezone.utc),
        )
        a = DisjunctiveLicense(name='foo', licensing=licensing)
        b = DisjunctiveLicense(name='foo', licensing=licensing)
        c = DisjunctiveLicense(name='foo')
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test_hash_with_licensing(self) -> None:
        licensing = Licensing(
            purchase_order='PO-1',
            licensor=LicenseEntity(organization=OrganizationalEntity(name='Acme')),
        )
        a = DisjunctiveLicense(name='foo', licensing=licensing, bom_ref='ref-wl')
        b = DisjunctiveLicense(name='foo', licensing=licensing, bom_ref='ref-wl')
        self.assertEqual(hash(a), hash(b))


class TestModelLicense(TestCase):

    def test_sort_mixed(self) -> None:
        expected_order = [1, 2, 0]
        licenses = [
            DisjunctiveLicense(name='my license'),
            LicenseExpression(value='MIT or Apache-2.0'),
            DisjunctiveLicense(id='MIT'),
        ]
        expected_licenses = reorder(licenses, expected_order)
        shuffle(licenses)
        sorted_licenses = sorted(licenses)
        self.assertListEqual(sorted_licenses, expected_licenses)
