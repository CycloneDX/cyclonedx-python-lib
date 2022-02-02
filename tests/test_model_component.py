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
import datetime
from typing import List
from unittest import TestCase
from unittest.mock import Mock, patch

from cyclonedx.exception.model import NoPropertiesProvidedException
from cyclonedx.model import AttachedText, Copyright, ExternalReference, ExternalReferenceType, \
    IdentifiableAction, Property, XsUri
from cyclonedx.model.component import Commit, Component, ComponentEvidence, ComponentType, Diff, Patch, \
    PatchClassification, Pedigree
from data import get_component_setuptools_simple, get_component_setuptools_simple_no_version, \
    get_component_toml_with_hashes_with_references, get_issue_1, get_issue_2, get_pedigree_1, get_swid_1, get_swid_2


class TestModelCommit(TestCase):

    def test_no_parameters(self) -> None:
        with self.assertRaises(NoPropertiesProvidedException):
            Commit()

    def test_same(self) -> None:
        ia_comitter = IdentifiableAction(timestamp=datetime.datetime.utcnow(), name='The Committer')
        c1 = Commit(uid='a-random-uid', author=ia_comitter, committer=ia_comitter, message="A commit message")
        c2 = Commit(uid='a-random-uid', author=ia_comitter, committer=ia_comitter, message="A commit message")
        self.assertEqual(hash(c1), hash(c2))
        self.assertTrue(c1 == c2)

    def test_not_same(self) -> None:
        ia_author = IdentifiableAction(timestamp=datetime.datetime.utcnow(), name='The Author')
        ia_comitter = IdentifiableAction(timestamp=datetime.datetime.utcnow(), name='The Committer')
        c1 = Commit(uid='a-random-uid', author=ia_comitter, committer=ia_comitter, message="A commit message")
        c2 = Commit(uid='a-random-uid', author=ia_author, committer=ia_comitter, message="A commit message")
        self.assertNotEqual(hash(c1), hash(c2))
        self.assertFalse(c1 == c2)


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

    def test_same_1(self) -> None:
        c1 = get_component_setuptools_simple()
        c2 = get_component_setuptools_simple()
        self.assertNotEqual(id(c1), id(c2))
        self.assertEqual(hash(c1), hash(c2))
        self.assertTrue(c1 == c2)

    def test_same_2(self) -> None:
        c1 = get_component_toml_with_hashes_with_references()
        c2 = get_component_toml_with_hashes_with_references()
        self.assertNotEqual(id(c1), id(c2))
        self.assertEqual(hash(c1), hash(c2))
        self.assertTrue(c1 == c2)

    def test_same_3(self) -> None:
        c1 = get_component_setuptools_simple_no_version()
        c2 = get_component_setuptools_simple_no_version()
        self.assertNotEqual(id(c1), id(c2))
        self.assertEqual(hash(c1), hash(c2))
        self.assertTrue(c1 == c2)

    def test_not_same_1(self) -> None:
        c1 = get_component_setuptools_simple()
        c2 = get_component_setuptools_simple_no_version()
        self.assertNotEqual(id(c1), id(c2))
        self.assertNotEqual(hash(c1), hash(c2))
        self.assertFalse(c1 == c2)


class TestModelComponentEvidence(TestCase):

    def test_no_params(self) -> None:
        with self.assertRaises(NoPropertiesProvidedException):
            ComponentEvidence()

    def test_same_1(self) -> None:
        ce_1 = ComponentEvidence(copyright_=[Copyright(text='Commercial')])
        ce_2 = ComponentEvidence(copyright_=[Copyright(text='Commercial')])
        self.assertEqual(hash(ce_1), hash(ce_2))
        self.assertTrue(ce_1 == ce_2)

    def test_same_2(self) -> None:
        ce_1 = ComponentEvidence(copyright_=[Copyright(text='Commercial'), Copyright(text='Commercial 2')])
        ce_2 = ComponentEvidence(copyright_=[Copyright(text='Commercial 2'), Copyright(text='Commercial')])
        self.assertEqual(hash(ce_1), hash(ce_2))
        self.assertTrue(ce_1 == ce_2)

    def test_not_same_1(self) -> None:
        ce_1 = ComponentEvidence(copyright_=[Copyright(text='Commercial')])
        ce_2 = ComponentEvidence(copyright_=[Copyright(text='Commercial 2')])
        self.assertNotEqual(hash(ce_1), hash(ce_2))
        self.assertFalse(ce_1 == ce_2)


