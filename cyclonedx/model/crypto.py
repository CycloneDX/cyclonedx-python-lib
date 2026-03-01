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

"""
This set of classes represents cryptoPropertiesType Complex Type in the CycloneDX standard.

.. note::
    Introduced in CycloneDX v1.6

.. note::
    See the CycloneDX Schema for hashType: https://cyclonedx.org/docs/1.7/xml/#type_cryptoPropertiesType
"""

from collections.abc import Iterable
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from attrs import Factory, define, field
from sortedcontainers import SortedSet

from .._internal.compare import ComparableTuple as _ComparableTuple
from ..exception.model import InvalidNistQuantumSecurityLevelException, InvalidRelatedCryptoMaterialSizeException
from ..schema import SchemaVersion
from .bom_ref import BomRef


def _sortedset_converter(value: Any) -> SortedSet:
    if value is None:
        return SortedSet()
    if isinstance(value, SortedSet):
        return value
    return SortedSet(value)


class CryptoAssetType(str, Enum):
    """
    This is our internal representation of the cryptoPropertiesType.assetType ENUM type within the CycloneDX standard.

    .. note::
        Introduced in CycloneDX v1.6
    """

    ALGORITHM = 'algorithm'
    CERTIFICATE = 'certificate'
    PROTOCOL = 'protocol'
    RELATED_CRYPTO_MATERIAL = 'related-crypto-material'


class CryptoPrimitive(str, Enum):
    """
    This is our internal representation of the cryptoPropertiesType.algorithmProperties.primitive ENUM type.

    .. note::
        Introduced in CycloneDX v1.6
    """

    AE = 'ae'
    BLOCK_CIPHER = 'block-cipher'
    COMBINER = 'combiner'
    DRBG = 'drbg'
    HASH = 'hash'
    KDF = 'kdf'
    KEM = 'kem'
    KEY_AGREE = 'key-agree'
    MAC = 'mac'
    PKE = 'pke'
    SIGNATURE = 'signature'
    STREAM_CIPHER = 'stream-cipher'
    XOF = 'xof'

    OTHER = 'other'
    UNKNOWN = 'unknown'


class CryptoExecutionEnvironment(str, Enum):
    """
    This is our internal representation of the cryptoPropertiesType.algorithmProperties.executionEnvironment ENUM type.

    .. note::
        Introduced in CycloneDX v1.6
    """

    SOFTWARE_PLAIN_RAM = 'software-plain-ram'
    SOFTWARE_ENCRYPTED_RAM = 'software-encrypted-ram'
    SOFTWARE_TEE = 'software-tee'
    HARDWARE = 'hardware'

    OTHER = 'other'
    UNKNOWN = 'unknown'


class CryptoImplementationPlatform(str, Enum):
    """
    This is our internal representation of the cryptoPropertiesType.algorithmProperties.implementationPlatform ENUM.

    .. note::
        Introduced in CycloneDX v1.6
    """

    GENERIC = 'generic'
    X86_32 = 'x86_32'
    X86_64 = 'x86_64'
    ARM_V7_A = 'armv7-a'
    ARM_V7_M = 'armv7-m'
    ARM_V8_A = 'armv8-a'
    ARM_V8_M = 'armv8-m'
    ARM_V9_A = 'armv9-a'
    ARM_V9_M = 'armv9-m'
    S390X = 's390x'
    PPC64 = 'ppc64'
    PPC64LE = 'ppc64le'

    OTHER = 'other'
    UNKNOWN = 'unknown'


