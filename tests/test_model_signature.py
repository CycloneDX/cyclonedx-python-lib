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
from cyclonedx.model import XsUri
from cyclonedx.model.signature import (
    JsfAlgorithm,
    JsfEcCurve,
    JsfKeyType,
    JsfOkpCurve,
    JsfPublicKey,
    JsfSignatureChain,
    JsfSignatureSigners,
    JsfSimpleSignature,
)
from tests import reorder


class TestJsfAlgorithm(TestCase):
    def test_enum_value(self) -> None:
        self.assertEqual(JsfAlgorithm.RS256.value, 'RS256')
        self.assertEqual(JsfAlgorithm.RS384.value, 'RS384')
        self.assertEqual(JsfAlgorithm.RS512.value, 'RS512')
        self.assertEqual(JsfAlgorithm.PS256.value, 'PS256')
        self.assertEqual(JsfAlgorithm.PS384.value, 'PS384')
        self.assertEqual(JsfAlgorithm.PS512.value, 'PS512')
        self.assertEqual(JsfAlgorithm.ES256.value, 'ES256')
        self.assertEqual(JsfAlgorithm.ES384.value, 'ES384')
        self.assertEqual(JsfAlgorithm.ES512.value, 'ES512')
        self.assertEqual(JsfAlgorithm.ED25519.value, 'Ed25519')
        self.assertEqual(JsfAlgorithm.ED448.value, 'Ed448')
        self.assertEqual(JsfAlgorithm.HS256.value, 'HS256')
        self.assertEqual(JsfAlgorithm.HS384.value, 'HS384')
        self.assertEqual(JsfAlgorithm.HS512.value, 'HS512')

    def test_enum_comparison(self) -> None:
        self.assertEqual(JsfAlgorithm.RS256, JsfAlgorithm('RS256'))
        self.assertEqual(JsfAlgorithm.RS384, JsfAlgorithm('RS384'))
        self.assertEqual(JsfAlgorithm.RS512, JsfAlgorithm('RS512'))
        self.assertEqual(JsfAlgorithm.PS256, JsfAlgorithm('PS256'))
        self.assertEqual(JsfAlgorithm.PS384, JsfAlgorithm('PS384'))
        self.assertEqual(JsfAlgorithm.PS512, JsfAlgorithm('PS512'))
        self.assertEqual(JsfAlgorithm.ES256, JsfAlgorithm('ES256'))
        self.assertEqual(JsfAlgorithm.ES384, JsfAlgorithm('ES384'))
        self.assertEqual(JsfAlgorithm.ES512, JsfAlgorithm('ES512'))
        self.assertEqual(JsfAlgorithm.ED25519, JsfAlgorithm('Ed25519'))
        self.assertEqual(JsfAlgorithm.ED448, JsfAlgorithm('Ed448'))
        self.assertEqual(JsfAlgorithm.HS256, JsfAlgorithm('HS256'))
        self.assertEqual(JsfAlgorithm.HS384, JsfAlgorithm('HS384'))
        self.assertEqual(JsfAlgorithm.HS512, JsfAlgorithm('HS512'))


class TestJsfKeyType(TestCase):
    def test_enum_value(self) -> None:
        self.assertEqual(JsfKeyType.EC.value, 'EC')
        self.assertEqual(JsfKeyType.OKP.value, 'OKP')
        self.assertEqual(JsfKeyType.RSA.value, 'RSA')

    def test_enum_comparison(self) -> None:
        self.assertEqual(JsfKeyType.EC, JsfKeyType('EC'))
        self.assertEqual(JsfKeyType.OKP, JsfKeyType('OKP'))
        self.assertEqual(JsfKeyType.RSA, JsfKeyType('RSA'))


