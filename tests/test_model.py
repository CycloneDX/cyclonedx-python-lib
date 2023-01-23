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

import base64
import datetime
from enum import Enum
from unittest import TestCase

from cyclonedx.exception.model import (
    InvalidLocaleTypeException,
    InvalidUriException,
    NoPropertiesProvidedException,
    UnknownHashTypeException,
)
from cyclonedx.model import (
    ComparableTuple,
    Copyright,
    Encoding,
    ExternalReference,
    ExternalReferenceType,
    HashAlgorithm,
    HashType,
    IdentifiableAction,
    License,
    LicenseChoice,
    Note,
    NoteText,
    OrganizationalContact,
    Property,
    Tool,
    XsUri,
)
from cyclonedx.model.issue import IssueClassification, IssueType, IssueTypeSource

from .data import reorder


class DummyStringEnum(str, Enum):
    FIRST = 'first'
    SECOND = 'second'
    THIRD = 'third'
    FOURTH = 'fourth'


class TestStringEnum(TestCase):

    def test_sort(self) -> None:
        enums = [
            DummyStringEnum.FIRST,
            DummyStringEnum.SECOND,
            DummyStringEnum.THIRD,
            DummyStringEnum.FOURTH,
        ]
        sorted_enums = sorted(enums)
        expected_enums = [
            DummyStringEnum.FIRST,
            DummyStringEnum.FOURTH,
            DummyStringEnum.SECOND,
            DummyStringEnum.THIRD,
        ]
        self.assertListEqual(sorted_enums, expected_enums)


class TestComparableTuple(TestCase):

    def test_equal_self(self) -> None:
        tuple1 = ComparableTuple((1, 2, 3, 4, 5))
        self.assertEqual(tuple1, tuple1)

    def test_equal(self) -> None:
        tuple1 = ComparableTuple((1, 2, 3, 4, 5))
        tuple2 = ComparableTuple((1, 2, 3, 4, 5))
        self.assertEqual(tuple1, tuple2)
        self.assertEqual(tuple2, tuple1)

    def test_equal_none(self) -> None:
        tuple1 = ComparableTuple((1, 2, None, 4, 5))
        tuple2 = ComparableTuple((1, 2, None, 4, 5))
        self.assertEqual(tuple1, tuple2)
        self.assertEqual(tuple2, tuple1)

    def test_compare_first_item(self) -> None:
        tuple1 = ComparableTuple((1, 2, 3, 4, 5))
        tuple2 = ComparableTuple((2, 2, 3, 4, 5))
        self.assertLess(tuple1, tuple2)
        self.assertGreater(tuple2, tuple1)
        self.assertNotEqual(tuple1, tuple2)
        self.assertNotEqual(tuple2, tuple1)

    def test_compare_mixed(self) -> None:
        tuple1 = ComparableTuple((1, 2, 1))
        tuple2 = ComparableTuple((2, 1, 2))
        self.assertLess(tuple1, tuple2)
        self.assertGreater(tuple2, tuple1)
        self.assertNotEqual(tuple1, tuple2)
        self.assertNotEqual(tuple2, tuple1)

    def test_compare_first_item_none(self) -> None:
        tuple1 = ComparableTuple((1, 2, 3, 4, 5))
        tuple2 = ComparableTuple((None, 2, 3, 4, 5))
        self.assertLess(tuple1, tuple2)
        self.assertGreater(tuple2, tuple1)
        self.assertNotEqual(tuple1, tuple2)
        self.assertNotEqual(tuple2, tuple1)

    def test_compare_last_item(self) -> None:
        tuple1 = ComparableTuple((1, 2, 3, 4, 5))
        tuple2 = ComparableTuple((1, 2, 3, 4, 10))
        self.assertLess(tuple1, tuple2)
        self.assertGreater(tuple2, tuple1)
        self.assertNotEqual(tuple1, tuple2)
        self.assertNotEqual(tuple2, tuple1)

    def test_compare_last_item_none(self) -> None:
        tuple1 = ComparableTuple((1, 2, 3, 4, 5))
        tuple2 = ComparableTuple((1, 2, 3, 4, None))
        self.assertLess(tuple1, tuple2)
        self.assertGreater(tuple2, tuple1)
        self.assertNotEqual(tuple1, tuple2)
        self.assertNotEqual(tuple2, tuple1)

    def test_compare_enum(self) -> None:
        tuple1 = ComparableTuple((DummyStringEnum.FIRST, ))
        tuple2 = ComparableTuple((DummyStringEnum.SECOND, ))
        self.assertLess(tuple1, tuple2)
        self.assertGreater(tuple2, tuple1)
        self.assertNotEqual(tuple1, tuple2)
        self.assertNotEqual(tuple2, tuple1)

    def test_compare_enum_then_none(self) -> None:
        tuple1 = ComparableTuple((DummyStringEnum.FIRST, None))
        tuple2 = ComparableTuple((DummyStringEnum.SECOND, 'a'))
        self.assertLess(tuple1, tuple2)
        self.assertGreater(tuple2, tuple1)
        self.assertNotEqual(tuple1, tuple2)
        self.assertNotEqual(tuple2, tuple1)


