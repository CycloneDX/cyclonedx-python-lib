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

from datetime import datetime, timezone
from json import loads as json_loads
from unittest import TestCase
from xml.etree.ElementTree import fromstring as xml_fromstring

from cyclonedx.model import HashAlgorithm, HashType
from cyclonedx.model.bom_ref import BomRef
from cyclonedx.model.crypto import (
    AlgorithmProperties,
    CertificateCommonExtension,
    CertificateCommonExtensionName,
    CertificateCustomExtension,
    CertificateCustomState,
    CertificateLifecycleState,
    CertificatePredefinedState,
    CertificateProperties,
    CryptoPrimitive,
    Ikev2TransformTypes,
    ProtocolProperties,
    ProtocolPropertiesType,
    RelatedCryptographicAsset,
    RelatedCryptoMaterialProperties,
    RelatedCryptoMaterialSecuredBy,
    RelatedCryptoMaterialType,
)
from cyclonedx.schema.schema import SchemaVersion1Dot6, SchemaVersion1Dot7


class TestModelAlgorithmProperties(TestCase):

    def test_algorithm_properties_sorting(self) -> None:
        """Test that AlgorithmProperties instances can be sorted without triggering TypeError"""
        algo1 = AlgorithmProperties(primitive=CryptoPrimitive.HASH, classical_security_level=128)
        algo2 = AlgorithmProperties(primitive=CryptoPrimitive.SIGNATURE, classical_security_level=256)
        algo3 = AlgorithmProperties(primitive=CryptoPrimitive.BLOCK_CIPHER, classical_security_level=192)

        # This should not raise TypeError: '<' not supported between instances
        algo_list = [algo2, algo3, algo1]
        sorted_algos = sorted(algo_list)
        self.assertEqual(len(sorted_algos), 3)