class TestJsfEcCurve(TestCase):
    def test_enum_value(self) -> None:
        self.assertEqual(JsfEcCurve.P_256.value, 'P-256')
        self.assertEqual(JsfEcCurve.P_384.value, 'P-384')
        self.assertEqual(JsfEcCurve.P_521.value, 'P-521')

    def test_enum_comparison(self) -> None:
        self.assertEqual(JsfEcCurve.P_256, JsfEcCurve('P-256'))
        self.assertEqual(JsfEcCurve.P_384, JsfEcCurve('P-384'))
        self.assertEqual(JsfEcCurve.P_521, JsfEcCurve('P-521'))


class TestJsfOkpCurve(TestCase):
    def test_enum_value(self) -> None:
        self.assertEqual(JsfOkpCurve.ED25519.value, 'Ed25519')
        self.assertEqual(JsfOkpCurve.ED448.value, 'Ed448')

    def test_enum_comparison(self) -> None:
        self.assertEqual(JsfOkpCurve.ED25519, JsfOkpCurve('Ed25519'))
        self.assertEqual(JsfOkpCurve.ED448, JsfOkpCurve('Ed448'))


class TestJsfPublicKey(TestCase):

    # -------------------------------------------------------------------------
    # Constructor & Property Tests (Valid Configurations)
    # -------------------------------------------------------------------------

    def test_constructor_ec(self) -> None:
        obj = JsfPublicKey(
            kty=JsfKeyType.EC,
            crv=JsfEcCurve.P_256,
            x='foo',
            y='bar'
        )
        self.assertEqual(obj.kty, JsfKeyType.EC)
        self.assertEqual(obj.crv, JsfEcCurve.P_256)
        self.assertEqual(obj.x, 'foo')
        self.assertEqual(obj.y, 'bar')
        self.assertIsNone(obj.n)
        self.assertIsNone(obj.e)

    def test_constructor_okp(self) -> None:
        obj = JsfPublicKey(
            kty=JsfKeyType.OKP,
            crv=JsfOkpCurve.ED25519,
            x='foo'
        )
        self.assertEqual(obj.kty, JsfKeyType.OKP)
        self.assertEqual(obj.crv, JsfOkpCurve.ED25519)
        self.assertEqual(obj.x, 'foo')
        self.assertIsNone(obj.y)
        self.assertIsNone(obj.n)
        self.assertIsNone(obj.e)

    def test_constructor_rsa(self) -> None:
        obj = JsfPublicKey(
            kty=JsfKeyType.RSA,
            n='modulus',
            e='exponent'
        )
        self.assertEqual(obj.kty, JsfKeyType.RSA)
        self.assertIsNone(obj.crv)
        self.assertIsNone(obj.x)
        self.assertIsNone(obj.y)
        self.assertEqual(obj.n, 'modulus')
        self.assertEqual(obj.e, 'exponent')

    def test_property_setters(self) -> None:
        obj = JsfPublicKey(kty=JsfKeyType.RSA, n='modulus', e='exponent')
        obj.n = 'new_modulus'
        self.assertEqual(obj.n, 'new_modulus')

    # -------------------------------------------------------------------------
    # Exhaustive Conditional Validation Tests (Every Permutation)
    # -------------------------------------------------------------------------

    # --- EC Key Type Validations ---

    def test_validation_ec_missing_crv(self) -> None:
        with self.assertRaises(InvalidValueException) as context:
            JsfPublicKey(kty=JsfKeyType.EC, crv=None, x='foo', y='bar')
        self.assertEqual(str(context.exception), 'EC public key requires crv, x, and y')

    def test_validation_ec_missing_x(self) -> None:
        with self.assertRaises(InvalidValueException) as context:
            JsfPublicKey(kty=JsfKeyType.EC, crv=JsfEcCurve.P_256, x=None, y='bar')
        self.assertEqual(str(context.exception), 'EC public key requires crv, x, and y')

    def test_validation_ec_missing_y(self) -> None:
        with self.assertRaises(InvalidValueException) as context:
            JsfPublicKey(kty=JsfKeyType.EC, crv=JsfEcCurve.P_256, x='foo', y=None)
        self.assertEqual(str(context.exception), 'EC public key requires crv, x, and y')

    def test_validation_ec_invalid_curve_type(self) -> None:
        with self.assertRaises(InvalidValueException) as context:
            JsfPublicKey(kty=JsfKeyType.EC, crv=JsfOkpCurve.ED25519, x='foo', y='bar')
        self.assertEqual(
            str(context.exception),
            "EC public key crv must be a JsfEcCurve instance, got 'JsfOkpCurve'"
        )

    def test_validation_ec_prohibits_n(self) -> None:
        with self.assertRaises(InvalidValueException):
            JsfPublicKey(kty=JsfKeyType.EC, crv=JsfEcCurve.P_256, x='foo', y='bar', n='modulus')

    def test_validation_ec_prohibits_e(self) -> None:
        with self.assertRaises(InvalidValueException):
            JsfPublicKey(kty=JsfKeyType.EC, crv=JsfEcCurve.P_256, x='foo', y='bar', e='exponent')

    # --- OKP Key Type Validations ---

    def test_validation_okp_missing_crv(self) -> None:
        with self.assertRaises(InvalidValueException) as context:
            JsfPublicKey(kty=JsfKeyType.OKP, crv=None, x='foo')
        self.assertEqual(str(context.exception), 'OKP public key requires crv and x')

    def test_validation_okp_missing_x(self) -> None:
        with self.assertRaises(InvalidValueException) as context:
            JsfPublicKey(kty=JsfKeyType.OKP, crv=JsfOkpCurve.ED25519, x=None)
        self.assertEqual(str(context.exception), 'OKP public key requires crv and x')

    def test_validation_okp_invalid_curve_type(self) -> None:
        with self.assertRaises(InvalidValueException) as context:
            JsfPublicKey(kty=JsfKeyType.OKP, crv=JsfEcCurve.P_256, x='foo')
        self.assertEqual(
            str(context.exception),
            "OKP public key crv must be a JsfOkpCurve instance, got 'JsfEcCurve'"
        )

    def test_validation_okp_prohibits_y(self) -> None:
        with self.assertRaises(InvalidValueException):
            JsfPublicKey(kty=JsfKeyType.OKP, crv=JsfOkpCurve.ED25519, x='foo', y='bar')

    def test_validation_okp_prohibits_n(self) -> None:
        with self.assertRaises(InvalidValueException):
            JsfPublicKey(kty=JsfKeyType.OKP, crv=JsfOkpCurve.ED25519, x='foo', n='modulus')

    def test_validation_okp_prohibits_e(self) -> None:
        with self.assertRaises(InvalidValueException):
            JsfPublicKey(kty=JsfKeyType.OKP, crv=JsfOkpCurve.ED25519, x='foo', e='exponent')

    # --- RSA Key Type Validations ---

    def test_validation_rsa_missing_n(self) -> None:
        with self.assertRaises(InvalidValueException) as context:
            JsfPublicKey(kty=JsfKeyType.RSA, n=None, e='exponent')
        self.assertEqual(str(context.exception), 'RSA public key requires n and e')

    def test_validation_rsa_missing_e(self) -> None:
        with self.assertRaises(InvalidValueException) as context:
            JsfPublicKey(kty=JsfKeyType.RSA, n='modulus', e=None)
        self.assertEqual(str(context.exception), 'RSA public key requires n and e')

    def test_validation_rsa_prohibits_crv(self) -> None:
        with self.assertRaises(InvalidValueException):
            JsfPublicKey(kty=JsfKeyType.RSA, n='modulus', e='exponent', crv=JsfEcCurve.P_256)

    def test_validation_rsa_prohibits_x(self) -> None:
        with self.assertRaises(InvalidValueException):
            JsfPublicKey(kty=JsfKeyType.RSA, n='modulus', e='exponent', x='foo')

    def test_validation_rsa_prohibits_y(self) -> None:
        with self.assertRaises(InvalidValueException):
            JsfPublicKey(kty=JsfKeyType.RSA, n='modulus', e='exponent', y='bar')

    def test_empty_key_values_are_allowed_by_schema(self) -> None:
        self.assertEqual(
            JsfPublicKey(kty=JsfKeyType.EC, crv=JsfEcCurve.P_256, x='', y='')._as_dict(),
            {'kty': 'EC', 'crv': 'P-256', 'x': '', 'y': ''},
        )
        self.assertEqual(
            JsfPublicKey(kty=JsfKeyType.RSA, n='', e='')._as_dict(),
            {'kty': 'RSA', 'n': '', 'e': ''},
        )

    def test_from_dict_rejects_incompatible_fields(self) -> None:
        cases = (
            {'kty': 'RSA', 'n': 'n', 'e': 'e', 'crv': 'P-256'},
            {'kty': 'RSA', 'n': 'n', 'e': 'e', 'crv': None},
            {'kty': 'RSA', 'n': 'n', 'e': 'e', 'x': 'x'},
            {'kty': 'EC', 'crv': 'P-256', 'x': 'x', 'y': 'y', 'n': 'n'},
            {'kty': 'EC', 'crv': 'P-256', 'x': 'x', 'y': 'y', 'e': None},
            {'kty': 'OKP', 'crv': 'Ed25519', 'x': 'x', 'y': 'y'},
            {'kty': 'OKP', 'crv': 'Ed25519', 'x': 'x', 'n': None},
        )
        for data in cases:
            with self.subTest(data=data), self.assertRaises(InvalidValueException):
                JsfPublicKey._from_dict(data)

    # -------------------------------------------------------------------------
    # Equality, Comparison, Hash & Sort Tests
    # -------------------------------------------------------------------------

    def test_same(self) -> None:
        key_1 = JsfPublicKey(kty=JsfKeyType.RSA, n='modulus', e='exponent')
        key_2 = JsfPublicKey(kty=JsfKeyType.RSA, n='modulus', e='exponent')

        self.assertNotEqual(id(key_1), id(key_2))
        self.assertEqual(hash(key_1), hash(key_2))
        self.assertTrue(key_1 == key_2)

    def test_not_same(self) -> None:
        key_1 = JsfPublicKey(kty=JsfKeyType.RSA, n='modulus1', e='exponent')
        key_2 = JsfPublicKey(kty=JsfKeyType.RSA, n='modulus2', e='exponent')

        self.assertNotEqual(hash(key_1), hash(key_2))
        self.assertFalse(key_1 == key_2)

    def test_compare_same_type(self) -> None:
        key_1 = JsfPublicKey(kty=JsfKeyType.RSA, n='modulus', e='exponent')
        key_2 = JsfPublicKey(kty=JsfKeyType.RSA, n='modulus', e='exponent')

        self.assertFalse(key_1 < key_2)

    def test_comparison(self) -> None:
        key_1 = JsfPublicKey(kty=JsfKeyType.RSA, n='a', e='exponent')
        key_2 = JsfPublicKey(kty=JsfKeyType.RSA, n='b', e='exponent')

        self.assertTrue(key_1 < key_2)

    def test_sort(self) -> None:
        expected_order = [2, 1, 0]
        keys = [
            JsfPublicKey(kty=JsfKeyType.RSA, n='c', e='exponent'),
            JsfPublicKey(kty=JsfKeyType.RSA, n='b', e='exponent'),
            JsfPublicKey(kty=JsfKeyType.RSA, n='a', e='exponent'),
        ]
        expected_keys = reorder(keys, expected_order)
        sorted_keys = sorted(keys)
        self.assertListEqual(sorted_keys, expected_keys)

    def test_repr(self) -> None:
        obj = JsfPublicKey(kty=JsfKeyType.RSA, n='modulus', e='exponent')
        self.assertIn('JsfPublicKey', repr(obj))