class TestModelLicense(TestCase):

    def test_sort(self) -> None:
        # expected sort order: ([id], [name])
        expected_order = [1, 0, 3, 2]
        licenses = [
            License(id_='MIT'),
            License(id_='Apache-2.0'),
            License(name='MIT'),
            License(name='Apache-2.0'),
        ]
        sorted_licenses = sorted(licenses)
        expected_licenses = reorder(licenses, expected_order)
        self.assertListEqual(sorted_licenses, expected_licenses)


class TestModelLicenseChoice(TestCase):

    def test_sort(self) -> None:
        license_a = License(id_='Apache-2.0')
        license_b = License(id_='MIT')

        # expected sort order: ([license], [expression])
        expected_order = [1, 0, 3, 2]
        licenses = [
            LicenseChoice(license_=license_b),
            LicenseChoice(license_=license_a),
            LicenseChoice(expression='MIT'),
            LicenseChoice(expression='Apache-2.0'),
        ]
        sorted_licenses = sorted(licenses)
        expected_licenses = reorder(licenses, expected_order)
        self.assertListEqual(sorted_licenses, expected_licenses)


class TestModelCopyright(TestCase):

    def test_same(self) -> None:
        copy_1 = Copyright(text='Copyright (c) OWASP Foundation. All Rights Reserved.')
        copy_2 = Copyright(text='Copyright (c) OWASP Foundation. All Rights Reserved.')
        self.assertEqual(hash(copy_1), hash(copy_2))
        self.assertTrue(copy_1 == copy_2)

    def test_not_same(self) -> None:
        copy_1 = Copyright(text='Copyright (c) OWASP Foundation. All Rights Reserved.')
        copy_2 = Copyright(text='Copyright (c) OWASP Foundation.')
        self.assertNotEqual(hash(copy_1), hash(copy_2))
        self.assertFalse(copy_1 == copy_2)

    def test_sort(self) -> None:
        # expected sort order: (text)
        expected_order = [0, 1, 2, 4, 3]
        copyrights = [
            Copyright(text='a'),
            Copyright(text='b'),
            Copyright(text='c'),
            Copyright(text='f'),
            Copyright(text='d'),
        ]
        sorted_copyrights = sorted(copyrights)
        expected_copyrights = reorder(copyrights, expected_order)
        self.assertListEqual(sorted_copyrights, expected_copyrights)