class CryptoCertificationLevel(str, Enum):
    """
    This is our internal representation of the cryptoPropertiesType.algorithmProperties.certificationLevel ENUM.

    .. note::
        Introduced in CycloneDX v1.6
    """

    NONE = 'none'
    FIPS_140_1_L1 = 'fips140-1-l1'
    FIPS_140_1_L2 = 'fips140-1-l2'
    FIPS_140_1_L3 = 'fips140-1-l3'
    FIPS_140_1_L4 = 'fips140-1-l4'
    FIPS_140_2_L1 = 'fips140-2-l1'
    FIPS_140_2_L2 = 'fips140-2-l2'
    FIPS_140_2_L3 = 'fips140-2-l3'
    FIPS_140_2_L4 = 'fips140-2-l4'
    FIPS_140_3_L1 = 'fips140-3-l1'
    FIPS_140_3_L2 = 'fips140-3-l2'
    FIPS_140_3_L3 = 'fips140-3-l3'
    FIPS_140_3_L4 = 'fips140-3-l4'
    CC_EAL1 = 'cc-eal1'
    CC_EAL1_PLUS = 'cc-eal1+'
    CC_EAL2 = 'cc-eal2'
    CC_EAL2_PLUS = 'cc-eal2+'
    CC_EAL3 = 'cc-eal3'
    CC_EAL3_PLUS = 'cc-eal3+'
    CC_EAL4 = 'cc-eal4'
    CC_EAL4_PLUS = 'cc-eal4+'
    CC_EAL5 = 'cc-eal5'
    CC_EAL5_PLUS = 'cc-eal5+'
    CC_EAL6 = 'cc-eal6'
    CC_EAL6_PLUS = 'cc-eal6+'
    CC_EAL7 = 'cc-eal7'
    CC_EAL7_PLUS = 'cc-eal7+'

    OTHER = 'other'
    UNKNOWN = 'unknown'


class CryptoMode(str, Enum):
    """
    This is our internal representation of the cryptoPropertiesType.algorithmProperties.mode ENUM type.

    .. note::
        Introduced in CycloneDX v1.6
    """

    CBC = 'cbc'
    ECB = 'ecb'
    CCM = 'ccm'
    GCM = 'gcm'
    CFB = 'cfb'
    OFB = 'ofb'
    CTR = 'ctr'

    OTHER = 'other'
    UNKNOWN = 'unknown'


class CryptoPadding(str, Enum):
    """
    This is our internal representation of the cryptoPropertiesType.algorithmProperties.padding ENUM type.

    .. note::
        Introduced in CycloneDX v1.6
    """

    PKCS5 = 'pkcs5'
    PKCS7 = 'pkcs7'
    PKCS1_V15 = 'pkcs1v15'
    OAEP = 'oaep'
    RAW = 'raw'

    OTHER = 'other'
    UNKNOWN = 'unknown'


class CryptoFunction(str, Enum):
    """
    This is our internal representation of the cryptoPropertiesType.algorithmProperties.cryptoFunctions ENUM.

    .. note::
        Introduced in CycloneDX v1.6
    """

    GENERATE = 'generate'
    KEYGEN = 'keygen'
    ENCRYPT = 'encrypt'
    DECRYPT = 'decrypt'
    DIGEST = 'digest'
    TAG = 'tag'
    KEYDERIVE = 'keyderive'
    SIGN = 'sign'
    VERIFY = 'verify'
    ENCAPSULATE = 'encapsulate'
    DECAPSULATE = 'decapsulate'

    OTHER = 'other'
    UNKNOWN = 'unknown'