class TestModelCertificateProperties(TestCase):

    def test_related_assets_are_gated_deterministic_and_preserve_deprecated_refs(self) -> None:
        algorithm = RelatedCryptographicAsset(type='algorithm', ref=BomRef('signature'))
        public_key = RelatedCryptographicAsset(type='publicKey', ref=BomRef('public-key'))
        properties = CertificateProperties(
            signature_algorithm_ref=BomRef('signature'),
            subject_public_key_ref=BomRef('public-key'),
            related_cryptographic_assets=[public_key, algorithm],
        )

        self.assertEqual([algorithm, public_key], list(properties.related_cryptographic_assets))
        self.assertNotEqual(properties, CertificateProperties())
        self.assertNotEqual(hash(properties), hash(CertificateProperties()))

        json_v1_6 = json_loads(properties.as_json(view_=SchemaVersion1Dot6))
        self.assertNotIn('relatedCryptographicAssets', json_v1_6)
        self.assertEqual('signature', json_v1_6['signatureAlgorithmRef'])
        self.assertEqual('public-key', json_v1_6['subjectPublicKeyRef'])

        json_v1_7 = json_loads(properties.as_json(view_=SchemaVersion1Dot7))
        self.assertEqual('signature', json_v1_7['signatureAlgorithmRef'])
        self.assertEqual('public-key', json_v1_7['subjectPublicKeyRef'])
        self.assertEqual(properties, CertificateProperties.from_json(json_v1_7))

        xml_v1_7 = xml_fromstring(properties.as_xml(view_=SchemaVersion1Dot7))
        self.assertEqual(properties, CertificateProperties.from_xml(xml_v1_7))

    def test_related_cryptographic_asset_comparison_and_hashing(self) -> None:
        first = RelatedCryptographicAsset(type='algorithm', ref=BomRef('a'))
        second = RelatedCryptographicAsset(type='publicKey', ref=BomRef('b'))

        self.assertNotEqual(first, second)
        self.assertNotEqual(hash(first), hash(second))
        self.assertEqual([first, second], sorted([second, first]))

    def test_certificate_extensions_are_gated_deterministic_and_round_trip(self) -> None:
        common = CertificateCommonExtension(
            common_extension_name=CertificateCommonExtensionName.KEY_USAGE,
            common_extension_value='digitalSignature',
        )
        custom = CertificateCustomExtension(
            custom_extension_name='1.2.3.4.5',
            custom_extension_value='custom-value',
        )
        properties = CertificateProperties(certificate_extensions=[custom, common])

        self.assertEqual([common, custom], list(properties.certificate_extensions))
        self.assertNotEqual(properties, CertificateProperties())
        self.assertNotEqual(hash(properties), hash(CertificateProperties()))
        self.assertNotIn('certificateExtensions', json_loads(properties.as_json(view_=SchemaVersion1Dot6)))

        json_v1_7 = json_loads(properties.as_json(view_=SchemaVersion1Dot7))
        from_json = CertificateProperties.from_json(json_v1_7)
        self.assertEqual(properties, from_json)
        self.assertEqual(
            {CertificateCommonExtension, CertificateCustomExtension},
            {type(extension) for extension in from_json.certificate_extensions},
        )

        xml_v1_7 = xml_fromstring(properties.as_xml(view_=SchemaVersion1Dot7))
        from_xml = CertificateProperties.from_xml(xml_v1_7)
        self.assertEqual(properties, from_xml)
        self.assertEqual(
            {CertificateCommonExtension, CertificateCustomExtension},
            {type(extension) for extension in from_xml.certificate_extensions},
        )

    def test_lifecycle_dates_are_gated_ordered_and_round_trip(self) -> None:
        properties = CertificateProperties(
            creation_date=datetime(2023, 5, 18, 12, 0, tzinfo=timezone.utc),
            activation_date=datetime(2023, 5, 19, 1, 0, tzinfo=timezone.utc),
            deactivation_date=datetime(2024, 5, 18, 12, 0, tzinfo=timezone.utc),
            revocation_date=datetime(2024, 5, 18, 13, 0, tzinfo=timezone.utc),
            destruction_date=datetime(2024, 5, 18, 14, 0, tzinfo=timezone.utc),
        )

        lifecycle_names = [
            'creationDate',
            'activationDate',
            'deactivationDate',
            'revocationDate',
            'destructionDate',
        ]
        json_v1_6 = json_loads(properties.as_json(view_=SchemaVersion1Dot6))
        self.assertTrue(all(name not in json_v1_6 for name in lifecycle_names))
        self.assertNotEqual(properties, CertificateProperties())
        self.assertNotEqual(hash(properties), hash(CertificateProperties()))

        json_v1_7 = json_loads(properties.as_json(view_=SchemaVersion1Dot7))
        self.assertEqual(properties, CertificateProperties.from_json(json_v1_7))

        xml_v1_7 = xml_fromstring(properties.as_xml(view_=SchemaVersion1Dot7))
        self.assertEqual(lifecycle_names, [child.tag for child in xml_v1_7])
        self.assertEqual(properties, CertificateProperties.from_xml(xml_v1_7))

    def test_certificate_states_are_gated_deterministic_and_round_trip(self) -> None:
        predefined = CertificatePredefinedState(
            state=CertificateLifecycleState.ACTIVE,
            reason='in use',
        )
        custom = CertificateCustomState(
            name='pending-rotation',
            description='custom state',
            reason='scheduled maintenance',
        )
        properties = CertificateProperties(certificate_states=[predefined, custom])

        self.assertEqual([custom, predefined], list(properties.certificate_states))
        self.assertNotEqual(properties, CertificateProperties())
        self.assertNotEqual(hash(properties), hash(CertificateProperties()))
        self.assertNotIn('certificateState', json_loads(properties.as_json(view_=SchemaVersion1Dot6)))

        json_v1_7 = json_loads(properties.as_json(view_=SchemaVersion1Dot7))
        from_json = CertificateProperties.from_json(json_v1_7)
        self.assertEqual(properties, from_json)
        self.assertEqual(
            {CertificateCustomState, CertificatePredefinedState},
            {type(state) for state in from_json.certificate_states},
        )

        xml_v1_7 = xml_fromstring(properties.as_xml(view_=SchemaVersion1Dot7))
        from_xml = CertificateProperties.from_xml(xml_v1_7)
        self.assertEqual(properties, from_xml)
        self.assertEqual(
            {CertificateCustomState, CertificatePredefinedState},
            {type(state) for state in from_xml.certificate_states},
        )

    def test_fingerprint_version_gating_comparison_and_round_trip(self) -> None:
        fingerprint = HashType(alg=HashAlgorithm.SHA_256, content='a' * 64)
        properties = CertificateProperties(fingerprint=fingerprint)

        self.assertNotEqual(properties, CertificateProperties())
        self.assertNotEqual(hash(properties), hash(CertificateProperties()))
        self.assertNotIn('fingerprint', json_loads(properties.as_json(view_=SchemaVersion1Dot6)))

        json_v1_7 = json_loads(properties.as_json(view_=SchemaVersion1Dot7))
        self.assertEqual(properties, CertificateProperties.from_json(json_v1_7))
        xml_v1_7 = xml_fromstring(properties.as_xml(view_=SchemaVersion1Dot7))
        self.assertEqual(properties, CertificateProperties.from_xml(xml_v1_7))

    def test_certificate_file_extension_preserves_deprecated_extension(self) -> None:
        properties = CertificateProperties(
            certificate_extension='crt',
            certificate_file_extension='pem',
        )

        json_v1_6 = json_loads(properties.as_json(view_=SchemaVersion1Dot6))
        json_v1_7 = json_loads(properties.as_json(view_=SchemaVersion1Dot7))
        self.assertEqual('crt', json_v1_6['certificateExtension'])
        self.assertNotIn('certificateFileExtension', json_v1_6)
        self.assertEqual('crt', json_v1_7['certificateExtension'])
        self.assertEqual('pem', json_v1_7['certificateFileExtension'])
        self.assertEqual(properties, CertificateProperties.from_json(json_v1_7))

        xml_v1_7 = xml_fromstring(properties.as_xml(view_=SchemaVersion1Dot7))
        self.assertEqual(properties, CertificateProperties.from_xml(xml_v1_7))

    def test_serial_number_construction_and_comparison(self) -> None:
        first = CertificateProperties(serial_number='1')
        second = CertificateProperties(serial_number='2')

        self.assertEqual('1', first.serial_number)
        self.assertNotEqual(first, second)
        self.assertNotEqual(hash(first), hash(second))
        self.assertEqual([first, second], sorted([second, first]))

    def test_serial_number_version_gating_and_round_trip(self) -> None:
        properties = CertificateProperties(serial_number='3942447fac867ae5cdb3229b658f4d48')

        json_v1_6 = json_loads(properties.as_json(view_=SchemaVersion1Dot6))
        json_v1_7 = json_loads(properties.as_json(view_=SchemaVersion1Dot7))
        self.assertNotIn('serialNumber', json_v1_6)
        self.assertEqual(properties.serial_number, json_v1_7['serialNumber'])
        self.assertEqual(properties, CertificateProperties.from_json(json_v1_7))

        xml_v1_7 = xml_fromstring(properties.as_xml(view_=SchemaVersion1Dot7))
        self.assertEqual(properties, CertificateProperties.from_xml(xml_v1_7))

    def test_certificate_properties_sorting(self) -> None:
        """Test that CertificateProperties instances can be sorted without triggering TypeError"""
        cert1 = CertificateProperties(subject_name='CN=Test1', certificate_format='X.509')
        cert2 = CertificateProperties(subject_name='CN=Test2', certificate_format='PEM')
        cert3 = CertificateProperties(subject_name='CN=Test3', certificate_format='DER')

        # This should not raise TypeError: '<' not supported between instances
        cert_list = [cert2, cert3, cert1]
        sorted_certs = sorted(cert_list)
        self.assertEqual(len(sorted_certs), 3)


