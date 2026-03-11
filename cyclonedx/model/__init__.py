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
Uniform set of models to represent objects within a CycloneDX software bill-of-materials.

You can either create a `cyclonedx.model.bom.Bom` yourself programmatically, or generate a `cyclonedx.model.bom.Bom`
from a `cyclonedx.parser.BaseParser` implementation.
"""

from ..exception.model import InvalidLocaleTypeException, InvalidUriException
from ..serialization import VERSIONS_1_1_AND_LATER
from .bom_ref import BomRef
from ..serialization import (
    ALL_VERSIONS,
    METADATA_KEY_JSON_NAME,
    METADATA_KEY_VERSIONS,
    METADATA_KEY_XML_ATTR,
    METADATA_KEY_XML_NAME,
    METADATA_KEY_XML_SEQUENCE,
    VERSIONS_1_2_AND_LATER,
    VERSIONS_1_3_AND_LATER,
    VERSIONS_1_4_AND_LATER,
    VERSIONS_1_5_AND_LATER,
    VERSIONS_1_6_AND_LATER,
    VERSIONS_1_7_AND_LATER,
)
from ..schema import SchemaVersion
from ..exception.serialization import CycloneDxDeserializationException, SerializationOfUnexpectedValueException
import re
import sys
from collections.abc import Iterable
from datetime import datetime
from enum import Enum
from functools import reduce
from typing import TYPE_CHECKING, Any, ClassVar, Optional, Union
from urllib.parse import quote as url_quote
from uuid import UUID
from warnings import warn

if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated

import attrs
from sortedcontainers import SortedSet

from .._internal.compare import ComparableTuple as _ComparableTuple


def _sortedset_converter(value: Any) -> SortedSet:
    """Converter to ensure values are always SortedSet."""
    if value is None:
        return SortedSet()
    if isinstance(value, SortedSet):
        return value
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes, dict)):
        return SortedSet(value)
    return SortedSet([value])


_BOM_LINK_PREFIX = 'urn:cdx:'


class DataFlow(str, Enum):
    """
    This is our internal representation of the dataFlowType simple type within the CycloneDX standard.

    .. note::
        See the CycloneDX Schema: https://cyclonedx.org/docs/1.7/xml/#type_dataFlowType
    """
    INBOUND = 'inbound'
    OUTBOUND = 'outbound'
    BI_DIRECTIONAL = 'bi-directional'
    UNKNOWN = 'unknown'


@attrs.define
class DataClassification:
    """
    This is our internal representation of the `dataClassificationType` complex type within the CycloneDX standard.

    DataClassification might be deprecated since CycloneDX 1.5, but it is not deprecated in this library.
    In fact, this library will try to provide a compatibility layer if needed.

    .. note::
        See the CycloneDX Schema for dataClassificationType:
        https://cyclonedx.org/docs/1.7/xml/#type_dataClassificationType
    """
    flow: DataFlow = attrs.field(
        metadata={METADATA_KEY_XML_ATTR: True}
    )
    classification: str = attrs.field(
        metadata={METADATA_KEY_XML_NAME: '.'}
    )

    def __lt__(self, other: object) -> bool:
        if isinstance(other, DataClassification):
            return (self.flow, self.classification) < (other.flow, other.classification)
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.flow, self.classification))


class Encoding(str, Enum):
    """
    This is our internal representation of the encoding simple type within the CycloneDX standard.

    .. note::
        See the CycloneDX Schema: https://cyclonedx.org/docs/1.7/xml/#type_encoding
    """
    BASE_64 = 'base64'


@attrs.define
class AttachedText:
    """
    This is our internal representation of the `attachedTextType` complex type within the CycloneDX standard.

    .. note::
        See the CycloneDX Schema for hashType: https://cyclonedx.org/docs/1.7/xml/#type_attachedTextType
    """

    DEFAULT_CONTENT_TYPE = 'text/plain'

    content: str = attrs.field(
        metadata={METADATA_KEY_XML_NAME: '.'}
    )
    content_type: str = attrs.field(
        default=DEFAULT_CONTENT_TYPE,
        metadata={
            METADATA_KEY_XML_ATTR: True,
            METADATA_KEY_XML_NAME: 'content-type',
            METADATA_KEY_JSON_NAME: 'contentType',
        }
    )
    encoding: Optional[Encoding] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_ATTR: True}
    )

    @staticmethod
    def _cmp(val: Any) -> tuple:
        """Wrap value for None-safe comparison (None sorts last)."""
        return (0, val) if val is not None else (1, '')

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, AttachedText):
            return (self._cmp(self.content_type), self._cmp(self.encoding), self.content) < (
                self._cmp(other.content_type), self._cmp(other.encoding), other.content)
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.content_type, self.encoding, self.content))


class HashAlgorithm(str, Enum):
    """
    This is our internal representation of the hashAlg simple type within the CycloneDX standard.

    .. note::
        See the CycloneDX Schema: https://cyclonedx.org/docs/1.7/xml/#type_hashAlg
    """
    BLAKE2B_256 = 'BLAKE2b-256'  # Only supported in >= 1.2
    BLAKE2B_384 = 'BLAKE2b-384'  # Only supported in >= 1.2
    BLAKE2B_512 = 'BLAKE2b-512'  # Only supported in >= 1.2
    BLAKE3 = 'BLAKE3'  # Only supported in >= 1.2
    MD5 = 'MD5'
    SHA_1 = 'SHA-1'
    SHA_256 = 'SHA-256'
    SHA_384 = 'SHA-384'
    SHA_512 = 'SHA-512'
    SHA3_256 = 'SHA3-256'
    SHA3_384 = 'SHA3-384'  # Only supported in >= 1.2
    SHA3_512 = 'SHA3-512'
    STREEBOG_256 = 'Streebog-256'  # Only supported in >= 1.7
    STREEBOG_512 = 'Streebog-512'  # Only supported in >= 1.7


# Hash algorithm support by schema version
HASH_ALG_VERSIONS: dict[HashAlgorithm, set[SchemaVersion]] = {
    HashAlgorithm.MD5: ALL_VERSIONS,
    HashAlgorithm.SHA_1: ALL_VERSIONS,
    HashAlgorithm.SHA_256: ALL_VERSIONS,
    HashAlgorithm.SHA_384: ALL_VERSIONS,
    HashAlgorithm.SHA_512: ALL_VERSIONS,
    HashAlgorithm.SHA3_256: ALL_VERSIONS,
    HashAlgorithm.SHA3_512: ALL_VERSIONS,
    HashAlgorithm.BLAKE2B_256: VERSIONS_1_2_AND_LATER,
    HashAlgorithm.BLAKE2B_384: VERSIONS_1_2_AND_LATER,
    HashAlgorithm.BLAKE2B_512: VERSIONS_1_2_AND_LATER,
    HashAlgorithm.BLAKE3: VERSIONS_1_2_AND_LATER,
    HashAlgorithm.SHA3_384: VERSIONS_1_2_AND_LATER,
    HashAlgorithm.STREEBOG_256: VERSIONS_1_7_AND_LATER,
    HashAlgorithm.STREEBOG_512: VERSIONS_1_7_AND_LATER,
}


def is_hash_alg_supported(alg: HashAlgorithm, version: SchemaVersion) -> bool:
    """Check if a hash algorithm is supported in a schema version."""
    return version in HASH_ALG_VERSIONS.get(alg, set())


@attrs.define
class HashType:
    """
    This is our internal representation of the hashType complex type within the CycloneDX standard.

    .. note::
        See the CycloneDX Schema for hashType: https://cyclonedx.org/docs/1.7/xml/#type_hashType
    """
    alg: HashAlgorithm = attrs.field(
        metadata={METADATA_KEY_XML_ATTR: True}
    )
    content: str = attrs.field(
        metadata={METADATA_KEY_XML_NAME: '.'}
    )

    @staticmethod
    @deprecated('Deprecated - use cyclonedx.contrib.hash.factories.HashTypeFactory().from_hashlib_alg() instead')
    def from_hashlib_alg(hashlib_alg: str, content: str) -> 'HashType':
        """Deprecated — Alias of :func:`cyclonedx.contrib.hash.factories.HashTypeFactory.from_hashlib_alg`.

        .. deprecated:: next
            Use ``cyclonedx.contrib.hash.factories.HashTypeFactory().from_hashlib_alg()`` instead.
        """
        from ..contrib.hash.factories import HashTypeFactory
        return HashTypeFactory().from_hashlib_alg(hashlib_alg, content)

    @staticmethod
    @deprecated('Deprecated - use cyclonedx.contrib.hash.factories.HashTypeFactory().from_composite_str() instead')
    def from_composite_str(composite_hash: str) -> 'HashType':
        """Deprecated — Alias of :func:`cyclonedx.contrib.hash.factories.HashTypeFactory.from_composite_str`.

        .. deprecated:: next
            Use ``cyclonedx.contrib.hash.factories.HashTypeFactory().from_composite_str()`` instead.
        """
        from ..contrib.hash.factories import HashTypeFactory
        return HashTypeFactory().from_composite_str(composite_hash)

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, HashType):
            return (self.alg, self.content) < (other.alg, other.content)
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.alg, self.content))

    def __repr__(self) -> str:
        return f'<HashType {self.alg.name}:{self.content}>'


class ExternalReferenceType(str, Enum):
    """
    Enum object that defines the permissible 'types' for an External Reference according to the CycloneDX schema.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_externalReferenceType
    """
    ADVERSARY_MODEL = 'adversary-model'  # Only supported in >= 1.5
    ADVISORIES = 'advisories'
    ATTESTATION = 'attestation'  # Only supported in >= 1.5
    BOM = 'bom'
    BUILD_META = 'build-meta'
    BUILD_SYSTEM = 'build-system'
    CERTIFICATION_REPORT = 'certification-report'  # Only supported in >= 1.5
    CHAT = 'chat'
    CITATION = 'citation'  # Only supported in >= 1.7
    CODIFIED_INFRASTRUCTURE = 'codified-infrastructure'  # Only supported in >= 1.5
    COMPONENT_ANALYSIS_REPORT = 'component-analysis-report'  # Only supported in >= 1.5
    CONFIGURATION = 'configuration'  # Only supported in >= 1.5
    DIGITAL_SIGNATURE = 'digital-signature'  # Only supported in >= 1.6
    DISTRIBUTION = 'distribution'
    DISTRIBUTION_INTAKE = 'distribution-intake'  # Only supported in >= 1.5
    DOCUMENTATION = 'documentation'
    DYNAMIC_ANALYSIS_REPORT = 'dynamic-analysis-report'  # Only supported in >= 1.5
    ELECTRONIC_SIGNATURE = 'electronic-signature'  # Only supported in >= 1.6
    EVIDENCE = 'evidence'  # Only supported in >= 1.5
    EXPLOITABILITY_STATEMENT = 'exploitability-statement'  # Only supported in >= 1.5
    FORMULATION = 'formulation'  # Only supported in >= 1.5
    ISSUE_TRACKER = 'issue-tracker'
    LICENSE = 'license'
    LOG = 'log'  # Only supported in >= 1.5
    MAILING_LIST = 'mailing-list'
    MATURITY_REPORT = 'maturity-report'  # Only supported in >= 1.5
    MODEL_CARD = 'model-card'  # Only supported in >= 1.5
    PATENT = 'patent'  # Only supported in >= 1.7
    PATENT_ASSERTION = 'patent-assertion'  # Only supported in >= 1.7
    PATENT_FAMILY = 'patent-family'  # Only supported in >= 1.7
    PENTEST_REPORT = 'pentest-report'  # Only supported in >= 1.5
    POAM = 'poam'  # Only supported in >= 1.5
    QUALITY_METRICS = 'quality-metrics'  # Only supported in >= 1.5
    RELEASE_NOTES = 'release-notes'  # Only supported in >= 1.4
    RFC_9166 = 'rfc-9116'  # Only supported in >= 1.6
    RISK_ASSESSMENT = 'risk-assessment'  # Only supported in >= 1.5
    RUNTIME_ANALYSIS_REPORT = 'runtime-analysis-report'  # Only supported in >= 1.5
    SECURITY_CONTACT = 'security-contact'  # Only supported in >= 1.5
    STATIC_ANALYSIS_REPORT = 'static-analysis-report'  # Only supported in >= 1.5
    SOCIAL = 'social'
    SOURCE_DISTRIBUTION = 'source-distribution'  # Only supported in >= 1.6
    SCM = 'vcs'
    SUPPORT = 'support'
    THREAT_MODEL = 'threat-model'  # Only supported in >= 1.5
    VCS = 'vcs'
    VULNERABILITY_ASSERTION = 'vulnerability-assertion'  # Only supported in >= 1.5
    WEBSITE = 'website'
    OTHER = 'other'


# External reference type support by schema version

EXTREF_TYPE_VERSIONS: dict[ExternalReferenceType, set[SchemaVersion]] = {
    ExternalReferenceType.VCS: VERSIONS_1_1_AND_LATER,
    ExternalReferenceType.ISSUE_TRACKER: VERSIONS_1_1_AND_LATER,
    ExternalReferenceType.WEBSITE: VERSIONS_1_1_AND_LATER,
    ExternalReferenceType.ADVISORIES: VERSIONS_1_1_AND_LATER,
    ExternalReferenceType.BOM: VERSIONS_1_1_AND_LATER,
    ExternalReferenceType.MAILING_LIST: VERSIONS_1_1_AND_LATER,
    ExternalReferenceType.SOCIAL: VERSIONS_1_1_AND_LATER,
    ExternalReferenceType.CHAT: VERSIONS_1_1_AND_LATER,
    ExternalReferenceType.DOCUMENTATION: VERSIONS_1_1_AND_LATER,
    ExternalReferenceType.SUPPORT: VERSIONS_1_1_AND_LATER,
    ExternalReferenceType.DISTRIBUTION: VERSIONS_1_1_AND_LATER,
    ExternalReferenceType.LICENSE: VERSIONS_1_1_AND_LATER,
    ExternalReferenceType.BUILD_META: VERSIONS_1_1_AND_LATER,
    ExternalReferenceType.BUILD_SYSTEM: VERSIONS_1_1_AND_LATER,
    ExternalReferenceType.OTHER: VERSIONS_1_1_AND_LATER,
    ExternalReferenceType.RELEASE_NOTES: VERSIONS_1_4_AND_LATER,
    ExternalReferenceType.DISTRIBUTION_INTAKE: VERSIONS_1_5_AND_LATER,
    ExternalReferenceType.SECURITY_CONTACT: VERSIONS_1_5_AND_LATER,
    ExternalReferenceType.MODEL_CARD: VERSIONS_1_5_AND_LATER,
    ExternalReferenceType.LOG: VERSIONS_1_5_AND_LATER,
    ExternalReferenceType.CONFIGURATION: VERSIONS_1_5_AND_LATER,
    ExternalReferenceType.EVIDENCE: VERSIONS_1_5_AND_LATER,
    ExternalReferenceType.FORMULATION: VERSIONS_1_5_AND_LATER,
    ExternalReferenceType.ATTESTATION: VERSIONS_1_5_AND_LATER,
    ExternalReferenceType.THREAT_MODEL: VERSIONS_1_5_AND_LATER,
    ExternalReferenceType.ADVERSARY_MODEL: VERSIONS_1_5_AND_LATER,
    ExternalReferenceType.RISK_ASSESSMENT: VERSIONS_1_5_AND_LATER,
    ExternalReferenceType.VULNERABILITY_ASSERTION: VERSIONS_1_5_AND_LATER,
    ExternalReferenceType.EXPLOITABILITY_STATEMENT: VERSIONS_1_5_AND_LATER,
    ExternalReferenceType.PENTEST_REPORT: VERSIONS_1_5_AND_LATER,
    ExternalReferenceType.STATIC_ANALYSIS_REPORT: VERSIONS_1_5_AND_LATER,
    ExternalReferenceType.DYNAMIC_ANALYSIS_REPORT: VERSIONS_1_5_AND_LATER,
    ExternalReferenceType.RUNTIME_ANALYSIS_REPORT: VERSIONS_1_5_AND_LATER,
    ExternalReferenceType.COMPONENT_ANALYSIS_REPORT: VERSIONS_1_5_AND_LATER,
    ExternalReferenceType.MATURITY_REPORT: VERSIONS_1_5_AND_LATER,
    ExternalReferenceType.CERTIFICATION_REPORT: VERSIONS_1_5_AND_LATER,
    ExternalReferenceType.QUALITY_METRICS: VERSIONS_1_5_AND_LATER,
    ExternalReferenceType.CODIFIED_INFRASTRUCTURE: VERSIONS_1_5_AND_LATER,
    ExternalReferenceType.POAM: VERSIONS_1_5_AND_LATER,
    ExternalReferenceType.SOURCE_DISTRIBUTION: VERSIONS_1_6_AND_LATER,
    ExternalReferenceType.ELECTRONIC_SIGNATURE: VERSIONS_1_6_AND_LATER,
    ExternalReferenceType.DIGITAL_SIGNATURE: VERSIONS_1_6_AND_LATER,
    ExternalReferenceType.RFC_9166: VERSIONS_1_6_AND_LATER,
    ExternalReferenceType.CITATION: VERSIONS_1_7_AND_LATER,
    ExternalReferenceType.PATENT: VERSIONS_1_7_AND_LATER,
    ExternalReferenceType.PATENT_ASSERTION: VERSIONS_1_7_AND_LATER,
    ExternalReferenceType.PATENT_FAMILY: VERSIONS_1_7_AND_LATER,
}


def get_extref_type_for_version(
    extref_type: ExternalReferenceType,
    version: SchemaVersion
) -> ExternalReferenceType:
    """Get the appropriate external reference type for a schema version.

    Returns OTHER if the type is not supported in the given version.
    """
    if version in EXTREF_TYPE_VERSIONS.get(extref_type, set()):
        return extref_type
    return ExternalReferenceType.OTHER


class XsUri:
    """
    Helper class that allows us to perform validation on data strings that are defined as xs:anyURI
    in CycloneDX schema.

    Developers can just use this via `str(XsUri('https://www.google.com'))`.

    .. note::
        See XSD definition for xsd:anyURI: http://www.datypic.com/sc/xsd/t-xsd_anyURI.html
        See JSON Schema definition for iri-reference: https://tools.ietf.org/html/rfc3987
    """

    _INVALID_URI_REGEX = re.compile(r'%(?![0-9A-F]{2})|#.*#', re.IGNORECASE + re.MULTILINE)

    __SPEC_REPLACEMENTS = (
        (' ', '%20'),
        ('"', '%22'),
        ("'", '%27'),
        ('[', '%5B'),
        (']', '%5D'),
        ('<', '%3C'),
        ('>', '%3E'),
        ('{', '%7B'),
        ('}', '%7D'),
    )

    @staticmethod
    def __spec_replace(v: str, r: tuple[str, str]) -> str:
        return v.replace(*r)

    @classmethod
    def _spec_migrate(cls, o: str) -> str:
        """
         Make a string valid to
         - XML::anyURI spec.
         - JSON::iri-reference spec.

         BEST EFFORT IMPLEMENTATION
        """
        return reduce(cls.__spec_replace, cls.__SPEC_REPLACEMENTS, o)

    def __init__(self, uri: str) -> None:
        if re.search(XsUri._INVALID_URI_REGEX, uri):
            raise InvalidUriException(
                f"Supplied value '{uri}' does not appear to be a valid URI."
            )
        self._uri = self._spec_migrate(uri)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, XsUri):
            return self._uri == other._uri
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, XsUri):
            return self._uri < other._uri
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._uri)

    def __repr__(self) -> str:
        return f'<XsUri {self._uri}>'

    def __str__(self) -> str:
        return self._uri

    @property
    def uri(self) -> str:
        return self._uri

    @classmethod
    def serialize(cls, o: Any) -> str:
        if isinstance(o, XsUri):
            return str(o)
        raise SerializationOfUnexpectedValueException(
            f'Attempt to serialize a non-XsUri: {o!r}')

    @classmethod
    def deserialize(cls, o: Any) -> 'XsUri':
        try:
            return XsUri(uri=str(o))
        except ValueError as err:
            raise CycloneDxDeserializationException(
                f'XsUri string supplied does not parse: {o!r}'
            ) from err

    @classmethod
    def make_bom_link(
        cls,
        serial_number: Union[UUID, str],
        version: int = 1,
        bom_ref: Optional[Union[str, BomRef]] = None
    ) -> 'XsUri':
        """
        Generate a BOM-Link URI.
        """
        bom_ref_part = f'#{url_quote(str(bom_ref))}' if bom_ref else ''
        return cls(f'{_BOM_LINK_PREFIX}{serial_number}/{version}{bom_ref_part}')

    def is_bom_link(self) -> bool:
        """Check if the URI is a BOM-Link."""
        return self._uri.startswith(_BOM_LINK_PREFIX)


@attrs.define
class ExternalReference:
    """
    This is our internal representation of an ExternalReference complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_externalReference
    """
    type: ExternalReferenceType = attrs.field(
        metadata={METADATA_KEY_XML_ATTR: True}
    )
    url: XsUri = attrs.field(
        metadata={METADATA_KEY_XML_SEQUENCE: 1}
    )
    comment: Optional[str] = attrs.field(default=None)
    hashes: 'SortedSet[HashType]' = attrs.field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={METADATA_KEY_VERSIONS: VERSIONS_1_3_AND_LATER}
    )
    properties: 'SortedSet[Property]' = attrs.field(
        factory=SortedSet,
        converter=_sortedset_converter,
        metadata={METADATA_KEY_VERSIONS: VERSIONS_1_7_AND_LATER}
    )

    @staticmethod
    def _cmp(val: Any) -> tuple:
        """Wrap value for None-safe comparison (None sorts last)."""
        return (0, val) if val is not None else (1, '')

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, ExternalReference):
            return (self.type, self.url, self._cmp(self.comment)) < (other.type, other.url, self._cmp(other.comment))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.type, self.url, self.comment, tuple(self.hashes), tuple(self.properties)))

    def __repr__(self) -> str:
        return f'<ExternalReference {self.type.name}, {self.url}>'


@attrs.define
class Property:
    """
    This is our internal representation of `propertyType` complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_propertyType

    Specifies an individual property with a name and value.
    """
    name: str = attrs.field(
        metadata={METADATA_KEY_XML_ATTR: True}
    )
    value: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_NAME: '.'}
    )

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Property):
            return (self.name, self.value) < (other.name, other.value)
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.name, self.value))

    def __repr__(self) -> str:
        return f'<Property name={self.name}>'


@attrs.define
class NoteText:
    """
    This is our internal representation of the Note.text complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_releaseNotesType
    """

    DEFAULT_CONTENT_TYPE: ClassVar[str] = 'text/plain'

    content: str = attrs.field(
        metadata={METADATA_KEY_XML_NAME: '.'}
    )
    content_type: Optional[str] = attrs.field(
        default=DEFAULT_CONTENT_TYPE,
        metadata={
            METADATA_KEY_XML_ATTR: True,
            METADATA_KEY_XML_NAME: 'content-type',
            METADATA_KEY_JSON_NAME: 'contentType',
        }
    )
    encoding: Optional[Encoding] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_ATTR: True}
    )

    @staticmethod
    def _cmp(val: Any) -> tuple:
        """Wrap value for None-safe comparison (None sorts last)."""
        return (0, val) if val is not None else (1, '')

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, NoteText):
            return (self.content, self.content_type, self._cmp(self.encoding)) < (
                other.content, other.content_type, self._cmp(other.encoding))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.content, self.content_type, self.encoding))

    def __repr__(self) -> str:
        return f'<NoteText content_type={self.content_type}, encoding={self.encoding}>'


@attrs.define
class Note:
    """
    This is our internal representation of the Note complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_releaseNotesType
    """

    _LOCALE_TYPE_REGEX = re.compile(r'^[a-z]{2}(?:\-[A-Z]{2})?$')

    text: NoteText
    locale: Optional[str] = attrs.field(default=None, metadata={METADATA_KEY_XML_SEQUENCE: 1})

    @locale.validator
    def _validate_locale(self, attribute: attrs.Attribute, value: Optional[str]) -> None:
        if value is not None and not re.search(Note._LOCALE_TYPE_REGEX, value):
            raise InvalidLocaleTypeException(
                f'Supplied locale {value!r} is not a valid locale.'
                ' Locale string should be formatted as the ISO-639 (or higher) language code and optional'
                " ISO-3166 (or higher) country code. Examples include: 'en', 'en-US'."
            )

    @staticmethod
    def _cmp(val: Any) -> tuple:
        """Wrap value for None-safe comparison (None sorts last)."""
        return (0, val) if val is not None else (1, '')

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Note):
            return (self._cmp(self.locale), self.text) < (self._cmp(other.locale), other.text)
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.locale, self.text))

    def __repr__(self) -> str:
        return f'<Note id={id(self)}, locale={self.locale}>'


@attrs.define
class IdentifiableAction:
    """
    This is our internal representation of the `identifiableActionType` complex type.

    .. note::
        See the CycloneDX specification: https://cyclonedx.org/docs/1.7/xml/#type_identifiableActionType
    """
    timestamp: Optional[datetime] = attrs.field(default=None)
    name: Optional[str] = attrs.field(default=None)
    email: Optional[str] = attrs.field(default=None)

    @staticmethod
    def _cmp(val: Any) -> tuple:
        """Wrap value for None-safe comparison (None sorts last)."""
        return (0, val) if val is not None else (1, '')

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, IdentifiableAction):
            return (self._cmp(self.timestamp), self._cmp(self.name), self._cmp(self.email)) < (
                self._cmp(other.timestamp), self._cmp(other.name), self._cmp(other.email))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.timestamp, self.name, self.email))

    def __repr__(self) -> str:
        return f'<IdentifiableAction name={self.name}, email={self.email}>'


@attrs.define
class Copyright:
    """
    This is our internal representation of the `copyrightsType` complex type.

    .. note::
        See the CycloneDX specification: https://cyclonedx.org/docs/1.7/xml/#type_copyrightsType
    """
    text: str = attrs.field(
        metadata={METADATA_KEY_XML_NAME: '.'}
    )

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Copyright):
            return self.text < other.text
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.text)

    def __repr__(self) -> str:
        return f'<Copyright text={self.text}>'