class TestJsfSimpleSignature(TestCase):

    def test_defaults(self) -> None:
        sig = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='val')
        self.assertIs(JsfAlgorithm.RS256, sig.algorithm)
        self.assertEqual(sig.value, 'val')
        self.assertIsNone(sig.key_id)
        self.assertIsNone(sig.public_key)
        self.assertEqual(sig.certificate_path, [])
        self.assertEqual(sig.excludes, [])

    def test_constructor(self) -> None:
        pk = JsfPublicKey(kty=JsfKeyType.RSA, n='modulus', e='exponent')
        sig = JsfSimpleSignature(
            algorithm=JsfAlgorithm.ES256,
            value='val',
            key_id='my-key',
            public_key=pk,
            certificate_path=['cert-a', 'cert-b'],
            excludes=['field1', 'field2'],
        )
        self.assertIs(JsfAlgorithm.ES256, sig.algorithm)
        self.assertEqual(sig.value, 'val')
        self.assertEqual(sig.key_id, 'my-key')
        self.assertEqual(sig.public_key, pk)
        # certificate_path/excludes are ordered lists -- order is preserved, not sorted
        self.assertEqual(sig.certificate_path, ['cert-a', 'cert-b'])
        self.assertEqual(sig.excludes, ['field1', 'field2'])

    def test_create(self) -> None:
        sig_rs = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='val1')
        proprietary_algorithm = XsUri('urn:ietf:rfc:8032')
        sig_proprietary = JsfSimpleSignature(algorithm=proprietary_algorithm, value='val2')
        self.assertIs(JsfAlgorithm.RS256, sig_rs.algorithm)
        self.assertEqual(proprietary_algorithm, sig_proprietary.algorithm)

    def test_update(self) -> None:
        sig = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='val')
        self.assertIs(JsfAlgorithm.RS256, sig.algorithm)
        sig.algorithm = JsfAlgorithm.ED25519
        self.assertIs(JsfAlgorithm.ED25519, sig.algorithm)

    def test_update_rejects_invalid_algorithm(self) -> None:
        sig = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='val')

        for algorithm in ('not-a-uri', JsfKeyType.RSA):
            with self.subTest(algorithm=algorithm), self.assertRaises(InvalidValueException):
                sig.algorithm = algorithm  # type: ignore[assignment]

        self.assertIs(JsfAlgorithm.RS256, sig.algorithm)

    def test_sort(self) -> None:
        expected_order = [1, 0]
        sigs = [
            JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='b'),
            JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='a'),
        ]
        expected_sigs = reorder(sigs, expected_order)
        sorted_sigs = sorted(sigs)
        self.assertListEqual(sorted_sigs, expected_sigs)

    def test_no_params(self) -> None:
        with self.assertRaises(TypeError):
            JsfSimpleSignature()

    def test_from_dict(self) -> None:
        self.assertIs(
            JsfAlgorithm.ES256,
            JsfSimpleSignature._from_dict({'algorithm': 'ES256', 'value': 'val'}).algorithm,
        )
        self.assertEqual(
            XsUri('urn:example:algorithm'),
            JsfSimpleSignature._from_dict({'algorithm': 'urn:example:algorithm', 'value': 'val'}).algorithm,
        )

    def test_proprietary_algorithm_requires_absolute_uri(self) -> None:
        with self.assertRaises(InvalidValueException):
            JsfSimpleSignature(algorithm=XsUri('relative-algorithm'), value='val')

    def test_same(self) -> None:
        sig_1 = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='val')
        sig_2 = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='val')

        self.assertNotEqual(id(sig_1), id(sig_2))
        self.assertEqual(hash(sig_1), hash(sig_2))
        self.assertTrue(sig_1 == sig_2)

    def test_not_same(self) -> None:
        sig_1 = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='a')
        sig_2 = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='b')

        self.assertNotEqual(hash(sig_1), hash(sig_2))
        self.assertFalse(sig_1 == sig_2)

    def test_unequal_different_type(self) -> None:
        sig = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='val')
        self.assertFalse(sig == 'other')

    def test_compare_same_type(self) -> None:
        sig_1 = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='val')
        sig_2 = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='val')

        self.assertFalse(sig_1 < sig_2)

    def test_comparison(self) -> None:
        sig_1 = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='a')
        sig_2 = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='b')

        self.assertTrue(sig_1 < sig_2)

    def test_repr(self) -> None:
        sig = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='val')
        self.assertIn(
            repr(sig),
            {
                '<JsfSimpleSignature algorithm=RS256>',
                '<JsfSimpleSignature algorithm=JsfAlgorithm.RS256>',
                "<JsfSimpleSignature algorithm=<JsfAlgorithm.RS256: 'RS256'>>"
            }
        )


