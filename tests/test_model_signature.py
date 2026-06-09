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

from cyclonedx.exception.model import InvalidValueException
from cyclonedx.model.signature import (
    JsfAlgorithm,
    JsfKeyType,
    JsfPublicKey,
    JsfSignature,
    JsfSignatureChain,
    JsfSignatureSigners,
    JsfSimpleSignature,
)


class TestJsfPublicKey(TestCase):

    def test_ec_public_key(self) -> None:
        pk = JsfPublicKey(kty=JsfKeyType.EC, crv='P-256', x='abc', y='def')
        self.assertEqual(pk.kty, JsfKeyType.EC)
        self.assertEqual(pk.crv, 'P-256')
        self.assertEqual(pk.x, 'abc')
        self.assertEqual(pk.y, 'def')
        self.assertIsNone(pk.n)
        self.assertIsNone(pk.e)

    def test_okp_public_key(self) -> None:
        pk = JsfPublicKey(kty=JsfKeyType.OKP, crv='Ed25519', x='xyz')
        self.assertEqual(pk.kty, JsfKeyType.OKP)
        self.assertEqual(pk.crv, 'Ed25519')
        self.assertEqual(pk.x, 'xyz')
        self.assertIsNone(pk.y)
        self.assertIsNone(pk.n)
        self.assertIsNone(pk.e)

    def test_rsa_public_key(self) -> None:
        pk = JsfPublicKey(kty=JsfKeyType.RSA, n='modulus', e='exponent')
        self.assertEqual(pk.kty, JsfKeyType.RSA)
        self.assertEqual(pk.n, 'modulus')
        self.assertEqual(pk.e, 'exponent')
        self.assertIsNone(pk.crv)
        self.assertIsNone(pk.x)
        self.assertIsNone(pk.y)

    def test_equality(self) -> None:
        pk1 = JsfPublicKey(kty=JsfKeyType.EC, crv='P-256', x='abc', y='def')
        pk2 = JsfPublicKey(kty=JsfKeyType.EC, crv='P-256', x='abc', y='def')
        pk3 = JsfPublicKey(kty=JsfKeyType.RSA, n='n', e='e')
        self.assertEqual(pk1, pk2)
        self.assertNotEqual(pk1, pk3)

    def test_hash_stable(self) -> None:
        pk1 = JsfPublicKey(kty=JsfKeyType.EC, crv='P-256', x='abc', y='def')
        pk2 = JsfPublicKey(kty=JsfKeyType.EC, crv='P-256', x='abc', y='def')
        self.assertEqual(hash(pk1), hash(pk2))

    def test_sorting(self) -> None:
        pks = [
            JsfPublicKey(kty=JsfKeyType.RSA, n='n', e='e'),
            JsfPublicKey(kty=JsfKeyType.EC, crv='P-256', x='abc', y='def'),
            JsfPublicKey(kty=JsfKeyType.OKP, crv='Ed25519', x='xyz'),
        ]
        sorted_pks = sorted(pks)
        self.assertEqual(len(sorted_pks), 3)

    def test_ec_validation_missing_crv(self) -> None:
        with self.assertRaises(InvalidValueException) as cm:
            JsfPublicKey(kty=JsfKeyType.EC, x='abc', y='def')
        self.assertIn('EC', str(cm.exception))

    def test_ec_validation_missing_x(self) -> None:
        with self.assertRaises(InvalidValueException) as cm:
            JsfPublicKey(kty=JsfKeyType.EC, crv='P-256', y='def')
        self.assertIn('EC', str(cm.exception))

    def test_ec_validation_missing_y(self) -> None:
        with self.assertRaises(InvalidValueException) as cm:
            JsfPublicKey(kty=JsfKeyType.EC, crv='P-256', x='abc')
        self.assertIn('EC', str(cm.exception))

    def test_okp_validation_missing_crv(self) -> None:
        with self.assertRaises(InvalidValueException) as cm:
            JsfPublicKey(kty=JsfKeyType.OKP, x='xyz')
        self.assertIn('OKP', str(cm.exception))

    def test_okp_validation_missing_x(self) -> None:
        with self.assertRaises(InvalidValueException) as cm:
            JsfPublicKey(kty=JsfKeyType.OKP, crv='Ed25519')
        self.assertIn('OKP', str(cm.exception))

    def test_rsa_validation_missing_n(self) -> None:
        with self.assertRaises(InvalidValueException) as cm:
            JsfPublicKey(kty=JsfKeyType.RSA, e='exponent')
        self.assertIn('RSA', str(cm.exception))

    def test_rsa_validation_missing_e(self) -> None:
        with self.assertRaises(InvalidValueException) as cm:
            JsfPublicKey(kty=JsfKeyType.RSA, n='modulus')
        self.assertIn('RSA', str(cm.exception))

    def test_repr(self) -> None:
        pk = JsfPublicKey(kty=JsfKeyType.EC, crv='P-256', x='abc', y='def')
        self.assertIn('JsfPublicKey', repr(pk))
        self.assertIn('EC', repr(pk))