class TestModelExternalReference(TestCase):

    def test_external_reference_with_xsuri(self) -> None:
        e = ExternalReference(type_=ExternalReferenceType.VCS, url=XsUri('https://www.google.com'))
        self.assertEqual(e.type_, ExternalReferenceType.VCS)
        self.assertEqual(e.url, XsUri('https://www.google.com'))
        self.assertIsNone(e.comment)
        self.assertSetEqual(e.hashes, set())

    def test_same(self) -> None:
        ref_1 = ExternalReference(
            type_=ExternalReferenceType.OTHER,
            url=XsUri('https://cyclonedx.org'),
            comment='No comment'
        )
        ref_2 = ExternalReference(
            type_=ExternalReferenceType.OTHER,
            url=XsUri('https://cyclonedx.org'),
            comment='No comment'
        )
        self.assertNotEqual(id(ref_1), id(ref_2))
        self.assertEqual(hash(ref_1), hash(ref_2))
        self.assertTrue(ref_1 == ref_2)

    def test_not_same(self) -> None:
        ref_1 = ExternalReference(
            type_=ExternalReferenceType.OTHER,
            url=XsUri('https://cyclonedx.org'),
            comment='No comment'
        )
        ref_2 = ExternalReference(
            type_=ExternalReferenceType.OTHER,
            url=XsUri('https://cyclonedx.org/'),
            comment='No comment'
        )
        self.assertNotEqual(id(ref_1), id(ref_2))
        self.assertNotEqual(hash(ref_1), hash(ref_2))
        self.assertFalse(ref_1 == ref_2)

    def test_sort(self) -> None:
        # expected sort order: (type, url, [comment])
        expected_order = [5, 4, 0, 1, 3, 2]
        refs = [
            ExternalReference(type_=ExternalReferenceType.OTHER, url=XsUri('a'), comment='a'),
            ExternalReference(type_=ExternalReferenceType.OTHER, url=XsUri('a'), comment='b'),
            ExternalReference(type_=ExternalReferenceType.OTHER, url=XsUri('b')),
            ExternalReference(type_=ExternalReferenceType.OTHER, url=XsUri('b'), comment='a'),
            ExternalReference(type_=ExternalReferenceType.LICENSE, url=XsUri('b'), comment='a'),
            ExternalReference(type_=ExternalReferenceType.BUILD_SYSTEM, url=XsUri('b'), comment='a'),
        ]
        sorted_refs = sorted(refs)
        expected_refs = reorder(refs, expected_order)
        self.assertListEqual(sorted_refs, expected_refs)


class TestModelHashType(TestCase):

    def test_hash_type_from_composite_str_1(self) -> None:
        h = HashType.from_composite_str('sha256:806143ae5bfb6a3c6e736a764057db0e6a0e05e338b5630894a5f779cabb4f9b')
        self.assertEqual(h.alg, HashAlgorithm.SHA_256)
        self.assertEqual(h.content, '806143ae5bfb6a3c6e736a764057db0e6a0e05e338b5630894a5f779cabb4f9b')

    def test_hash_type_from_composite_str_2(self) -> None:
        h = HashType.from_composite_str('md5:dc26cd71b80d6757139f38156a43c545')
        self.assertEqual(h.alg, HashAlgorithm.MD5)
        self.assertEqual(h.content, 'dc26cd71b80d6757139f38156a43c545')

    def test_hash_type_from_unknown(self) -> None:
        with self.assertRaises(UnknownHashTypeException):
            HashType.from_composite_str('unknown:dc26cd71b80d6757139f38156a43c545')

    def test_sort(self) -> None:
        # expected sort order: (alg, content)
        expected_order = [5, 3, 4, 1, 2, 0]
        hashes = [
            HashType(alg=HashAlgorithm.SHA_256, content='c'),
            HashType(alg=HashAlgorithm.SHA_256, content='a'),
            HashType(alg=HashAlgorithm.SHA_256, content='b'),
            HashType(alg=HashAlgorithm.SHA_1, content='a'),
            HashType(alg=HashAlgorithm.SHA_1, content='b'),
            HashType(alg=HashAlgorithm.MD5, content='a'),
        ]
        sorted_hashes = sorted(hashes)
        expected_hashes = reorder(hashes, expected_order)
        self.assertListEqual(sorted_hashes, expected_hashes)