class TestJsfSignatureSigners(TestCase):

    def test_no_params(self) -> None:
        with self.assertRaises(TypeError):
            JsfSignatureSigners()

    def test_empty_signers_allowed_by_schema(self) -> None:
        obj = JsfSignatureSigners._from_dict({'signers': []})

        self.assertEqual([], obj.signers)
        self.assertEqual({'signers': []}, obj._as_dict())

    def test_rejects_non_simple_signature(self) -> None:
        with self.assertRaisesRegex(InvalidValueException, 'signers must contain only JsfSimpleSignature instances'):
            JsfSignatureSigners(signers=[JsfSignatureChain(chain=[])])  # type: ignore[list-item]

    def test_defaults(self) -> None:
        sig = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='val')
        obj = JsfSignatureSigners(signers=[sig])
        self.assertEqual(list(obj.signers), [sig])

    def test_constructor(self) -> None:
        sigs = [
            JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='b'),
            JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='a'),
        ]
        obj = JsfSignatureSigners(signers=sigs)
        # signers is an ordered list -- input order is preserved, not sorted
        self.assertEqual(list(obj.signers), sigs)

    def test_sort(self) -> None:
        expected_order = [1, 0]
        objs = [
            JsfSignatureSigners(signers=[JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='b')]),
            JsfSignatureSigners(signers=[JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='a')]),
        ]
        expected_objs = reorder(objs, expected_order)
        sorted_objs = sorted(objs)
        self.assertListEqual(sorted_objs, expected_objs)

    def test_same(self) -> None:
        sig = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='val')
        obj_1 = JsfSignatureSigners(signers=[sig])
        obj_2 = JsfSignatureSigners(signers=[sig])

        self.assertNotEqual(id(obj_1), id(obj_2))
        self.assertEqual(hash(obj_1), hash(obj_2))
        self.assertTrue(obj_1 == obj_2)

    def test_not_same(self) -> None:
        obj_1 = JsfSignatureSigners(signers=[JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='a')])
        obj_2 = JsfSignatureSigners(signers=[JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='b')])

        self.assertNotEqual(hash(obj_1), hash(obj_2))
        self.assertFalse(obj_1 == obj_2)

    def test_unequal_different_type(self) -> None:
        obj = JsfSignatureSigners(signers=[JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='val')])
        self.assertFalse(obj == 'other')

    def test_compare_same_type(self) -> None:
        sig = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='val')
        obj_1 = JsfSignatureSigners(signers=[sig])
        obj_2 = JsfSignatureSigners(signers=[sig])

        self.assertFalse(obj_1 < obj_2)

    def test_comparison(self) -> None:
        sig_a = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='a')
        sig_b = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='b')
        obj_1 = JsfSignatureSigners(signers=[sig_a])
        obj_2 = JsfSignatureSigners(signers=[sig_b])

        self.assertTrue(obj_1 < obj_2)

    def test_hash(self) -> None:
        sig = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='val')
        self.assertEqual(
            hash(JsfSignatureSigners(signers=[sig])),
            hash(JsfSignatureSigners(signers=[sig])),
        )

    def test_repr(self) -> None:
        self.assertIn(
            'JsfSignatureSigners',
            repr(JsfSignatureSigners(signers=[JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='val')])),
        )