class TestModelRelatedCryptoMaterialSecuredBy(TestCase):

    def test_related_crypto_material_secured_by_sorting(self) -> None:
        """Test that RelatedCryptoMaterialSecuredBy instances can be sorted without triggering TypeError"""
        secured1 = RelatedCryptoMaterialSecuredBy(mechanism='HSM', algorithm_ref=BomRef('algo1'))
        secured2 = RelatedCryptoMaterialSecuredBy(mechanism='TPM', algorithm_ref=BomRef('algo2'))
        secured3 = RelatedCryptoMaterialSecuredBy(mechanism='Software', algorithm_ref=BomRef('algo3'))

        # This should not raise TypeError: '<' not supported between instances
        secured_list = [secured3, secured1, secured2]
        sorted_secured = sorted(secured_list)
        self.assertEqual(len(sorted_secured), 3)


class TestModelRelatedCryptoMaterialProperties(TestCase):

    def test_related_assets_are_gated_deterministic_and_preserve_deprecated_refs(self) -> None:
        related_asset = RelatedCryptographicAsset(type='algorithm', ref=BomRef('material-algorithm'))
        properties = RelatedCryptoMaterialProperties(
            algorithm_ref=BomRef('material-algorithm'),
            secured_by=RelatedCryptoMaterialSecuredBy(
                mechanism='HSM',
                algorithm_ref=BomRef('securing-algorithm'),
            ),
            related_cryptographic_assets=[related_asset],
        )

        self.assertEqual([related_asset], list(properties.related_cryptographic_assets))
        self.assertNotEqual(properties, RelatedCryptoMaterialProperties())
        self.assertNotEqual(hash(properties), hash(RelatedCryptoMaterialProperties()))

        json_v1_6 = json_loads(properties.as_json(view_=SchemaVersion1Dot6))
        self.assertNotIn('relatedCryptographicAssets', json_v1_6)
        self.assertEqual('material-algorithm', json_v1_6['algorithmRef'])
        self.assertEqual('securing-algorithm', json_v1_6['securedBy']['algorithmRef'])

        json_v1_7 = json_loads(properties.as_json(view_=SchemaVersion1Dot7))
        self.assertEqual('material-algorithm', json_v1_7['algorithmRef'])
        self.assertEqual('securing-algorithm', json_v1_7['securedBy']['algorithmRef'])
        self.assertEqual(properties, RelatedCryptoMaterialProperties.from_json(json_v1_7))

        xml_v1_7 = xml_fromstring(properties.as_xml(view_=SchemaVersion1Dot7))
        self.assertEqual(properties, RelatedCryptoMaterialProperties.from_xml(xml_v1_7))

    def test_fingerprint_version_gating_comparison_and_round_trip(self) -> None:
        fingerprint = HashType(alg=HashAlgorithm.SHA_256, content='b' * 64)
        properties = RelatedCryptoMaterialProperties(fingerprint=fingerprint)

        self.assertNotEqual(properties, RelatedCryptoMaterialProperties())
        self.assertNotEqual(hash(properties), hash(RelatedCryptoMaterialProperties()))
        self.assertNotIn('fingerprint', json_loads(properties.as_json(view_=SchemaVersion1Dot6)))

        json_v1_7 = json_loads(properties.as_json(view_=SchemaVersion1Dot7))
        self.assertEqual(properties, RelatedCryptoMaterialProperties.from_json(json_v1_7))
        xml_v1_7 = xml_fromstring(properties.as_xml(view_=SchemaVersion1Dot7))
        self.assertEqual(properties, RelatedCryptoMaterialProperties.from_xml(xml_v1_7))

    def test_related_crypto_material_properties_sorting(self) -> None:
        """Test that RelatedCryptoMaterialProperties instances can be sorted without triggering TypeError"""
        material1 = RelatedCryptoMaterialProperties(
            type=RelatedCryptoMaterialType.KEY,
            id='key1',
            size=256
        )
        material2 = RelatedCryptoMaterialProperties(
            type=RelatedCryptoMaterialType.PRIVATE_KEY,
            id='key2',
            size=512
        )
        material3 = RelatedCryptoMaterialProperties(
            type=RelatedCryptoMaterialType.PUBLIC_KEY,
            id='key3',
            size=1024
        )

        # This should not raise TypeError: '<' not supported between instances
        material_list = [material3, material1, material2]
        sorted_materials = sorted(material_list)
        self.assertEqual(len(sorted_materials), 3)