class TestModelIdentifiableAction(TestCase):

    def test_no_params(self) -> None:
        with self.assertRaises(NoPropertiesProvidedException):
            IdentifiableAction()

    def test_same(self) -> None:
        ts = datetime.datetime.utcnow()
        ia_1 = IdentifiableAction(timestamp=ts, name='A Name', email='something@somewhere.tld')
        ia_2 = IdentifiableAction(timestamp=ts, name='A Name', email='something@somewhere.tld')
        self.assertEqual(hash(ia_1), hash(ia_2))
        self.assertTrue(ia_1 == ia_2)

    def test_not_same(self) -> None:
        now = datetime.datetime.utcnow()
        not_now = now + datetime.timedelta(seconds=1)
        ia_1 = IdentifiableAction(timestamp=now, name='A Name', email='something@somewhere.tld')
        ia_2 = IdentifiableAction(timestamp=not_now, name='A Name', email='something@somewhere.tld')
        self.assertNotEqual(hash(ia_1), hash(ia_2))
        self.assertFalse(ia_1 == ia_2)

    def test_sort(self) -> None:
        now = datetime.datetime.utcnow()
        now_plus_one = now + datetime.timedelta(seconds=1)
        # expected sort order: ([timestamp], [name], [email])
        expected_order = [2, 3, 5, 4, 6, 0, 1]
        actions = [
            IdentifiableAction(timestamp=now_plus_one, name='a', email='a'),
            IdentifiableAction(timestamp=now_plus_one, name='a', email='b'),
            IdentifiableAction(timestamp=now, name='a', email='a'),
            IdentifiableAction(timestamp=now, name='a', email='b'),
            IdentifiableAction(timestamp=now, name='b', email='a'),
            IdentifiableAction(timestamp=now, name='a'),
            IdentifiableAction(timestamp=now),
        ]
        sorted_notes = sorted(actions)
        expected_notes = reorder(actions, expected_order)
        self.assertListEqual(sorted_notes, expected_notes)


class TestModelIssueType(TestCase):

    def test_issue_type(self) -> None:
        it = IssueType(
            type_=IssueClassification.SECURITY, id_='CVE-2021-44228', name='Apache Log3Shell',
            description='Apache Log4j2 2.0-beta9 through 2.12.1 and 2.13.0 through 2.15.0 JNDI features used in '
                        'configuration, log messages, and parameters do not protect against attacker controlled LDAP '
                        'and other JNDI related endpoints. An attacker who can control log messages or log message '
                        'parameters can execute arbitrary code loaded from LDAP servers when message lookup '
                        'substitution is enabled. From log4j 2.15.0, this behavior has been disabled by default. From '
                        'version 2.16.0, this functionality has been completely removed. Note that this vulnerability '
                        'is specific to log4j-core and does not affect log4net, log4cxx, or other Apache Logging '
                        'Services projects.',
            source=IssueTypeSource(name='NVD', url=XsUri('https://nvd.nist.gov/vuln/detail/CVE-2021-44228')),
            references=[
                XsUri('https://logging.apache.org/log4j/2.x/security.html'),
                XsUri('https://central.sonatype.org/news/20211213_log4shell_help')
            ]
        )
        self.assertEqual(it.type_, IssueClassification.SECURITY),
        self.assertEqual(it.id_, 'CVE-2021-44228'),
        self.assertEqual(it.name, 'Apache Log3Shell')
        self.assertEqual(
            it.description,
            'Apache Log4j2 2.0-beta9 through 2.12.1 and 2.13.0 through 2.15.0 JNDI features used in '
            'configuration, log messages, and parameters do not protect against attacker controlled LDAP '
            'and other JNDI related endpoints. An attacker who can control log messages or log message '
            'parameters can execute arbitrary code loaded from LDAP servers when message lookup '
            'substitution is enabled. From log4j 2.15.0, this behavior has been disabled by default. From '
            'version 2.16.0, this functionality has been completely removed. Note that this vulnerability '
            'is specific to log4j-core and does not affect log4net, log4cxx, or other Apache Logging '
            'Services projects.'
        )
        self.assertEqual(it.source.name, 'NVD'),
        self.assertEqual(it.source.url, XsUri('https://nvd.nist.gov/vuln/detail/CVE-2021-44228'))
        self.assertSetEqual(it.references, {
            XsUri('https://logging.apache.org/log4j/2.x/security.html'),
            XsUri('https://central.sonatype.org/news/20211213_log4shell_help')
        })