class TestJsfSignatureChain(TestCase):

    def test_no_params(self) -> None:
        with self.assertRaises(TypeError):
            JsfSignatureChain()

    def test_empty_chain_allowed_by_schema(self) -> None:
        obj = JsfSignatureChain._from_dict({'chain': []})

        self.assertEqual([], obj.chain)
        self.assertEqual({'chain': []}, obj._as_dict())

    def test_rejects_non_simple_signature(self) -> None:
        with self.assertRaisesRegex(InvalidValueException, 'chain must contain only JsfSimpleSignature instances'):
            JsfSignatureChain(chain=[JsfSignatureSigners(signers=[])])  # type: ignore[list-item]

    def test_defaults(self) -> None:
        sig = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='val')
        obj = JsfSignatureChain(chain=[sig])
        self.assertEqual(list(obj.chain), [sig])

    def test_constructor(self) -> None:
        sigs = [
            JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='b'),
            JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='a'),
        ]
        obj = JsfSignatureChain(chain=sigs)
        # chain is an ordered list -- per the JSF spec the first element must be the signature
        # certificate and the chain must stay contiguous, so input order is preserved, not sorted
        self.assertEqual(list(obj.chain), sigs)

    def test_sort(self) -> None:
        expected_order = [1, 0]
        objs = [
            JsfSignatureChain(chain=[JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='b')]),
            JsfSignatureChain(chain=[JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='a')]),
        ]
        expected_objs = reorder(objs, expected_order)
        sorted_objs = sorted(objs)
        self.assertListEqual(sorted_objs, expected_objs)

    def test_same(self) -> None:
        sig = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='val')
        obj_1 = JsfSignatureChain(chain=[sig])
        obj_2 = JsfSignatureChain(chain=[sig])

        self.assertNotEqual(id(obj_1), id(obj_2))
        self.assertEqual(hash(obj_1), hash(obj_2))
        self.assertTrue(obj_1 == obj_2)

    def test_not_same(self) -> None:
        obj_1 = JsfSignatureChain(chain=[JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='a')])
        obj_2 = JsfSignatureChain(chain=[JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='b')])

        self.assertNotEqual(hash(obj_1), hash(obj_2))
        self.assertFalse(obj_1 == obj_2)

    def test_unequal_different_type(self) -> None:
        obj = JsfSignatureChain(chain=[JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='val')])
        self.assertFalse(obj == 'other')

    def test_compare_same_type(self) -> None:
        sig = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='val')
        obj_1 = JsfSignatureChain(chain=[sig])
        obj_2 = JsfSignatureChain(chain=[sig])

        self.assertFalse(obj_1 < obj_2)

    def test_comparison(self) -> None:
        sig_a = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='a')
        sig_b = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='b')
        obj_1 = JsfSignatureChain(chain=[sig_a])
        obj_2 = JsfSignatureChain(chain=[sig_b])

        self.assertTrue(obj_1 < obj_2)

    def test_hash(self) -> None:
        sig = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='val')
        self.assertEqual(
            hash(JsfSignatureChain(chain=[sig])),
            hash(JsfSignatureChain(chain=[sig])),
        )

    def test_repr(self) -> None:
        self.assertIn(
            'JsfSignatureChain',
            repr(JsfSignatureChain(chain=[JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='val')])),
        )


class TestJsfSignaturePolymorphism(TestCase):
    """Tests for equality/ordering across the three JsfSignature subtypes via the shared base class."""

    def test_different_subtypes_are_not_equal(self) -> None:
        simple = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='val')
        signers = JsfSignatureSigners(signers=[simple])
        chain = JsfSignatureChain(chain=[simple])

        self.assertFalse(simple == signers)
        self.assertFalse(signers == chain)
        self.assertFalse(chain == simple)

    def test_sortable_across_subtypes(self) -> None:
        # This should not raise TypeError: '<' not supported between instances
        simple = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='val')
        signers = JsfSignatureSigners(signers=[simple])
        chain = JsfSignatureChain(chain=[simple])

        sorted_sigs = sorted([chain, simple, signers])
        self.assertEqual(len(sorted_sigs), 3)

    def test_unequal_different_type(self) -> None:
        simple = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='val')
        self.assertFalse(simple == 'other')

    def test_incomparable_type_raises(self) -> None:
        simple = JsfSimpleSignature(algorithm=JsfAlgorithm.RS256, value='val')
        with self.assertRaises(TypeError):
            r = simple < 'other'  # pylint: disable=unused-variable # noqa: disable=E841