class TestModelDiff(TestCase):

    def test_no_params(self) -> None:
        with self.assertRaises(NoPropertiesProvidedException):
            Diff()

    def test_same(self) -> None:
        at = AttachedText(content='A very long diff')
        diff_1 = Diff(text=at, url=XsUri('https://cyclonedx.org'))
        diff_2 = Diff(text=at, url=XsUri('https://cyclonedx.org'))
        self.assertEqual(hash(diff_1), hash(diff_2))
        self.assertTrue(diff_1 == diff_2)

    def test_not_same(self) -> None:
        at = AttachedText(content='A very long diff')
        diff_1 = Diff(text=at, url=XsUri('https://cyclonedx.org/'))
        diff_2 = Diff(text=at, url=XsUri('https://cyclonedx.org'))
        self.assertNotEqual(hash(diff_1), hash(diff_2))
        self.assertFalse(diff_1 == diff_2)


class TestModelPatch(TestCase):

    def test_same_1(self) -> None:
        p1 = Patch(
            type_=PatchClassification.BACKPORT, diff=Diff(url=XsUri('https://cyclonedx.org')),
            resolves=[get_issue_1(), get_issue_2()]
        )
        p2 = Patch(
            type_=PatchClassification.BACKPORT, diff=Diff(url=XsUri('https://cyclonedx.org')),
            resolves=[get_issue_2(), get_issue_1()]
        )
        self.assertEqual(hash(p1), hash(p2))
        self.assertNotEqual(id(p1), id(p2))
        self.assertTrue(p1 == p2)

    def test_not_same_1(self) -> None:
        p1 = Patch(
            type_=PatchClassification.MONKEY, diff=Diff(url=XsUri('https://cyclonedx.org/')),
            resolves=[get_issue_1(), get_issue_2()]
        )
        p2 = Patch(
            type_=PatchClassification.BACKPORT, diff=Diff(url=XsUri('https://cyclonedx.org')),
            resolves=[get_issue_2(), get_issue_1()]
        )
        self.assertNotEqual(hash(p1), hash(p2))
        self.assertNotEqual(id(p1), id(p2))
        self.assertFalse(p1 == p2)


class TestModelPedigree(TestCase):

    def test_no_params(self) -> None:
        with self.assertRaises(NoPropertiesProvidedException):
            Pedigree()

    def test_same_1(self) -> None:
        p1 = get_pedigree_1()
        p2 = get_pedigree_1()
        self.assertNotEqual(id(p1), id(p2))
        self.assertEqual(hash(p1), hash(p2))
        self.assertTrue(p1 == p2)

    def test_not_same_1(self) -> None:
        p1 = get_pedigree_1()
        p2 = get_pedigree_1()
        p2.notes = 'Some other notes here'
        self.assertNotEqual(id(p1), id(p2))
        self.assertNotEqual(hash(p1), hash(p2))
        self.assertFalse(p1 == p2)


class TestModelSwid(TestCase):

    def test_same_1(self) -> None:
        sw_1 = get_swid_1()
        sw_2 = get_swid_1()
        self.assertNotEqual(id(sw_1), id(sw_2))
        self.assertEqual(hash(sw_1), hash(sw_2))
        self.assertTrue(sw_1 == sw_2)

    def test_same_2(self) -> None:
        sw_1 = get_swid_2()
        sw_2 = get_swid_2()
        self.assertNotEqual(id(sw_1), id(sw_2))
        self.assertEqual(hash(sw_1), hash(sw_2))
        self.assertTrue(sw_1 == sw_2)

    def test_not_same(self) -> None:
        sw_1 = get_swid_1()
        sw_2 = get_swid_2()
        self.assertNotEqual(id(sw_1), id(sw_2))
        self.assertNotEqual(hash(sw_1), hash(sw_2))
        self.assertFalse(sw_1 == sw_2)
