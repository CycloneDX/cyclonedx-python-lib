from unittest import TestCase

from cyclonedx.exception.model import InvalidLocaleTypeException, InvalidUriException

from cyclonedx.model import HashAlgorithm, HashType, Note, XsUri


class TestModel(TestCase):

    def test_hash_type_from_composite_str_1(self) -> None:
        h = HashType.from_composite_str('sha256:806143ae5bfb6a3c6e736a764057db0e6a0e05e338b5630894a5f779cabb4f9b')
        self.assertEqual(h.get_algorithm(), HashAlgorithm.SHA_256)
        self.assertEqual(h.get_hash_value(), '806143ae5bfb6a3c6e736a764057db0e6a0e05e338b5630894a5f779cabb4f9b')

    def test_hash_type_from_composite_str_2(self) -> None:
        h = HashType.from_composite_str('md5:dc26cd71b80d6757139f38156a43c545')
        self.assertEqual(h.get_algorithm(), HashAlgorithm.MD5)
        self.assertEqual(h.get_hash_value(), 'dc26cd71b80d6757139f38156a43c545')

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
