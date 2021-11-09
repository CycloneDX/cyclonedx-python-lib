from unittest import TestCase

from cyclonedx.model import HashAlgorithm, HashType


class TestModel(TestCase):

    def test_hash_type_from_composite_str_1(self) -> None:
        h = HashType.from_composite_str('sha256:806143ae5bfb6a3c6e736a764057db0e6a0e05e338b5630894a5f779cabb4f9b')
        self.assertEqual(h.get_algorithm(), HashAlgorithm.SHA_256)
        self.assertEqual(h.get_hash_value(), '806143ae5bfb6a3c6e736a764057db0e6a0e05e338b5630894a5f779cabb4f9b')

    def test_hash_type_from_composite_str_2(self) -> None:
        h = HashType.from_composite_str('md5:dc26cd71b80d6757139f38156a43c545')
        self.assertEqual(h.get_algorithm(), HashAlgorithm.MD5)
        self.assertEqual(h.get_hash_value(), 'dc26cd71b80d6757139f38156a43c545')