class TestJsfSimpleSignature(TestCase):
    """Tests for JsfSimpleSignature (simple signature mode)."""

    def test_minimal(self) -> None:
        sig = JsfSimpleSignature(algorithm=JsfAlgorithm.ES256, value='sig-value')
        self.assertEqual(sig.algorithm, JsfAlgorithm.ES256)
        self.assertEqual(sig.value, 'sig-value')
        self.assertIsNone(sig.key_id)
        self.assertIsNone(sig.public_key)
        self.assertEqual(sig.certificate_path, [])
        self.assertEqual(sig.excludes, [])

    def test_full(self) -> None:
        pk = JsfPublicKey(kty=JsfKeyType.EC, crv='P-256', x='abc', y='def')
        sig = JsfSimpleSignature(
            algorithm=JsfAlgorithm.ES256,
            value='sig-value',
            key_id='my-key',
            public_key=pk,
            certificate_path=['cert-pem'],
            excludes=['field1', 'field2'],
        )
        self.assertEqual(sig.public_key, pk)
        self.assertEqual(sig.key_id, 'my-key')
        self.assertEqual(sig.certificate_path, ['cert-pem'])
        self.assertEqual(sig.excludes, ['field1', 'field2'])

    def test_algorithm_as_enum(self) -> None:
        sig = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='v')
        self.assertIsInstance(sig.algorithm, JsfAlgorithm)

    def test_algorithm_as_uri_string(self) -> None:
        sig = JsfSimpleSignature(algorithm='https://example.com/algo', value='v')
        self.assertIsInstance(sig.algorithm, str)
        self.assertNotIsInstance(sig.algorithm, JsfAlgorithm)

    def test_equality(self) -> None:
        sig1 = JsfSimpleSignature(algorithm=JsfAlgorithm.ES256, value='v')
        sig2 = JsfSimpleSignature(algorithm=JsfAlgorithm.ES256, value='v')
        sig3 = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='v')
        self.assertEqual(sig1, sig2)
        self.assertNotEqual(sig1, sig3)

    def test_not_equal_to_other_modes(self) -> None:
        simple = JsfSimpleSignature(algorithm=JsfAlgorithm.ES256, value='v')
        multi = JsfSignatureSigners(signers=[JsfSimpleSignature(algorithm=JsfAlgorithm.ES256, value='v')])
        self.assertNotEqual(simple, multi)

    def test_hash_stable(self) -> None:
        sig1 = JsfSimpleSignature(algorithm=JsfAlgorithm.ES256, value='v')
        sig2 = JsfSimpleSignature(algorithm=JsfAlgorithm.ES256, value='v')
        self.assertEqual(hash(sig1), hash(sig2))

    def test_sorting(self) -> None:
        sigs = [
            JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='b'),
            JsfSimpleSignature(algorithm=JsfAlgorithm.ES256, value='a'),
        ]
        sorted_sigs = sorted(sigs)
        self.assertEqual(len(sorted_sigs), 2)

    def test_repr(self) -> None:
        sig = JsfSimpleSignature(algorithm=JsfAlgorithm.ES256, value='v')
        self.assertIn('JsfSimpleSignature', repr(sig))
        self.assertIn('ES256', repr(sig))


class TestJsfSignatureSigners(TestCase):
    """Tests for JsfSignatureSigners (multisignature mode)."""

    def test_minimal(self) -> None:
        signer = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='v1')
        sig = JsfSignatureSigners(signers=[signer])
        self.assertEqual(len(sig.signers), 1)
        self.assertEqual(sig.signers[0], signer)

    def test_multiple_signers(self) -> None:
        s1 = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='v1')
        s2 = JsfSimpleSignature(algorithm=JsfAlgorithm.ES256, value='v2')
        sig = JsfSignatureSigners(signers=[s1, s2])
        self.assertEqual(len(sig.signers), 2)

    def test_is_jsfsignature_subclass(self) -> None:
        sig = JsfSignatureSigners(signers=[JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='v')])
        self.assertIsInstance(sig, JsfSignature)

    def test_equality(self) -> None:
        s = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='v')
        sig1 = JsfSignatureSigners(signers=[s])
        sig2 = JsfSignatureSigners(signers=[s])
        sig3 = JsfSignatureSigners(signers=[JsfSimpleSignature(algorithm=JsfAlgorithm.ES256, value='x')])
        self.assertEqual(sig1, sig2)
        self.assertNotEqual(sig1, sig3)

    def test_not_equal_to_chain(self) -> None:
        s = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='v')
        multi = JsfSignatureSigners(signers=[s])
        chain = JsfSignatureChain(chain=[s])
        self.assertNotEqual(multi, chain)

    def test_hash_stable(self) -> None:
        s = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='v')
        sig1 = JsfSignatureSigners(signers=[s])
        sig2 = JsfSignatureSigners(signers=[s])
        self.assertEqual(hash(sig1), hash(sig2))

    def test_repr(self) -> None:
        s = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='v')
        sig = JsfSignatureSigners(signers=[s])
        self.assertIn('JsfSignatureSigners', repr(sig))
        self.assertIn('1', repr(sig))