@define
class AlgorithmProperties:
    """
    This is our internal representation of the cryptoPropertiesType.algorithmProperties complex type.

    .. note::
        Introduced in CycloneDX v1.6
    """

    primitive: Optional[CryptoPrimitive] = field(
        default=None,
        metadata={'json_name': 'primitive', 'xml_name': 'primitive', 'xml_sequence': 1,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    parameter_set_identifier: Optional[str] = field(
        default=None,
        metadata={'json_name': 'parameterSetIdentifier', 'xml_name': 'parameterSetIdentifier', 'xml_sequence': 2,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    curve: Optional[str] = field(
        default=None,
        metadata={'json_name': 'curve', 'xml_name': 'curve', 'xml_sequence': 3,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    execution_environment: Optional[CryptoExecutionEnvironment] = field(
        default=None,
        metadata={'json_name': 'executionEnvironment', 'xml_name': 'executionEnvironment', 'xml_sequence': 4,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    implementation_platform: Optional[CryptoImplementationPlatform] = field(
        default=None,
        metadata={'json_name': 'implementationPlatform', 'xml_name': 'implementationPlatform', 'xml_sequence': 5,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    _certification_levels: 'SortedSet[CryptoCertificationLevel]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'certificationLevel', 'xml_name': 'certificationLevel', 'xml_sequence': 6,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    mode: Optional[CryptoMode] = field(
        default=None,
        metadata={'json_name': 'mode', 'xml_name': 'mode', 'xml_sequence': 7,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    padding: Optional[CryptoPadding] = field(
        default=None,
        metadata={'json_name': 'padding', 'xml_name': 'padding', 'xml_sequence': 8,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    _crypto_functions: 'SortedSet[CryptoFunction]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'cryptoFunctions', 'xml_name': 'cryptoFunctions', 'xml_item_name': 'cryptoFunction',
                  'xml_sequence': 9, 'min_schema_version': SchemaVersion.V1_6}
    )

    classical_security_level: Optional[int] = field(
        default=None,
        metadata={'json_name': 'classicalSecurityLevel', 'xml_name': 'classicalSecurityLevel', 'xml_sequence': 10,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    _nist_quantum_security_level: Optional[int] = field(
        default=None,
        metadata={'json_name': 'nistQuantumSecurityLevel', 'xml_name': 'nistQuantumSecurityLevel', 'xml_sequence': 11,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    @property
    def certification_levels(self) -> 'SortedSet[CryptoCertificationLevel]':
        return self._certification_levels

    @certification_levels.setter
    def certification_levels(self, certification_levels: Iterable[CryptoCertificationLevel]) -> None:
        self._certification_levels = SortedSet(certification_levels)

    @property
    def crypto_functions(self) -> 'SortedSet[CryptoFunction]':
        return self._crypto_functions

    @crypto_functions.setter
    def crypto_functions(self, crypto_functions: Iterable[CryptoFunction]) -> None:
        self._crypto_functions = SortedSet(crypto_functions)

    @property
    def nist_quantum_security_level(self) -> Optional[int]:
        return self._nist_quantum_security_level

    @nist_quantum_security_level.setter
    def nist_quantum_security_level(self, nist_quantum_security_level: Optional[int]) -> None:
        if nist_quantum_security_level is not None and not (0 <= nist_quantum_security_level <= 6):
            raise InvalidNistQuantumSecurityLevelException(
                f'nist_quantum_security_level must be between 0 and 6. Got: {nist_quantum_security_level}')
        self._nist_quantum_security_level = nist_quantum_security_level

    def __hash__(self) -> int:
        return hash((self.primitive, self.parameter_set_identifier, self.curve, self.execution_environment,
                     self.implementation_platform, self.mode, self.padding, self.classical_security_level,
                     self.nist_quantum_security_level))

    @staticmethod
    def _cmp(val: Any) -> tuple:
        """Wrap value for None-safe comparison (None sorts last)."""
        return (0, val) if val is not None else (1, '')

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, AlgorithmProperties):
            return (self._cmp(self.primitive), self._cmp(self.parameter_set_identifier),
                    self._cmp(self.curve)) < (
                self._cmp(other.primitive), self._cmp(other.parameter_set_identifier),
                self._cmp(other.curve))
        return NotImplemented


@define
class CertificateProperties:
    """
    This is our internal representation of the cryptoPropertiesType.certificateProperties complex type.

    .. note::
        Introduced in CycloneDX v1.6
    """

    subject_name: Optional[str] = field(
        default=None,
        metadata={'json_name': 'subjectName', 'xml_name': 'subjectName', 'xml_sequence': 1,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    issuer_name: Optional[str] = field(
        default=None,
        metadata={'json_name': 'issuerName', 'xml_name': 'issuerName', 'xml_sequence': 2,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    not_valid_before: Optional[datetime] = field(
        default=None,
        metadata={'json_name': 'notValidBefore', 'xml_name': 'notValidBefore', 'xml_sequence': 3,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    not_valid_after: Optional[datetime] = field(
        default=None,
        metadata={'json_name': 'notValidAfter', 'xml_name': 'notValidAfter', 'xml_sequence': 4,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    signature_algorithm_ref: Optional[BomRef] = field(
        default=None,
        metadata={'json_name': 'signatureAlgorithmRef', 'xml_name': 'signatureAlgorithmRef', 'xml_sequence': 5,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    subject_public_key_ref: Optional[BomRef] = field(
        default=None,
        metadata={'json_name': 'subjectPublicKeyRef', 'xml_name': 'subjectPublicKeyRef', 'xml_sequence': 6,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    certificate_format: Optional[str] = field(
        default=None,
        metadata={'json_name': 'certificateFormat', 'xml_name': 'certificateFormat', 'xml_sequence': 7,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    certificate_extension: Optional[str] = field(
        default=None,
        metadata={'json_name': 'certificateExtension', 'xml_name': 'certificateExtension', 'xml_sequence': 8,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    def __hash__(self) -> int:
        return hash((self.subject_name, self.issuer_name, self.not_valid_before, self.not_valid_after))

    @staticmethod
    def _cmp(val: Any) -> tuple:
        """Wrap value for None-safe comparison (None sorts last)."""
        return (0, val) if val is not None else (1, '')

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, CertificateProperties):
            return (self._cmp(self.subject_name), self._cmp(self.issuer_name)) < (
                self._cmp(other.subject_name), self._cmp(other.issuer_name))
        return NotImplemented


class RelatedCryptoMaterialType(str, Enum):
    """
    This is our internal representation of the cryptoPropertiesType.relatedCryptoMaterialProperties.type ENUM.

    .. note::
        Introduced in CycloneDX v1.6
    """

    PRIVATE_KEY = 'private-key'
    PUBLIC_KEY = 'public-key'
    SECRET_KEY = 'secret-key'
    KEY = 'key'
    CIPHERTEXT = 'ciphertext'
    SIGNATURE = 'signature'
    DIGEST = 'digest'
    INITIALIZATION_VECTOR = 'initialization-vector'
    NONCE = 'nonce'
    SEED = 'seed'
    SALT = 'salt'
    SHARED_SECRET = 'shared-secret'
    TAG = 'tag'
    ADDITIONAL_DATA = 'additional-data'
    PASSWORD = 'password'
    CREDENTIAL = 'credential'
    TOKEN = 'token'
    OTHER = 'other'
    UNKNOWN = 'unknown'


class RelatedCryptoMaterialState(str, Enum):
    """
    This is our internal representation of the cryptoPropertiesType.relatedCryptoMaterialProperties.state ENUM.

    .. note::
        Introduced in CycloneDX v1.6
    """

    PRE_ACTIVATION = 'pre-activation'
    ACTIVE = 'active'
    SUSPENDED = 'suspended'
    DEACTIVATED = 'deactivated'
    COMPROMISED = 'compromised'
    DESTROYED = 'destroyed'


@define
class RelatedCryptoMaterialSecuredBy:
    """
    This is our internal representation of the cryptoPropertiesType.relatedCryptoMaterialProperties.securedBy type.

    .. note::
        Introduced in CycloneDX v1.6
    """

    mechanism: Optional[str] = field(
        default=None,
        metadata={'json_name': 'mechanism', 'xml_name': 'mechanism', 'xml_sequence': 1,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    algorithm_ref: Optional[BomRef] = field(
        default=None,
        metadata={'json_name': 'algorithmRef', 'xml_name': 'algorithmRef', 'xml_sequence': 2,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    def __hash__(self) -> int:
        return hash((self.mechanism, self.algorithm_ref))

    @staticmethod
    def _cmp(val: Any) -> tuple:
        """Wrap value for None-safe comparison (None sorts last)."""
        return (0, val) if val is not None else (1, '')

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, RelatedCryptoMaterialSecuredBy):
            return (self._cmp(self.mechanism), self._cmp(self.algorithm_ref)) < (
                self._cmp(other.mechanism), self._cmp(other.algorithm_ref))
        return NotImplemented


@define
class RelatedCryptoMaterialProperties:
    """
    This is our internal representation of the cryptoPropertiesType.relatedCryptoMaterialProperties complex type.

    .. note::
        Introduced in CycloneDX v1.6
    """

    type: Optional[RelatedCryptoMaterialType] = field(
        default=None,
        metadata={'json_name': 'type', 'xml_name': 'type', 'xml_sequence': 1,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    id: Optional[str] = field(
        default=None,
        metadata={'json_name': 'id', 'xml_name': 'id', 'xml_sequence': 2,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    state: Optional[RelatedCryptoMaterialState] = field(
        default=None,
        metadata={'json_name': 'state', 'xml_name': 'state', 'xml_sequence': 3,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    algorithm_ref: Optional[BomRef] = field(
        default=None,
        metadata={'json_name': 'algorithmRef', 'xml_name': 'algorithmRef', 'xml_sequence': 4,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    creation_date: Optional[datetime] = field(
        default=None,
        metadata={'json_name': 'creationDate', 'xml_name': 'creationDate', 'xml_sequence': 5,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    activation_date: Optional[datetime] = field(
        default=None,
        metadata={'json_name': 'activationDate', 'xml_name': 'activationDate', 'xml_sequence': 6,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    update_date: Optional[datetime] = field(
        default=None,
        metadata={'json_name': 'updateDate', 'xml_name': 'updateDate', 'xml_sequence': 7,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    expiration_date: Optional[datetime] = field(
        default=None,
        metadata={'json_name': 'expirationDate', 'xml_name': 'expirationDate', 'xml_sequence': 8,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    value: Optional[str] = field(
        default=None,
        metadata={'json_name': 'value', 'xml_name': 'value', 'xml_sequence': 9,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    _size: Optional[int] = field(
        default=None,
        metadata={'json_name': 'size', 'xml_name': 'size', 'xml_sequence': 10,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    format: Optional[str] = field(
        default=None,
        metadata={'json_name': 'format', 'xml_name': 'format', 'xml_sequence': 11,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    secured_by: Optional[RelatedCryptoMaterialSecuredBy] = field(
        default=None,
        metadata={'json_name': 'securedBy', 'xml_name': 'securedBy', 'xml_sequence': 12,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    @property
    def size(self) -> Optional[int]:
        return self._size

    @size.setter
    def size(self, size: Optional[int]) -> None:
        if size is not None and size <= 0:
            raise InvalidRelatedCryptoMaterialSizeException(
                f'size must be a positive integer. Got: {size}')
        self._size = size

    def __hash__(self) -> int:
        return hash((self.type, self.id, self.state, self.algorithm_ref))

    @staticmethod
    def _cmp(val: Any) -> tuple:
        """Wrap value for None-safe comparison (None sorts last)."""
        return (0, val) if val is not None else (1, '')

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, RelatedCryptoMaterialProperties):
            return (self._cmp(self.type), self._cmp(self.id), self._cmp(self.state)) < (
                self._cmp(other.type), self._cmp(other.id), self._cmp(other.state))
        return NotImplemented


class ProtocolPropertiesType(str, Enum):
    """
    This is our internal representation of the cryptoPropertiesType.protocolProperties.type ENUM type.

    .. note::
        Introduced in CycloneDX v1.6
    """

    TLS = 'tls'
    SSH = 'ssh'
    IPSEC = 'ipsec'
    IKE = 'ike'
    SSTP = 'sstp'
    WPA = 'wpa'

    OTHER = 'other'
    UNKNOWN = 'unknown'


@define
class ProtocolPropertiesCipherSuite:
    """
    This is our internal representation of the cryptoPropertiesType.protocolProperties.cipherSuites complex type.

    .. note::
        Introduced in CycloneDX v1.6
    """

    name: Optional[str] = field(
        default=None,
        metadata={'json_name': 'name', 'xml_name': 'name', 'xml_sequence': 1,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    _algorithms: 'SortedSet[BomRef]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'algorithms', 'xml_name': 'algorithms', 'xml_item_name': 'algorithm',
                  'xml_sequence': 2, 'min_schema_version': SchemaVersion.V1_6}
    )

    _identifiers: 'SortedSet[str]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'identifiers', 'xml_name': 'identifiers', 'xml_item_name': 'identifier',
                  'xml_sequence': 3, 'min_schema_version': SchemaVersion.V1_6}
    )

    @property
    def algorithms(self) -> 'SortedSet[BomRef]':
        return self._algorithms

    @algorithms.setter
    def algorithms(self, algorithms: Iterable[BomRef]) -> None:
        self._algorithms = SortedSet(algorithms)

    @property
    def identifiers(self) -> 'SortedSet[str]':
        return self._identifiers

    @identifiers.setter
    def identifiers(self, identifiers: Iterable[str]) -> None:
        self._identifiers = SortedSet(identifiers)

    def __hash__(self) -> int:
        return hash(self.name)

    @staticmethod
    def _cmp(val: Any) -> tuple:
        """Wrap value for None-safe comparison (None sorts last)."""
        return (0, val) if val is not None else (1, '')

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, ProtocolPropertiesCipherSuite):
            return self._cmp(self.name) < self._cmp(other.name)
        return NotImplemented


@define
class Ikev2TransformTypes:
    """
    This is our internal representation of the cryptoPropertiesType.protocolProperties.ikev2TransformTypes.

    .. note::
        Introduced in CycloneDX v1.6
    """

    _encr: 'SortedSet[BomRef]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'encr', 'xml_name': 'encr', 'xml_item_name': 'ref', 'xml_sequence': 1,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    _prf: 'SortedSet[BomRef]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'prf', 'xml_name': 'prf', 'xml_item_name': 'ref', 'xml_sequence': 2,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    _integ: 'SortedSet[BomRef]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'integ', 'xml_name': 'integ', 'xml_item_name': 'ref', 'xml_sequence': 3,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    _ke: 'SortedSet[BomRef]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'ke', 'xml_name': 'ke', 'xml_item_name': 'ref', 'xml_sequence': 4,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    _esn: bool = field(
        default=False,
        metadata={'json_name': 'esn', 'xml_name': 'esn', 'xml_sequence': 5,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    _auth: 'SortedSet[BomRef]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'auth', 'xml_name': 'auth', 'xml_item_name': 'ref', 'xml_sequence': 6,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    @property
    def encr(self) -> 'SortedSet[BomRef]':
        return self._encr

    @encr.setter
    def encr(self, encr: Iterable[BomRef]) -> None:
        self._encr = SortedSet(encr)

    @property
    def prf(self) -> 'SortedSet[BomRef]':
        return self._prf

    @prf.setter
    def prf(self, prf: Iterable[BomRef]) -> None:
        self._prf = SortedSet(prf)

    @property
    def integ(self) -> 'SortedSet[BomRef]':
        return self._integ

    @integ.setter
    def integ(self, integ: Iterable[BomRef]) -> None:
        self._integ = SortedSet(integ)

    @property
    def ke(self) -> 'SortedSet[BomRef]':
        return self._ke

    @ke.setter
    def ke(self, ke: Iterable[BomRef]) -> None:
        self._ke = SortedSet(ke)

    @property
    def esn(self) -> bool:
        return self._esn

    @esn.setter
    def esn(self, esn: bool) -> None:
        self._esn = esn

    @property
    def auth(self) -> 'SortedSet[BomRef]':
        return self._auth

    @auth.setter
    def auth(self, auth: Iterable[BomRef]) -> None:
        self._auth = SortedSet(auth)

    def __hash__(self) -> int:
        return hash((tuple(self.encr), tuple(self.prf), tuple(self.integ), tuple(self.ke), self.esn, tuple(self.auth)))

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Ikev2TransformTypes):
            return (
                tuple(self.encr), tuple(self.prf), tuple(self.integ),
                tuple(self.ke), self.esn, tuple(self.auth)
            ) < (
                tuple(other.encr), tuple(other.prf), tuple(other.integ),
                tuple(other.ke), other.esn, tuple(other.auth)
            )
        return NotImplemented


@define
class ProtocolProperties:
    """
    This is our internal representation of the cryptoPropertiesType.protocolProperties complex type.

    .. note::
        Introduced in CycloneDX v1.6
    """

    type: Optional[ProtocolPropertiesType] = field(
        default=None,
        metadata={'json_name': 'type', 'xml_name': 'type', 'xml_sequence': 1,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    version: Optional[str] = field(
        default=None,
        metadata={'json_name': 'version', 'xml_name': 'version', 'xml_sequence': 2,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    _cipher_suites: 'SortedSet[ProtocolPropertiesCipherSuite]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'cipherSuites', 'xml_name': 'cipherSuites', 'xml_item_name': 'cipherSuite',
                  'xml_sequence': 3, 'min_schema_version': SchemaVersion.V1_6}
    )

    ikev2_transform_types: Optional[Ikev2TransformTypes] = field(
        default=None,
        metadata={'json_name': 'ikev2TransformTypes', 'xml_name': 'ikev2TransformTypes', 'xml_sequence': 4,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    _crypto_refs: 'SortedSet[BomRef]' = field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={'json_name': 'cryptoRefArray', 'xml_name': 'cryptoRefArray', 'xml_item_name': 'cryptoRef',
                  'xml_sequence': 5, 'min_schema_version': SchemaVersion.V1_6}
    )

    @property
    def cipher_suites(self) -> 'SortedSet[ProtocolPropertiesCipherSuite]':
        return self._cipher_suites

    @cipher_suites.setter
    def cipher_suites(self, cipher_suites: Iterable[ProtocolPropertiesCipherSuite]) -> None:
        self._cipher_suites = SortedSet(cipher_suites)

    @property
    def crypto_refs(self) -> 'SortedSet[BomRef]':
        return self._crypto_refs

    @crypto_refs.setter
    def crypto_refs(self, crypto_refs: Iterable[BomRef]) -> None:
        self._crypto_refs = SortedSet(crypto_refs)

    def __hash__(self) -> int:
        return hash((self.type, self.version))

    @staticmethod
    def _cmp(val: Any) -> tuple:
        """Wrap value for None-safe comparison (None sorts last)."""
        return (0, val) if val is not None else (1, '')

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, ProtocolProperties):
            return (self._cmp(self.type), self._cmp(self.version)) < (
                self._cmp(other.type), self._cmp(other.version))
        return NotImplemented


@define
class CryptoProperties:
    """
    This is our internal representation of the cryptoPropertiesType complex type.

    .. note::
        Introduced in CycloneDX v1.6
    """

    asset_type: Optional[CryptoAssetType] = field(
        default=None,
        metadata={'json_name': 'assetType', 'xml_name': 'assetType', 'xml_sequence': 1,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    algorithm_properties: Optional[AlgorithmProperties] = field(
        default=None,
        metadata={'json_name': 'algorithmProperties', 'xml_name': 'algorithmProperties', 'xml_sequence': 2,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    certificate_properties: Optional[CertificateProperties] = field(
        default=None,
        metadata={'json_name': 'certificateProperties', 'xml_name': 'certificateProperties', 'xml_sequence': 3,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    related_crypto_material_properties: Optional[RelatedCryptoMaterialProperties] = field(
        default=None,
        metadata={'json_name': 'relatedCryptoMaterialProperties', 'xml_name': 'relatedCryptoMaterialProperties',
                  'xml_sequence': 4, 'min_schema_version': SchemaVersion.V1_6}
    )

    protocol_properties: Optional[ProtocolProperties] = field(
        default=None,
        metadata={'json_name': 'protocolProperties', 'xml_name': 'protocolProperties', 'xml_sequence': 5,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    oid: Optional[str] = field(
        default=None,
        metadata={'json_name': 'oid', 'xml_name': 'oid', 'xml_sequence': 6,
                  'min_schema_version': SchemaVersion.V1_6}
    )

    def __hash__(self) -> int:
        return hash((self.asset_type, self.oid))
