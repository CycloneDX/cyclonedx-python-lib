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

import datetime
from typing import List
from unittest import TestCase

from cyclonedx.exception.model import NoPropertiesProvidedException
from cyclonedx.model import (
    AttachedText,
    Copyright,
    Encoding,
    ExternalReference,
    ExternalReferenceType,
    IdentifiableAction,
    Property,
    XsUri,
)
from cyclonedx.model.component import (
    Commit,
    Component,
    ComponentEvidence,
    ComponentType,
    Diff,
    Patch,
    PatchClassification,
    Pedigree,
)
from cyclonedx.model.issue import IssueClassification, IssueType
from tests import reorder
from tests._data.models import (
    get_component_setuptools_simple,
    get_component_setuptools_simple_no_version,
    get_component_toml_with_hashes_with_references,
    get_issue_1,
    get_issue_2,
    get_pedigree_1,
    get_swid_1,
    get_swid_2,
)


class TestModelCommit(TestCase):

    def test_no_parameters(self) -> None:
        with self.assertRaises(NoPropertiesProvidedException):
            Commit()

    def test_same(self) -> None:
        ia_comitter = IdentifiableAction(timestamp=datetime.datetime.utcnow(), name='The Committer')
        c1 = Commit(uid='a-random-uid', author=ia_comitter, committer=ia_comitter, message='A commit message')
        c2 = Commit(uid='a-random-uid', author=ia_comitter, committer=ia_comitter, message='A commit message')
        self.assertEqual(hash(c1), hash(c2))
        self.assertTrue(c1 == c2)

    def test_not_same(self) -> None:
        ia_author = IdentifiableAction(timestamp=datetime.datetime.utcnow(), name='The Author')
        ia_comitter = IdentifiableAction(timestamp=datetime.datetime.utcnow(), name='The Committer')
        c1 = Commit(uid='a-random-uid', author=ia_comitter, committer=ia_comitter, message='A commit message')
        c2 = Commit(uid='a-random-uid', author=ia_author, committer=ia_comitter, message='A commit message')
        self.assertNotEqual(hash(c1), hash(c2))
        self.assertFalse(c1 == c2)

    def test_sort(self) -> None:
        url_a = XsUri('a')
        url_b = XsUri('b')
        action_a = IdentifiableAction(name='a')
        action_b = IdentifiableAction(name='b')

        # expected sort order: ([uid], [url], [author], [committer], [message])
        expected_order = [0, 1, 6, 2, 7, 3, 8, 4, 9, 5, 10]
        commits = [
            Commit(uid='a', url=url_a, author=action_a, committer=action_a, message='a'),
            Commit(uid='a', url=url_a, author=action_a, committer=action_a, message='b'),
            Commit(uid='a', url=url_a, author=action_a, committer=action_b, message='a'),
            Commit(uid='a', url=url_a, author=action_b, committer=action_a, message='a'),
            Commit(uid='a', url=url_b, author=action_a, committer=action_a, message='a'),
            Commit(uid='b', url=url_a, author=action_a, committer=action_a, message='a'),
            Commit(uid='a', url=url_a, author=action_a, committer=action_a),
            Commit(uid='a', url=url_a, author=action_a),
            Commit(uid='a', url=url_a),
            Commit(uid='a'),
            Commit(message='a'),
        ]
        sorted_commits = sorted(commits)
        expected_commits = reorder(commits, expected_order)
        self.assertListEqual(sorted_commits, expected_commits)


