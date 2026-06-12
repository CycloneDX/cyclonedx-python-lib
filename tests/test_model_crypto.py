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

from cyclonedx.model.bom_ref import BomRef
from cyclonedx.model.crypto import (
    AlgorithmProperties,
    CertificateProperties,
    CryptoPrimitive,
    Ikev2TransformTypes,
    ProtocolProperties,
    ProtocolPropertiesType,
    RelatedCryptoMaterialProperties,
    RelatedCryptoMaterialSecuredBy,
    RelatedCryptoMaterialType,
)


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