class TestModelNote(TestCase):

    def test_note_plain_text(self) -> None:
        n = Note(text=NoteText(content='Some simple plain text'))
        self.assertEqual(n.text.content, 'Some simple plain text')
        self.assertEqual(n.text.content_type, NoteText.DEFAULT_CONTENT_TYPE)
        self.assertIsNone(n.locale)
        self.assertIsNone(n.text.encoding)

    def test_note_invalid_locale(self) -> None:
        with self.assertRaises(InvalidLocaleTypeException):
            Note(text=NoteText(content='Some simple plain text'), locale='invalid-locale')

    def test_note_encoded_text_with_locale(self) -> None:
        text_content: str = base64.b64encode(
            bytes('Some simple plain text', encoding='UTF-8')
        ).decode(encoding='UTF-8')

        n = Note(
            text=NoteText(
                content=text_content, content_type='text/plain; charset=UTF-8', encoding=Encoding.BASE_64
            ), locale='en-GB'
        )
        self.assertEqual(n.text.content, text_content)
        self.assertEqual(n.text.content_type, 'text/plain; charset=UTF-8')
        self.assertEqual(n.locale, 'en-GB')
        self.assertEqual(n.text.encoding, Encoding.BASE_64)

    def test_sort(self) -> None:
        # expected sort order: ([locale], text)
        expected_order = [1, 2, 0, 3, 5, 4]
        notes = [
            Note(text=NoteText(content='c'), locale='en-GB'),
            Note(text=NoteText(content='a'), locale='en-GB'),
            Note(text=NoteText(content='b'), locale='en-GB'),
            Note(text=NoteText(content='d'), locale='en-GB'),
            Note(text=NoteText(content='a')),
            Note(text=NoteText(content='a'), locale='en-US'),
        ]
        sorted_notes = sorted(notes)
        expected_notes = reorder(notes, expected_order)
        self.assertListEqual(sorted_notes, expected_notes)


class TestModelNoteText(TestCase):

    def test_sort(self) -> None:
        # expected sort order: (content, [content_type], [encoding])
        expected_order = [1, 7, 4, 5, 6, 2, 0, 3]
        notes = [
            NoteText(content='c'),
            NoteText(content='a'),
            NoteText(content='b'),
            NoteText(content='d'),
            NoteText(content='b', content_type='a'),
            NoteText(content='b', content_type='b'),
            NoteText(content='b', content_type='c'),
            NoteText(content='b', content_type='a', encoding=Encoding.BASE_64),
        ]
        sorted_notes = sorted(notes)
        expected_notes = reorder(notes, expected_order)
        self.assertListEqual(sorted_notes, expected_notes)


class TestModelOrganizationalContact(TestCase):

    def test_sort(self) -> None:
        # expected sort order: ([name], [email], [phone])
        expected_order = [0, 3, 2, 1, 5, 4]
        contacts = [
            OrganizationalContact(name='a', email='a', phone='a'),
            OrganizationalContact(name='b', email='a', phone='a'),
            OrganizationalContact(name='a', email='b', phone='a'),
            OrganizationalContact(name='a', email='a', phone='b'),
            OrganizationalContact(phone='a'),
            OrganizationalContact(email='a'),
        ]
        sorted_contacts = sorted(contacts)
        expected_contacts = reorder(contacts, expected_order)
        self.assertListEqual(sorted_contacts, expected_contacts)


