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
from time import sleep
from unittest import TestCase

from cyclonedx.exception.model import InvalidLocaleTypeException, InvalidUriException, UnknownHashTypeException, \
    NoPropertiesProvidedException
from cyclonedx.model import Copyright, Encoding, ExternalReference, ExternalReferenceType, HashAlgorithm, HashType, \
    IdentifiableAction, Note, NoteText, XsUri
from cyclonedx.model.issue import IssueClassification, IssueType


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


class TestModelExternalReference(TestCase):

    def test_external_reference_with_str(self) -> None:
        e = ExternalReference(reference_type=ExternalReferenceType.VCS, url='https://www.google.com')
        self.assertEqual(e.get_reference_type(), ExternalReferenceType.VCS)
        self.assertEqual(e.get_url(), 'https://www.google.com')
        self.assertEqual(e.get_comment(), '')
        self.assertListEqual(e.get_hashes(), [])

    def test_external_reference_with_xsuri(self) -> None:
        e = ExternalReference(reference_type=ExternalReferenceType.VCS, url=XsUri('https://www.google.com'))
        self.assertEqual(e.get_reference_type(), ExternalReferenceType.VCS)
        self.assertEqual(e.get_url(), 'https://www.google.com')
        self.assertEqual(e.get_comment(), '')
        self.assertListEqual(e.get_hashes(), [])

    def test_same(self) -> None:
        ref_1 = ExternalReference(
            reference_type=ExternalReferenceType.OTHER,
            url='https://cyclonedx.org',
            comment='No comment'
        )
        ref_2 = ExternalReference(
            reference_type=ExternalReferenceType.OTHER,
            url='https://cyclonedx.org',
            comment='No comment'
        )
        self.assertNotEqual(id(ref_1), id(ref_2))
        self.assertEqual(hash(ref_1), hash(ref_2))
        self.assertTrue(ref_1 == ref_2)

    def test_not_same(self) -> None:
        ref_1 = ExternalReference(
            reference_type=ExternalReferenceType.OTHER,
            url='https://cyclonedx.org',
            comment='No comment'
        )
        ref_2 = ExternalReference(
            reference_type=ExternalReferenceType.OTHER,
            url='https://cyclonedx.org/',
            comment='No comment'
        )
        self.assertNotEqual(id(ref_1), id(ref_2))
        self.assertNotEqual(hash(ref_1), hash(ref_2))
        self.assertFalse(ref_1 == ref_2)


class TestModelHashType(TestCase):

    def test_hash_type_from_composite_str_1(self) -> None:
        h = HashType.from_composite_str('sha256:806143ae5bfb6a3c6e736a764057db0e6a0e05e338b5630894a5f779cabb4f9b')
        self.assertEqual(h.get_algorithm(), HashAlgorithm.SHA_256)
        self.assertEqual(h.get_hash_value(), '806143ae5bfb6a3c6e736a764057db0e6a0e05e338b5630894a5f779cabb4f9b')

    def test_hash_type_from_composite_str_2(self) -> None:
        h = HashType.from_composite_str('md5:dc26cd71b80d6757139f38156a43c545')
        self.assertEqual(h.get_algorithm(), HashAlgorithm.MD5)
        self.assertEqual(h.get_hash_value(), 'dc26cd71b80d6757139f38156a43c545')

    def test_hash_type_from_unknown(self) -> None:
        with self.assertRaises(UnknownHashTypeException):
            HashType.from_composite_str('unknown:dc26cd71b80d6757139f38156a43c545')


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
        ia_1 = IdentifiableAction(timestamp=datetime.datetime.utcnow(), name='A Name', email='something@somewhere.tld')
        sleep(secs=1)
        ia_2 = IdentifiableAction(timestamp=datetime.datetime.utcnow(), name='A Name', email='something@somewhere.tld')
        self.assertNotEqual(hash(ia_1), hash(ia_2))
        self.assertFalse(ia_1 == ia_2)


class TestModelIssueType(TestCase):

    def test_issue_type(self) -> None:
        it = IssueType(
            classification=IssueClassification.SECURITY, id='CVE-2021-44228', name='Apache Log3Shell',
            description='Apache Log4j2 2.0-beta9 through 2.12.1 and 2.13.0 through 2.15.0 JNDI features used in '
                        'configuration, log messages, and parameters do not protect against attacker controlled LDAP '
                        'and other JNDI related endpoints. An attacker who can control log messages or log message '
                        'parameters can execute arbitrary code loaded from LDAP servers when message lookup '
                        'substitution is enabled. From log4j 2.15.0, this behavior has been disabled by default. From '
                        'version 2.16.0, this functionality has been completely removed. Note that this vulnerability '
                        'is specific to log4j-core and does not affect log4net, log4cxx, or other Apache Logging '
                        'Services projects.',
            source_name='NVD', source_url=XsUri('https://nvd.nist.gov/vuln/detail/CVE-2021-44228'),
            references=[
                XsUri('https://logging.apache.org/log4j/2.x/security.html'),
                XsUri('https://central.sonatype.org/news/20211213_log4shell_help')
            ]
        )
        self.assertEqual(it.get_classification(), IssueClassification.SECURITY),
        self.assertEqual(it.get_id(), 'CVE-2021-44228'),
        self.assertEqual(it.get_name(), 'Apache Log3Shell')
        self.assertEqual(
            it.get_description(),
            'Apache Log4j2 2.0-beta9 through 2.12.1 and 2.13.0 through 2.15.0 JNDI features used in '
            'configuration, log messages, and parameters do not protect against attacker controlled LDAP '
            'and other JNDI related endpoints. An attacker who can control log messages or log message '
            'parameters can execute arbitrary code loaded from LDAP servers when message lookup '
            'substitution is enabled. From log4j 2.15.0, this behavior has been disabled by default. From '
            'version 2.16.0, this functionality has been completely removed. Note that this vulnerability '
            'is specific to log4j-core and does not affect log4net, log4cxx, or other Apache Logging '
            'Services projects.'
        )
        self.assertEqual(it.get_source_name(), 'NVD'),
        self.assertEqual(str(it.get_source_url()), str(XsUri('https://nvd.nist.gov/vuln/detail/CVE-2021-44228')))
        self.assertEqual(str(it.get_source_url()), str('https://nvd.nist.gov/vuln/detail/CVE-2021-44228'))
        self.assertListEqual(list(map(lambda u: str(u), it.get_references())), [
            'https://logging.apache.org/log4j/2.x/security.html',
            'https://central.sonatype.org/news/20211213_log4shell_help'
        ])
        self.assertListEqual(list(map(lambda u: str(u), it.get_references())), [
            'https://logging.apache.org/log4j/2.x/security.html',
            'https://central.sonatype.org/news/20211213_log4shell_help'
        ])


class TestModelNote(TestCase):

    def test_note_plain_text(self) -> None:
        n = Note(text=NoteText('Some simple plain text'))
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
                content=text_content, content_type='text/plain; charset=UTF-8', content_encoding=Encoding.BASE_64
            ), locale='en-GB'
        )
        self.assertEqual(n.text.content, text_content)
        self.assertEqual(n.text.content_type, 'text/plain; charset=UTF-8')
        self.assertEqual(n.locale, 'en-GB')
        self.assertEqual(n.text.encoding, Encoding.BASE_64)


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