class TestJsfSignatureChain(TestCase):
    """Tests for JsfSignatureChain (signaturechain mode)."""

    def test_minimal(self) -> None:
        signer = JsfSimpleSignature(algorithm=JsfAlgorithm.ED25519, value='xyzSig==')
        sig = JsfSignatureChain(chain=[signer])
        self.assertEqual(len(sig.chain), 1)
        self.assertEqual(sig.chain[0], signer)

    def test_multiple_in_chain(self) -> None:
        s1 = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='v1')
        s2 = JsfSimpleSignature(algorithm=JsfAlgorithm.ES256, value='v2')
        sig = JsfSignatureChain(chain=[s1, s2])
        self.assertEqual(len(sig.chain), 2)

    def test_is_jsfsignature_subclass(self) -> None:
        sig = JsfSignatureChain(chain=[JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='v')])
        self.assertIsInstance(sig, JsfSignature)

    def test_equality(self) -> None:
        s = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='v')
        sig1 = JsfSignatureChain(chain=[s])
        sig2 = JsfSignatureChain(chain=[s])
        sig3 = JsfSignatureChain(chain=[JsfSimpleSignature(algorithm=JsfAlgorithm.ES256, value='x')])
        self.assertEqual(sig1, sig2)
        self.assertNotEqual(sig1, sig3)

    def test_not_equal_to_multi(self) -> None:
        s = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='v')
        chain = JsfSignatureChain(chain=[s])
        multi = JsfSignatureSigners(signers=[s])
        self.assertNotEqual(chain, multi)

    def test_hash_stable(self) -> None:
        s = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='v')
        sig1 = JsfSignatureChain(chain=[s])
        sig2 = JsfSignatureChain(chain=[s])
        self.assertEqual(hash(sig1), hash(sig2))

    def test_repr(self) -> None:
        s = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='v')
        sig = JsfSignatureChain(chain=[s])
        self.assertIn('JsfSignatureChain', repr(sig))
        self.assertIn('1', repr(sig))


class TestJsfSignatureBaseClass(TestCase):
    """Tests that JsfSignature acts as a proper abstract base class / type for isinstance checks."""

    def test_simple_is_jsfsignature(self) -> None:
        self.assertIsInstance(
            JsfSimpleSignature(algorithm=JsfAlgorithm.ES256, value='v'),
            JsfSignature,
        )

    def test_signers_is_jsfsignature(self) -> None:
        self.assertIsInstance(
            JsfSignatureSigners(signers=[JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='v')]),
            JsfSignature,
        )

    def test_chain_is_jsfsignature(self) -> None:
        self.assertIsInstance(
            JsfSignatureChain(chain=[JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='v')]),
            JsfSignature,
        )

    def test_modes_are_distinct_types(self) -> None:
        simple = JsfSimpleSignature(algorithm=JsfAlgorithm.ES256, value='v')
        multi = JsfSignatureSigners(signers=[JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='v')])
        chain = JsfSignatureChain(chain=[JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='v')])
        # All are JsfSignature instances
        self.assertIsInstance(simple, JsfSignature)
        self.assertIsInstance(multi, JsfSignature)
        self.assertIsInstance(chain, JsfSignature)
        # But they are different types
        self.assertEqual(type(simple).__name__, 'JsfSimpleSignature')
        self.assertEqual(type(multi).__name__, 'JsfSignatureSigners')
        self.assertEqual(type(chain).__name__, 'JsfSignatureChain')


class TestJsfAlgorithm(TestCase):

    def test_enum_values(self) -> None:
        self.assertEqual(JsfAlgorithm.RS256.value, 'RS256')
        self.assertEqual(JsfAlgorithm.ES256.value, 'ES256')
        self.assertEqual(JsfAlgorithm.ED25519.value, 'Ed25519')
        self.assertEqual(JsfAlgorithm.ED448.value, 'Ed448')
        self.assertEqual(JsfAlgorithm.HS512.value, 'HS512')

    def test_all_algorithms_count(self) -> None:
        self.assertEqual(len(JsfAlgorithm), 14)


class TestJsfKeyType(TestCase):

    def test_enum_values(self) -> None:
        self.assertEqual(JsfKeyType.EC.value, 'EC')
        self.assertEqual(JsfKeyType.OKP.value, 'OKP')
        self.assertEqual(JsfKeyType.RSA.value, 'RSA')

    def test_all_key_types_count(self) -> None:
        self.assertEqual(len(JsfKeyType), 3)