class TestModelComponent(TestCase):

    def test_empty_basic_component(self) -> None:
        c = Component(name='test-component')
        self.assertEqual(c.name, 'test-component')
        self.assertEqual(c.type, ComponentType.LIBRARY)
        self.assertIsNone(c.mime_type)
        self.assertIsNone(c.bom_ref.value)
        self.assertIsNone(c.supplier)
        self.assertIsNone(c.author)
        self.assertIsNone(c.publisher)
        self.assertIsNone(c.group)
        self.assertIsNone(c.version)
        self.assertIsNone(c.description)
        self.assertIsNone(c.scope)
        self.assertSetEqual(c.hashes, set())
        self.assertSetEqual(c.licenses, set())
        self.assertIsNone(c.copyright)
        self.assertIsNone(c.purl)
        self.assertSetEqual(c.external_references, set())
        self.assertFalse(c.properties)
        self.assertIsNone(c.release_notes)
        self.assertEqual(len(c.components), 0)
        self.assertEqual(len(c.get_all_nested_components(include_self=True)), 1)

    def test_multiple_basic_components(self) -> None:
        c1 = Component(name='test-component')
        self.assertEqual(c1.name, 'test-component')
        self.assertIsNone(c1.version)
        self.assertEqual(c1.type, ComponentType.LIBRARY)
        self.assertEqual(len(c1.external_references), 0)
        self.assertEqual(len(c1.hashes), 0)

        c2 = Component(name='test2-component')
        self.assertEqual(c2.name, 'test2-component')
        self.assertIsNone(c2.version)
        self.assertEqual(c2.type, ComponentType.LIBRARY)
        self.assertEqual(len(c2.external_references), 0)
        self.assertEqual(len(c2.hashes), 0)

        self.assertNotEqual(c1, c2)

    def test_external_references(self) -> None:
        c = Component(name='test-component')
        c.external_references.add(ExternalReference(
            type=ExternalReferenceType.OTHER,
            url=XsUri('https://cyclonedx.org'),
            comment='No comment'
        ))
        self.assertEqual(c.name, 'test-component')
        self.assertIsNone(c.version)
        self.assertEqual(c.type, ComponentType.LIBRARY)
        self.assertEqual(len(c.external_references), 1)
        self.assertEqual(len(c.hashes), 0)

        c2 = Component(name='test2-component')
        self.assertEqual(c2.name, 'test2-component')
        self.assertIsNone(c2.version)
        self.assertEqual(c2.type, ComponentType.LIBRARY)
        self.assertEqual(len(c2.external_references), 0)
        self.assertEqual(len(c2.hashes), 0)

    def test_empty_component_with_version(self) -> None:
        c = Component(name='test-component', version='1.2.3')
        self.assertEqual(c.name, 'test-component')
        self.assertEqual(c.version, '1.2.3')
        self.assertEqual(c.type, ComponentType.LIBRARY)
        self.assertEqual(len(c.external_references), 0)
        self.assertEqual(len(c.hashes), 0)

    def test_component_equal_1(self) -> None:
        c = Component(name='test-component')
        c.external_references.add(ExternalReference(
            type=ExternalReferenceType.OTHER,
            url=XsUri('https://cyclonedx.org'),
            comment='No comment'
        ))

        c2 = Component(name='test-component')
        c2.external_references.add(ExternalReference(
            type=ExternalReferenceType.OTHER,
            url=XsUri('https://cyclonedx.org'),
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

    def test_sort(self) -> None:
        # expected sort order: (type, [group], name, [version])
        expected_order = [6, 4, 5, 3, 2, 1, 0]
        components = [
            Component(name='component-c', type=ComponentType.LIBRARY),
            Component(name='component-a', type=ComponentType.LIBRARY),
            Component(name='component-b', type=ComponentType.LIBRARY, group='group-2'),
            Component(name='component-a', type=ComponentType.LIBRARY, group='group-2'),
            Component(name='component-a', type=ComponentType.FILE),
            Component(name='component-b', type=ComponentType.FILE),
            Component(name='component-a', type=ComponentType.FILE, version='1.0.0'),
        ]
        sorted_components = sorted(components)
        expected_components = reorder(components, expected_order)
        self.assertListEqual(sorted_components, expected_components)

    def test_nested_components_1(self) -> None:
        comp_b = Component(name='comp_b')
        comp_c = Component(name='comp_c')
        comp_b.components.add(comp_c)

        self.assertEqual(1, len(comp_b.components))
        self.assertEqual(2, len(comp_b.get_all_nested_components(include_self=True)))
        self.assertEqual(1, len(comp_b.get_all_nested_components(include_self=False)))

    def test_nested_components_2(self) -> None:
        comp_a = Component(name='comp_a')
        comp_b = Component(name='comp_b')
        comp_c = Component(name='comp_c')
        comp_b.components.add(comp_c)
        comp_b.components.add(comp_a)

        self.assertEqual(2, len(comp_b.components))
        self.assertEqual(3, len(comp_b.get_all_nested_components(include_self=True)))
        self.assertEqual(2, len(comp_b.get_all_nested_components(include_self=False)))


class TestModelComponentEvidence(TestCase):

    def test_no_params(self) -> None:
        with self.assertRaises(NoPropertiesProvidedException):
            ComponentEvidence()

    def test_same_1(self) -> None:
        ce_1 = ComponentEvidence(copyright=[Copyright(text='Commercial')])
        ce_2 = ComponentEvidence(copyright=[Copyright(text='Commercial')])
        self.assertEqual(hash(ce_1), hash(ce_2))
        self.assertTrue(ce_1 == ce_2)

    def test_same_2(self) -> None:
        ce_1 = ComponentEvidence(copyright=[Copyright(text='Commercial'), Copyright(text='Commercial 2')])
        ce_2 = ComponentEvidence(copyright=[Copyright(text='Commercial 2'), Copyright(text='Commercial')])
        self.assertEqual(hash(ce_1), hash(ce_2))
        self.assertTrue(ce_1 == ce_2)

    def test_not_same_1(self) -> None:
        ce_1 = ComponentEvidence(copyright=[Copyright(text='Commercial')])
        ce_2 = ComponentEvidence(copyright=[Copyright(text='Commercial 2')])
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

    def test_sort(self) -> None:
        text_a = AttachedText(content='a')
        text_b = AttachedText(content='b')

        # expected sort order: ([url], [text])
        expected_order = [1, 0, 5, 2, 3, 4]
        diffs = [
            Diff(url=XsUri('a'), text=text_b),
            Diff(url=XsUri('a'), text=text_a),
            Diff(url=XsUri('b'), text=text_a),
            Diff(text=text_a),
            Diff(text=text_b),
            Diff(url=XsUri('a')),
        ]
        sorted_diffs = sorted(diffs)
        expected_diffs = reorder(diffs, expected_order)
        self.assertListEqual(sorted_diffs, expected_diffs)


class TestModelAttachedText(TestCase):

    def test_sort(self) -> None:
        # expected sort order: (content_type, content, encoding)
        expected_order = [0, 4, 2, 1, 3]
        text = [
            AttachedText(content='a', content_type='a', encoding=Encoding.BASE_64),
            AttachedText(content='a', content_type='b', encoding=Encoding.BASE_64),
            AttachedText(content='b', content_type='a', encoding=Encoding.BASE_64),
            AttachedText(content='b', content_type='b', encoding=Encoding.BASE_64),
            AttachedText(content='a', content_type='a'),
        ]
        sorted_text = sorted(text)
        expected_text = reorder(text, expected_order)
        self.assertListEqual(sorted_text, expected_text)


class TestModelPatch(TestCase):

    def test_same_1(self) -> None:
        p1 = Patch(
            type=PatchClassification.BACKPORT, diff=Diff(url=XsUri('https://cyclonedx.org')),
            resolves=[get_issue_1(), get_issue_2()]
        )
        p2 = Patch(
            type=PatchClassification.BACKPORT, diff=Diff(url=XsUri('https://cyclonedx.org')),
            resolves=[get_issue_2(), get_issue_1()]
        )
        self.assertEqual(hash(p1), hash(p2))
        self.assertNotEqual(id(p1), id(p2))
        self.assertTrue(p1 == p2)

    def test_multiple_times_same(self) -> None:
        i = 0
        while i < 1000:
            p1 = Patch(
                type=PatchClassification.BACKPORT, diff=Diff(url=XsUri('https://cyclonedx.org')),
                resolves=[get_issue_1(), get_issue_2()]
            )
            p2 = Patch(
                type=PatchClassification.BACKPORT, diff=Diff(url=XsUri('https://cyclonedx.org')),
                resolves=[get_issue_2(), get_issue_1(), get_issue_1(), get_issue_1(), get_issue_2()]
            )
            self.assertEqual(hash(p1), hash(p2))
            self.assertNotEqual(id(p1), id(p2))
            self.assertTrue(p1 == p2)

            i += 1

    def test_not_same_1(self) -> None:
        p1 = Patch(
            type=PatchClassification.MONKEY, diff=Diff(url=XsUri('https://cyclonedx.org/')),
            resolves=[get_issue_1(), get_issue_2()]
        )
        p2 = Patch(
            type=PatchClassification.BACKPORT, diff=Diff(url=XsUri('https://cyclonedx.org')),
            resolves=[get_issue_2(), get_issue_1()]
        )
        self.assertNotEqual(hash(p1), hash(p2))
        self.assertNotEqual(id(p1), id(p2))
        self.assertFalse(p1 == p2)

    def test_sort(self) -> None:
        diff_a = Diff(text=AttachedText(content='a'))
        diff_b = Diff(text=AttachedText(content='b'))

        resolves_a = [
            IssueType(type=IssueClassification.DEFECT),
            IssueType(type=IssueClassification.SECURITY)
        ]

        # expected sort order: (type, [diff], sorted(resolves))
        expected_order = [5, 4, 3, 2, 1, 0]
        patches = [
            Patch(type=PatchClassification.MONKEY),
            Patch(type=PatchClassification.MONKEY, diff=diff_b),
            Patch(type=PatchClassification.MONKEY, diff=diff_a),
            Patch(type=PatchClassification.MONKEY, diff=diff_a, resolves=resolves_a),
            Patch(type=PatchClassification.BACKPORT),
            Patch(type=PatchClassification.BACKPORT, diff=diff_a),
        ]
        sorted_patches = sorted(patches)
        expected_patches = reorder(patches, expected_order)
        self.assertListEqual(sorted_patches, expected_patches)


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
