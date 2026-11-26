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

from cyclonedx.contrib.hash.factories import HashTypeFactory
from cyclonedx.exception.model import UnknownHashTypeException
from cyclonedx.model import HashAlgorithm


class TestHashTypeFactoryCompositeStr(TestCase):

    def test_known_prefixes(self) -> None:
        factory = HashTypeFactory()
        for composite, alg in (
            ('md5:ABC', HashAlgorithm.MD5),
            ('sha1:ABC', HashAlgorithm.SHA_1),
            ('sha256:ABC', HashAlgorithm.SHA_256),
            ('sha3-256:ABC', HashAlgorithm.SHA3_256),
            ('blake2b256:ABC', HashAlgorithm.BLAKE2B_256),
            ('blake3:ABC', HashAlgorithm.BLAKE3),
        ):
            with self.subTest(composite=composite):
                hash_ = factory.from_composite_str(composite)
                self.assertIs(alg, hash_.alg)
                self.assertEqual('abc', hash_.content)

    def test_unsupported_algorithm_raises_unknown_hash_type(self) -> None:
        factory = HashTypeFactory()
        for composite in (
            'unknown:abc',
            'blake2b_256:abc',
            'sha224:abc',
            'sha3_224:abc',
        ):
            with self.subTest(composite=composite), self.assertRaises(UnknownHashTypeException):
                factory.from_composite_str(composite)

    def test_missing_separator_raises_unknown_hash_type(self) -> None:
        factory = HashTypeFactory()
        for composite in ('md5', 'sha256', 'sha3-256', 'blake3', ''):
            with self.subTest(composite=composite), self.assertRaises(UnknownHashTypeException):
                factory.from_composite_str(composite)