class TestModelXsUri(TestCase):

    # URI samples taken from http://www.datypic.com/sc/xsd/t-xsd_anyURI.html
    def test_valid_url(self) -> None:
        self.assertIsInstance(
            XsUri(uri='https://www.google.com'), XsUri
        )

    def test_valid_mailto(self) -> None:
        self.assertIsInstance(
            XsUri(uri='mailto:test@testing.tld'), XsUri
        )

    def test_valid_relative_url_escaped_ascii(self) -> None:
        self.assertIsInstance(
            XsUri(uri='../%C3%A9dition.html'), XsUri
        )

    def test_valid_relative_url_unescaped_ascii(self) -> None:
        self.assertIsInstance(
            XsUri(uri='../édition.html'), XsUri
        )

    def test_valid_url_with_fragment(self) -> None:
        self.assertIsInstance(
            XsUri(uri='http://datypic.com/prod.html#shirt'), XsUri
        )

    def test_valid_relative_url_with_fragment(self) -> None:
        self.assertIsInstance(
            XsUri(uri='../prod.html#shirt'), XsUri
        )

    def test_valid_urn(self) -> None:
        self.assertIsInstance(
            XsUri(uri='urn:example:org'), XsUri
        )

    def test_valid_empty(self) -> None:
        self.assertIsInstance(
            XsUri(uri=''), XsUri
        )

    def test_invalid_url_multiple_fragments(self) -> None:
        with self.assertRaises(InvalidUriException):
            XsUri(uri='http://datypic.com#frag1#frag2')

    def test_invalid_url_bad_escaped_character(self) -> None:
        with self.assertRaises(InvalidUriException):
            XsUri(uri='http://datypic.com#f% rag')

    def test_note_with_no_locale(self) -> None:
        self.assertIsInstance(
            Note(text=NoteText(content='Something')), Note
        )

    def test_note_with_valid_locale(self) -> None:
        self.assertIsInstance(
            Note(text=NoteText(content='Something'), locale='en-GB'), Note
        )

    def test_note_with_invalid_locale(self) -> None:
        with self.assertRaises(InvalidLocaleTypeException):
            Note(text=NoteText(content='Something'), locale='rubbish')

    def test_sort(self) -> None:
        # expected sort order: (uri)
        expected_order = [2, 1, 3, 0]
        uris = [
            XsUri(uri="d"),
            XsUri(uri="b"),
            XsUri(uri="a"),
            XsUri(uri="c"),
        ]
        sorted_uris = sorted(uris)
        expected_uris = reorder(uris, expected_order)
        self.assertListEqual(sorted_uris, expected_uris)


class TestModelProperty(TestCase):

    def test_sort(self) -> None:
        # expected sort order: (name, value)
        expected_order = [0, 5, 2, 3, 4, 1]
        props = [
            Property(name='a', value='a'),
            Property(name='b', value='b'),
            Property(name='a', value='c'),
            Property(name='a', value='d'),
            Property(name='b', value='a'),
            Property(name='a', value='b'),
        ]
        sorted_props = sorted(props)
        expected_props = reorder(props, expected_order)
        self.assertListEqual(sorted_props, expected_props)


class TestModelTool(TestCase):

    def test_sort(self) -> None:
        # expected sort order: (vendor, name, version)
        expected_order = [0, 1, 2, 3, 4, 5, 6]
        tools = [
            Tool(vendor='a', name='a', version='1.0.0'),
            Tool(vendor='a', name='a', version='2.0.0'),
            Tool(vendor='a', name='b', version='1.0.0'),
            Tool(vendor='a', name='b'),
            Tool(vendor='b', name='a'),
            Tool(vendor='b', name='b', version='1.0.0'),
            Tool(name='b'),
        ]
        sorted_tools = sorted(tools)
        expected_tools = reorder(tools, expected_order)
        self.assertListEqual(sorted_tools, expected_tools)