class TestModelIkev2TransformTypes(TestCase):

    def test_ikev2_transform_types_sorting(self) -> None:
        """Test that Ikev2TransformTypes instances can be sorted without triggering TypeError"""
        ikev2_1 = Ikev2TransformTypes(
            encr=[BomRef('encr1')],
            esn=True
        )
        ikev2_2 = Ikev2TransformTypes(
            encr=[BomRef('encr2')],
            esn=False
        )
        ikev2_3 = Ikev2TransformTypes(
            encr=[BomRef('encr3')],
            esn=True
        )

        # This should not raise TypeError: '<' not supported between instances
        ikev2_list = [ikev2_3, ikev2_1, ikev2_2]
        sorted_ikev2 = sorted(ikev2_list)
        self.assertEqual(len(sorted_ikev2), 3)


class TestModelProtocolProperties(TestCase):

    def test_protocol_properties_sorting(self) -> None:
        """Test that ProtocolProperties instances can be sorted without triggering TypeError"""
        proto1 = ProtocolProperties(type=ProtocolPropertiesType.TLS, version='1.2')
        proto2 = ProtocolProperties(type=ProtocolPropertiesType.SSH, version='2.0')
        proto3 = ProtocolProperties(type=ProtocolPropertiesType.IPSEC, version='1.0')

        # This should not raise TypeError: '<' not supported between instances
        proto_list = [proto3, proto1, proto2]
        sorted_protos = sorted(proto_list)
        self.assertEqual(len(sorted_protos), 3)
