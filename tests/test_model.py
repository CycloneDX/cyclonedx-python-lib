import base64
from unittest import TestCase

from cyclonedx.exception.model import InvalidLocaleTypeException, InvalidUriException
from cyclonedx.exception.parser import UnknownHashTypeException

from cyclonedx.model import Encoding, ExternalReference, ExternalReferenceType, HashAlgorithm, HashType, \
    IssueClassification, IssueType, Note, NoteText, XsUri


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
            bytearray('Some simple plain text', encoding='UTF-8')
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
            Note(text='Something'), Note
        )

    def test_note_with_valid_locale(self) -> None:
        self.assertIsInstance(
            Note(text='Something', locale='en-GB'), Note
        )

    def test_note_with_invalid_locale(self) -> None:
        with self.assertRaises(InvalidLocaleTypeException):
            Note(text='Something', locale='rubbish')
