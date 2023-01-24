# encoding: utf-8

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

import hashlib
import re
import sys
import warnings
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Iterable, Optional, Tuple, TypeVar

import serializable
from sortedcontainers import SortedSet

from ..exception.model import (
    InvalidLocaleTypeException,
    InvalidUriException,
    MutuallyExclusivePropertiesException,
    NoPropertiesProvidedException,
    UnknownHashTypeException,
)
from ..schema.schema import SchemaVersion1Dot3, SchemaVersion1Dot4

"""
Uniform set of models to represent objects within a CycloneDX software bill-of-materials.

You can either create a `cyclonedx.model.bom.Bom` yourself programmatically, or generate a `cyclonedx.model.bom.Bom`
from a `cyclonedx.parser.BaseParser` implementation.
"""


def get_now_utc() -> datetime:
    return datetime.now(tz=timezone.utc)


def sha1sum(filename: str) -> str:
    """
    Generate a SHA1 hash of the provided file.

    Args:
        filename:
            Absolute path to file to hash as `str`

    Returns:
        SHA-1 hash
    """
    h = hashlib.sha1()
    with open(filename, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            h.update(byte_block)
    return h.hexdigest()


_T = TypeVar('_T')


class ComparableTuple(Tuple[Optional[_T], ...]):
    """
    Allows comparison of tuples, allowing for None values.
    """

    def __lt__(self, other: Any) -> bool:
        for s, o in zip(self, other):
            if s == o:
                continue
            if s is None:
                return False
            if o is None:
                return True
            if s < o:
                return True
            if s > o:
                return False
        return False

    def __gt__(self, other: Any) -> bool:
        for s, o in zip(self, other):
            if s == o:
                continue
            if s is None:
                return True
            if o is None:
                return False
            if s < o:
                return False
            if s > o:
                return True
        return False


class DataFlow(str, Enum):
    """
    This is our internal representation of the dataFlowType simple type within the CycloneDX standard.

    .. note::
        See the CycloneDX Schema: https://cyclonedx.org/docs/1.4/xml/#type_dataFlowType
    """
    INBOUND = "inbound"
    OUTBOUND = "outbound"
    BI_DIRECTIONAL = "bi-directional"
    UNKNOWN = "unknown"


@serializable.serializable_class
class DataClassification:
    """
    This is our internal representation of the `dataClassificationType` complex type within the CycloneDX standard.

    .. note::
        See the CycloneDX Schema for dataClassificationType:
        https://cyclonedx.org/docs/1.4/xml/#type_dataClassificationType
    """

    def __init__(self, *, flow: DataFlow, classification: str) -> None:
        self.flow = flow
        self.classification = classification

    @property  # type: ignore[misc]
    @serializable.xml_attribute()
    def flow(self) -> DataFlow:
        """
        Specifies the flow direction of the data.

        Valid values are: inbound, outbound, bi-directional, and unknown.

        Direction is relative to the service.

        - Inbound flow states that data enters the service
        - Outbound flow states that data leaves the service
        - Bi-directional states that data flows both ways
        - Unknown states that the direction is not known

        Returns:
            `DataFlow`
        """
        return self._flow

    @flow.setter
    def flow(self, flow: DataFlow) -> None:
        self._flow = flow

    @property  # type: ignore[misc]
    @serializable.xml_name('.')
    def classification(self) -> str:
        """
        Data classification tags data according to its type, sensitivity, and value if altered, stolen, or destroyed.

        Returns:
            `str`
        """
        return self._classification

    @classification.setter
    def classification(self, classification: str) -> None:
        self._classification = classification

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DataClassification):
            return hash(other) == hash(self)
        return False

    def __hash__(self) -> int:
        return hash((self.flow, self.classification))

    def __repr__(self) -> str:
        return f'<DataClassification flow={self.flow}>'


class Encoding(str, Enum):
    """
    This is our internal representation of the encoding simple type within the CycloneDX standard.

    .. note::
        See the CycloneDX Schema: https://cyclonedx.org/docs/1.4/#type_encoding
    """
    BASE_64 = 'base64'


@serializable.serializable_class
class AttachedText:
    """
    This is our internal representation of the `attachedTextType` complex type within the CycloneDX standard.

    .. note::
        See the CycloneDX Schema for hashType: https://cyclonedx.org/docs/1.3/#type_attachedTextType
    """

    DEFAULT_CONTENT_TYPE = 'text/plain'

    def __init__(self, *, content: str, content_type: str = DEFAULT_CONTENT_TYPE,
                 encoding: Optional[Encoding] = None) -> None:
        self.content_type = content_type
        self.encoding = encoding
        self.content = content

    @property  # type: ignore[misc]
    @serializable.xml_attribute()
    @serializable.xml_name('content-type')
    def content_type(self) -> str:
        """
        Specifies the content type of the text. Defaults to text/plain if not specified.

        Returns:
            `str`
        """
        return self._content_type

    @content_type.setter
    def content_type(self, content_type: str) -> None:
        self._content_type = content_type

    @property  # type: ignore[misc]
    @serializable.xml_attribute()
    def encoding(self) -> Optional[Encoding]:
        """
        Specifies the optional encoding the text is represented in.

        Returns:
            `Encoding` if set else `None`
        """
        return self._encoding

    @encoding.setter
    def encoding(self, encoding: Optional[Encoding]) -> None:
        self._encoding = encoding

    @property  # type: ignore[misc]
    @serializable.xml_name('.')
    def content(self) -> str:
        """
        The attachment data.

        Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment
        text.

        Returns:
            `str`
        """
        return self._content

    @content.setter
    def content(self, content: str) -> None:
        self._content = content

    def __eq__(self, other: object) -> bool:
        if isinstance(other, AttachedText):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, AttachedText):
            return ComparableTuple((self.content_type, self.content, self.encoding)) < \
                ComparableTuple((other.content_type, other.content, other.encoding))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.content, self.content_type, self.encoding))

    def __repr__(self) -> str:
        return f'<AttachedText content-type={self.content_type}, encoding={self.encoding}>'


class HashAlgorithm(str, Enum):
    """
    This is our internal representation of the hashAlg simple type within the CycloneDX standard.

    .. note::
        See the CycloneDX Schema: https://cyclonedx.org/docs/1.3/#type_hashAlg
    """

    BLAKE2B_256 = 'BLAKE2b-256'
    BLAKE2B_384 = 'BLAKE2b-384'
    BLAKE2B_512 = 'BLAKE2b-512'
    BLAKE3 = 'BLAKE3'
    MD5 = 'MD5'
    SHA_1 = 'SHA-1'
    SHA_256 = 'SHA-256'
    SHA_384 = 'SHA-384'
    SHA_512 = 'SHA-512'
    SHA3_256 = 'SHA3-256'
    SHA3_384 = 'SHA3-384'
    SHA3_512 = 'SHA3-512'


@serializable.serializable_class
class HashType:
    """
    This is our internal representation of the hashType complex type within the CycloneDX standard.

    .. note::
        See the CycloneDX Schema for hashType: https://cyclonedx.org/docs/1.3/#type_hashType
    """

    @staticmethod
    def from_composite_str(composite_hash: str) -> 'HashType':
        """
        Attempts to convert a string which includes both the Hash Algorithm and Hash Value and represent using our
        internal model classes.

        Args:
             composite_hash:
                Composite Hash string of the format `HASH_ALGORITHM`:`HASH_VALUE`.
                Example: `sha256:806143ae5bfb6a3c6e736a764057db0e6a0e05e338b5630894a5f779cabb4f9b`.

        Raises:
            `UnknownHashTypeException` if the type of hash cannot be determined.

        Returns:
            An instance of `HashType`.
        """
        parts = composite_hash.split(':')

        algorithm_prefix = parts[0].lower()
        if algorithm_prefix == 'md5':
            return HashType(
                alg=HashAlgorithm.MD5,
                content=parts[1].lower()
            )
        elif algorithm_prefix[0:3] == 'sha':
            return HashType(
                alg=getattr(HashAlgorithm, 'SHA_{}'.format(algorithm_prefix[3:])),
                content=parts[1].lower()
            )
        elif algorithm_prefix[0:6] == 'blake2':
            return HashType(
                alg=getattr(HashAlgorithm, 'BLAKE2b_{}'.format(algorithm_prefix[6:])),
                content=parts[1].lower()
            )

        raise UnknownHashTypeException(f"Unable to determine hash type from '{composite_hash}'")

    def __init__(self, *, alg: HashAlgorithm, content: str) -> None:
        self.alg = alg
        self.content = content

    @property  # type: ignore[misc]
    @serializable.xml_attribute()
    def alg(self) -> HashAlgorithm:
        """
        Specifies the algorithm used to create the hash.

        Returns:
            `HashAlgorithm`
        """
        return self._alg

    @alg.setter
    def alg(self, alg: HashAlgorithm) -> None:
        self._alg = alg

    @property  # type: ignore[misc]
    @serializable.xml_name('.')
    def content(self) -> str:
        """
        Hash value content.

        Returns:
            `str`
        """
        return self._content

    @content.setter
    def content(self, content: str) -> None:
        self._content = content

    def __eq__(self, other: object) -> bool:
        if isinstance(other, HashType):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, HashType):
            return ComparableTuple((self.alg, self.content)) < ComparableTuple((other.alg, other.content))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.alg, self.content))

    def __repr__(self) -> str:
        return f'<HashType {self.alg.name}:{self.content}>'


class ExternalReferenceType(str, Enum):
    """
    Enum object that defines the permissible 'types' for an External Reference according to the CycloneDX schema.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.3/#type_externalReferenceType
    """

    ADVISORIES = 'advisories'
    BOM = 'bom'
    BUILD_META = 'build-meta'
    BUILD_SYSTEM = 'build-system'
    CHAT = 'chat'
    DISTRIBUTION = 'distribution'
    DOCUMENTATION = 'documentation'
    ISSUE_TRACKER = 'issue-tracker'
    LICENSE = 'license'
    MAILING_LIST = 'mailing-list'
    OTHER = 'other'
    RELEASE_NOTES = 'release-notes'  # Only supported in >= 1.4
    SOCIAL = 'social'
    SCM = 'vcs'
    SUPPORT = 'support'
    VCS = 'vcs'
    WEBSITE = 'website'


@serializable.serializable_class
class XsUri(serializable.helpers.BaseHelper):
    """
    Helper class that allows us to perform validation on data strings that are defined as xs:anyURI
    in CycloneDX schema.

    Developers can just use this via `str(XsUri('https://www.google.com'))`.

    .. note::
        See XSD definition for xsd:anyURI: http://www.datypic.com/sc/xsd/t-xsd_anyURI.html
    """

    _INVALID_URI_REGEX = re.compile(r'%(?![0-9A-F]{2})|#.*#', re.IGNORECASE + re.MULTILINE)

    def __init__(self, uri: str) -> None:
        if re.search(XsUri._INVALID_URI_REGEX, uri):
            raise InvalidUriException(
                f"Supplied value '{uri}' does not appear to be a valid URI."
            )
        self._uri = uri

    @property  # type: ignore[misc]
    @serializable.json_name('.')
    @serializable.xml_name('.')
    def uri(self) -> str:
        return self._uri

    @classmethod
    def serialize(cls, o: object) -> str:
        if isinstance(o, XsUri):
            return str(o)

        raise ValueError(f'Attempt to serialize a non-XsUri: {o.__class__}')

    @classmethod
    def deserialize(cls, o: object) -> 'XsUri':
        try:
            return XsUri(uri=str(o))
        except ValueError:
            raise ValueError(f'XsUri string supplied ({o}) does not parse!')

    def __eq__(self, other: object) -> bool:
        if isinstance(other, XsUri):
            return hash(other) == hash(self)
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


@serializable.serializable_class
class ExternalReference:
    """
    This is our internal representation of an ExternalReference complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.3/#type_externalReference
    """

    def __init__(self, *, type_: ExternalReferenceType, url: XsUri, comment: Optional[str] = None,
                 hashes: Optional[Iterable[HashType]] = None) -> None:
        self.url = url
        self.comment = comment
        self.type_ = type_
        self.hashes = hashes or []  # type: ignore

    @property  # type: ignore[misc]
    @serializable.xml_sequence(1)
    def url(self) -> XsUri:
        """
        The URL to the external reference.

        Returns:
            `XsUri`
        """
        return self._url

    @url.setter
    def url(self, url: XsUri) -> None:
        self._url = url

    @property
    def comment(self) -> Optional[str]:
        """
        An optional comment describing the external reference.

        Returns:
            `str` if set else `None`
        """
        return self._comment

    @comment.setter
    def comment(self, comment: Optional[str]) -> None:
        self._comment = comment

    @property  # type: ignore[misc]
    @serializable.xml_attribute()
    def type_(self) -> ExternalReferenceType:
        """
        Specifies the type of external reference.

        There are built-in types to describe common references. If a type does not exist for the reference being
        referred to, use the "other" type.

        Returns:
            `ExternalReferenceType`
        """
        return self._type_

    @type_.setter
    def type_(self, type_: ExternalReferenceType) -> None:
        self._type_ = type_

    @property  # type: ignore[misc]
    @serializable.view(SchemaVersion1Dot3)
    @serializable.view(SchemaVersion1Dot4)
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'hash')
    def hashes(self) -> "SortedSet[HashType]":
        """
        The hashes of the external reference (if applicable).

        Returns:
            Set of `HashType`
        """
        return self._hashes

    @hashes.setter
    def hashes(self, hashes: Iterable[HashType]) -> None:
        self._hashes = SortedSet(hashes)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ExternalReference):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, ExternalReference):
            return ComparableTuple((self._type_, self._url, self._comment)) < \
                ComparableTuple((other._type_, other._url, other._comment))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((
            self._type_, self._url, self._comment,
            tuple(sorted(self._hashes, key=hash))
        ))

    def __repr__(self) -> str:
        return f'<ExternalReference {self.type_.name}, {self.url}>'


@serializable.serializable_class
class License:
    """
    This is our internal representation of `licenseType` complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_licenseType
    """

    def __init__(self, *, id_: Optional[str] = None, name: Optional[str] = None,
                 text: Optional[AttachedText] = None, url: Optional[XsUri] = None) -> None:
        if not id_ and not name:
            raise MutuallyExclusivePropertiesException('Either `id_` or `name` MUST be supplied')
        if id_ and name:
            warnings.warn(
                'Both `id_` and `name` have been supplied - `name` will be ignored!',
                RuntimeWarning
            )
        self.id_ = id_
        if not id_:
            self.name = name
        else:
            self.name = None
        self.text = text
        self.url = url

    @property
    def id_(self) -> Optional[str]:
        """
        A valid SPDX license ID

        Returns:
            `str` or `None`
        """
        return self._id

    @id_.setter
    def id_(self, id_: Optional[str]) -> None:
        self._id = id_

    @property
    def name(self) -> Optional[str]:
        """
        If SPDX does not define the license used, this field may be used to provide the license name.

        Returns:
            `str` or `None`
        """
        return self._name

    @name.setter
    def name(self, name: Optional[str]) -> None:
        self._name = name

    @property
    def text(self) -> Optional[AttachedText]:
        """
        Specifies the optional full text of the attachment

        Returns:
            `AttachedText` else `None`
        """
        return self._text

    @text.setter
    def text(self, text: Optional[AttachedText]) -> None:
        self._text = text

    @property
    def url(self) -> Optional[XsUri]:
        """
        The URL to the attachment file. If the attachment is a license or BOM, an externalReference should also be
        specified for completeness.

        Returns:
            `XsUri` or `None`
        """
        return self._url

    @url.setter
    def url(self, url: Optional[XsUri]) -> None:
        self._url = url

    def __eq__(self, other: object) -> bool:
        if isinstance(other, License):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, License):
            return ComparableTuple((self.id_, self.name)) < ComparableTuple((other.id_, other.name))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.id_, self.name, self.text, self.url))

    def __repr__(self) -> str:
        return f'<License id={self.id_}, name={self.name}>'


@serializable.serializable_class
class LicenseChoice:
    """
    This is our internal representation of `licenseChoiceType` complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_licenseChoiceType
    """

    def __init__(self, *, license_: Optional[License] = None, expression: Optional[str] = None) -> None:
        if not license_ and not expression:
            raise NoPropertiesProvidedException(
                'One of `license` or `license_expression` must be supplied - neither supplied'
            )
        if license_ and expression:
            warnings.warn(
                'Both `license` and `license_expression` have been supplied - `license` will take precedence',
                RuntimeWarning
            )
        self.license_ = license_
        if not license_:
            self.expression = expression
        else:
            self.expression = None

    @property
    def license_(self) -> Optional[License]:
        """
        License definition

        Returns:
            `License` or `None`
        """
        return self._license_

    @license_.setter
    def license_(self, license_: Optional[License]) -> None:
        self._license_ = license_

    @property
    def expression(self) -> Optional[str]:
        """
        A valid SPDX license expression (not enforced).

        Refer to https://spdx.org/specifications for syntax requirements.

        Returns:
            `str` or `None`
        """
        return self._expression

    @expression.setter
    def expression(self, expression: Optional[str]) -> None:
        self._expression = expression

    def __eq__(self, other: object) -> bool:
        if isinstance(other, LicenseChoice):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, LicenseChoice):
            return ComparableTuple((self.license_, self.expression)) < ComparableTuple(
                (other.license_, other.expression))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.license_, self.expression))

    def __repr__(self) -> str:
        return f'<LicenseChoice license={self.license_}, expression={self.expression}>'


@serializable.serializable_class
class Property:
    """
    This is our internal representation of `propertyType` complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_propertyType

    Specifies an individual property with a name and value.
    """

    def __init__(self, *, name: str, value: str) -> None:
        self.name = name
        self.value = value

    @property  # type: ignore[misc]
    @serializable.xml_attribute()
    def name(self) -> str:
        """
        The name of the property.

        Duplicate names are allowed, each potentially having a different value.

        Returns:
            `str`
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property  # type: ignore[misc]
    @serializable.xml_name('.')
    def value(self) -> str:
        """
        Value of this Property.

        Returns:
             `str`
        """
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        self._value = value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Property):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Property):
            return ComparableTuple((self.name, self.value)) < ComparableTuple((other.name, other.value))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.name, self.value))

    def __repr__(self) -> str:
        return f'<Property name={self.name}>'


@serializable.serializable_class
class NoteText:
    """
    This is our internal representation of the Note.text complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_releaseNotesType
    """

    DEFAULT_CONTENT_TYPE: str = 'text/plain'

    def __init__(self, *, content: str, content_type: Optional[str] = None,
                 encoding: Optional[Encoding] = None) -> None:
        self.content = content
        self.content_type = content_type or NoteText.DEFAULT_CONTENT_TYPE
        self.encoding = encoding

    @property  # type: ignore[misc]
    @serializable.xml_name('.')
    def content(self) -> str:
        """
        Get the text content of this Note.

        Returns:
            `str` note content
        """
        return self._content

    @content.setter
    def content(self, content: str) -> None:
        self._content = content

    @property  # type: ignore[misc]
    @serializable.xml_attribute()
    @serializable.xml_name('content-type')
    def content_type(self) -> Optional[str]:
        """
        Get the content-type of this Note.

        Defaults to 'text/plain' if one was not explicitly specified.

        Returns:
            `str` content-type
        """
        return self._content_type

    @content_type.setter
    def content_type(self, content_type: str) -> None:
        self._content_type = content_type

    @property  # type: ignore[misc]
    @serializable.xml_attribute()
    def encoding(self) -> Optional[Encoding]:
        """
        Get the encoding method used for the note's content.

        Returns:
            `Encoding` if set else `None`
        """
        return self._encoding

    @encoding.setter
    def encoding(self, encoding: Optional[Encoding]) -> None:
        self._encoding = encoding

    def __eq__(self, other: object) -> bool:
        if isinstance(other, NoteText):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, NoteText):
            return ComparableTuple((self.content, self.content_type, self.encoding)) < \
                ComparableTuple((other.content, other.content_type, other.encoding))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.content, self.content_type, self.encoding))

    def __repr__(self) -> str:
        return f'<NoteText content_type={self.content_type}, encoding={self.encoding}>'


@serializable.serializable_class
class Note:
    """
    This is our internal representation of the Note complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_releaseNotesType

    @todo: Replace ``NoteText`` with ``AttachedText``?
    """

    _LOCALE_TYPE_REGEX = re.compile(r'^[a-z]{2}(?:\-[A-Z]{2})?$')

    def __init__(self, *, text: NoteText, locale: Optional[str] = None) -> None:
        self.text = text
        self.locale = locale

    @property
    def text(self) -> NoteText:
        """
        Specifies the full content of the release note.

        Returns:
            `NoteText`
        """
        return self._text

    @text.setter
    def text(self, text: NoteText) -> None:
        self._text = text

    @property  # type: ignore[misc]
    @serializable.xml_sequence(1)
    def locale(self) -> Optional[str]:
        """
        Get the ISO locale of this Note.

        The ISO-639 (or higher) language code and optional ISO-3166 (or higher) country code.

        Examples include: "en", "en-US", "fr" and "fr-CA".

        Returns:
            `str` locale if set else `None`
        """
        return self._locale

    @locale.setter
    def locale(self, locale: Optional[str]) -> None:
        self._locale = locale
        if isinstance(locale, str):
            if not re.search(Note._LOCALE_TYPE_REGEX, locale):
                self._locale = None
                raise InvalidLocaleTypeException(
                    f"Supplied locale '{locale}' is not a valid locale. "
                    f"Locale string should be formatted as the ISO-639 (or higher) language code and optional "
                    f"ISO-3166 (or higher) country code. according to ISO-639 format. Examples include: 'en', 'en-US'."
                )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Note):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Note):
            return ComparableTuple((self.locale, self.text)) < ComparableTuple((other.locale, other.text))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.text, self.locale))

    def __repr__(self) -> str:
        return f'<Note id={id(self)}, locale={self.locale}>'


@serializable.serializable_class
class OrganizationalContact:
    """
    This is our internal representation of the `organizationalContact` complex type that can be used in multiple places
    within a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_organizationalContact
    """

    def __init__(self, *, name: Optional[str] = None, phone: Optional[str] = None, email: Optional[str] = None) -> None:
        if not name and not phone and not email:
            raise NoPropertiesProvidedException(
                'One of name, email or phone must be supplied for an OrganizationalContact - none supplied.'
            )
        self.name = name
        self.email = email
        self.phone = phone

    @property  # type: ignore[misc]
    @serializable.xml_sequence(1)
    def name(self) -> Optional[str]:
        """
        Get the name of the contact.

        Returns:
            `str` if set else `None`
        """
        return self._name

    @name.setter
    def name(self, name: Optional[str]) -> None:
        self._name = name

    @property  # type: ignore[misc]
    @serializable.xml_sequence(2)
    def email(self) -> Optional[str]:
        """
        Get the email of the contact.

        Returns:
            `str` if set else `None`
        """
        return self._email

    @email.setter
    def email(self, email: Optional[str]) -> None:
        self._email = email

    @property  # type: ignore[misc]
    @serializable.xml_sequence(3)
    def phone(self) -> Optional[str]:
        """
        Get the phone of the contact.

        Returns:
            `str` if set else `None`
        """
        return self._phone

    @phone.setter
    def phone(self, phone: Optional[str]) -> None:
        self._phone = phone

    def __eq__(self, other: object) -> bool:
        if isinstance(other, OrganizationalContact):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, OrganizationalContact):
            return ComparableTuple((self.name, self.email, self.phone)) < \
                ComparableTuple((other.name, other.email, other.phone))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.name, self.phone, self.email))

    def __repr__(self) -> str:
        return f'<OrganizationalContact name={self.name}, email={self.email}, phone={self.phone}>'


@serializable.serializable_class
class OrganizationalEntity:
    """
    This is our internal representation of the `organizationalEntity` complex type that can be used in multiple places
    within a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_organizationalEntity
    """

    def __init__(self, *, name: Optional[str] = None, urls: Optional[Iterable[XsUri]] = None,
                 contacts: Optional[Iterable[OrganizationalContact]] = None) -> None:
        if not name and not urls and not contacts:
            raise NoPropertiesProvidedException(
                'One of name, urls or contacts must be supplied for an OrganizationalEntity - none supplied.'
            )
        self.name = name
        self.urls = urls or []  # type: ignore
        self.contacts = contacts or []  # type: ignore

    @property  # type: ignore[misc]
    @serializable.xml_sequence(1)
    def name(self) -> Optional[str]:
        """
        Get the name of the organization.

        Returns:
            `str` if set else `None`
        """
        return self._name

    @name.setter
    def name(self, name: Optional[str]) -> None:
        self._name = name

    @property  # type: ignore[misc]
    @serializable.json_name('url')
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'url')
    @serializable.xml_sequence(2)
    def urls(self) -> "SortedSet[XsUri]":
        """
        Get a list of URLs of the organization. Multiple URLs are allowed.

        Returns:
            Set of `XsUri`
        """
        return self._urls

    @urls.setter
    def urls(self, urls: Iterable[XsUri]) -> None:
        self._urls = SortedSet(urls)

    @property  # type: ignore[misc]
    @serializable.json_name('contact')
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'contact')
    @serializable.xml_sequence(3)
    def contacts(self) -> "SortedSet[OrganizationalContact]":
        """
        Get a list of contact person at the organization. Multiple contacts are allowed.

        Returns:
            Set of `OrganizationalContact`
        """
        return self._contacts

    @contacts.setter
    def contacts(self, contacts: Iterable[OrganizationalContact]) -> None:
        self._contacts = SortedSet(contacts)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, OrganizationalEntity):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, OrganizationalEntity):
            return hash(self) < hash(other)
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.name, tuple(self.urls), tuple(self.contacts)))

    def __repr__(self) -> str:
        return f'<OrganizationalEntity name={self.name}>'


@serializable.serializable_class
class Tool:
    """
    This is our internal representation of the `toolType` complex type within the CycloneDX standard.

    Tool(s) are the things used in the creation of the BOM.

    .. note::
        See the CycloneDX Schema for toolType: https://cyclonedx.org/docs/1.3/#type_toolType
    """

    def __init__(self, *, vendor: Optional[str] = None, name: Optional[str] = None, version: Optional[str] = None,
                 hashes: Optional[Iterable[HashType]] = None,
                 external_references: Optional[Iterable[ExternalReference]] = None) -> None:
        self.vendor = vendor
        self.name = name
        self.version = version
        self.hashes = hashes or []  # type: ignore
        self.external_references = external_references or []  # type: ignore

    @property  # type: ignore[misc]
    @serializable.xml_sequence(1)
    def vendor(self) -> Optional[str]:
        """
        The name of the vendor who created the tool.

        Returns:
            `str` if set else `None`
        """
        return self._vendor

    @vendor.setter
    def vendor(self, vendor: Optional[str]) -> None:
        self._vendor = vendor

    @property  # type: ignore[misc]
    @serializable.xml_sequence(2)
    def name(self) -> Optional[str]:
        """
        The name of the tool.

        Returns:
             `str` if set else `None`
        """
        return self._name

    @name.setter
    def name(self, name: Optional[str]) -> None:
        self._name = name

    @property  # type: ignore[misc]
    @serializable.xml_sequence(3)
    def version(self) -> Optional[str]:
        """
        The version of the tool.

        Returns:
             `str` if set else `None`
        """
        return self._version

    @version.setter
    def version(self, version: Optional[str]) -> None:
        self._version = version

    @property  # type: ignore[misc]
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'hash')
    @serializable.xml_sequence(4)
    def hashes(self) -> "SortedSet[HashType]":
        """
        The hashes of the tool (if applicable).

        Returns:
            Set of `HashType`
        """
        return self._hashes

    @hashes.setter
    def hashes(self, hashes: Iterable[HashType]) -> None:
        self._hashes = SortedSet(hashes)

    @property  # type: ignore[misc]
    @serializable.view(SchemaVersion1Dot4)
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'reference')
    @serializable.xml_sequence(5)
    def external_references(self) -> "SortedSet[ExternalReference]":
        """
        External References provide a way to document systems, sites, and information that may be relevant but which
        are not included with the BOM.

        Returns:
            Set of `ExternalReference`
        """
        return self._external_references

    @external_references.setter
    def external_references(self, external_references: Iterable[ExternalReference]) -> None:
        self._external_references = SortedSet(external_references)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Tool):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Tool):
            return ComparableTuple((self.vendor, self.name, self.version)) < \
                ComparableTuple((other.vendor, other.name, other.version))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.vendor, self.name, self.version, tuple(self.hashes), tuple(self.external_references)))

    def __repr__(self) -> str:
        return f'<Tool name={self.name}, version={self.version}, vendor={self.vendor}>'


@serializable.serializable_class
class IdentifiableAction:
    """
    This is our internal representation of the `identifiableActionType` complex type.

    .. note::
        See the CycloneDX specification: https://cyclonedx.org/docs/1.4/xml/#type_identifiableActionType
    """

    def __init__(self, *, timestamp: Optional[datetime] = None, name: Optional[str] = None,
                 email: Optional[str] = None) -> None:
        if not timestamp and not name and not email:
            raise NoPropertiesProvidedException(
                'At least one of `timestamp`, `name` or `email` must be provided for an `IdentifiableAction`.'
            )

        self.timestamp = timestamp
        self.name = name
        self.email = email

    @property  # type: ignore[misc]
    @serializable.type_mapping(serializable.helpers.XsdDateTime)
    def timestamp(self) -> Optional[datetime]:
        """
        The timestamp in which the action occurred.

        Returns:
            `datetime` if set else `None`
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: Optional[datetime]) -> None:
        self._timestamp = timestamp

    @property
    def name(self) -> Optional[str]:
        """
        The name of the individual who performed the action.

        Returns:
            `str` if set else `None`
        """
        return self._name

    @name.setter
    def name(self, name: Optional[str]) -> None:
        self._name = name

    @property
    def email(self) -> Optional[str]:
        """
        The email address of the individual who performed the action.

        Returns:
            `str` if set else `None`
        """
        return self._email

    @email.setter
    def email(self, email: Optional[str]) -> None:
        self._email = email

    def __eq__(self, other: object) -> bool:
        if isinstance(other, IdentifiableAction):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, IdentifiableAction):
            return ComparableTuple((self.timestamp, self.name, self.email)) < \
                ComparableTuple((other.timestamp, other.name, other.email))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.timestamp, self.name, self.email))

    def __repr__(self) -> str:
        return f'<IdentifiableAction name={self.name}, email={self.email}>'


@serializable.serializable_class
class Copyright:
    """
    This is our internal representation of the `copyrightsType` complex type.

    .. note::
        See the CycloneDX specification: https://cyclonedx.org/docs/1.4/xml/#type_copyrightsType
    """

    def __init__(self, *, text: str) -> None:
        self.text = text

    @property  # type: ignore[misc]
    @serializable.xml_name('.')
    def text(self) -> str:
        """
        Copyright statement.

        Returns:
            `str` if set else `None`
        """
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Copyright):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Copyright):
            return self.text < other.text
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.text)

    def __repr__(self) -> str:
        return f'<Copyright text={self.text}>'


if sys.version_info >= (3, 8):
    from importlib.metadata import version as meta_version
else:
    from importlib_metadata import version as meta_version

try:
    __ThisToolVersion: Optional[str] = str(meta_version('cyclonedx-python-lib'))  # type: ignore[no-untyped-call]
except Exception:
    __ThisToolVersion = None
ThisTool = Tool(vendor='CycloneDX', name='cyclonedx-python-lib', version=__ThisToolVersion or 'UNKNOWN')
ThisTool.external_references.update([
    ExternalReference(
        type_=ExternalReferenceType.BUILD_SYSTEM,
        url=XsUri('https://github.com/CycloneDX/cyclonedx-python-lib/actions')
    ),
    ExternalReference(
        type_=ExternalReferenceType.DISTRIBUTION,
        url=XsUri('https://pypi.org/project/cyclonedx-python-lib/')
    ),
    ExternalReference(
        type_=ExternalReferenceType.DOCUMENTATION,
        url=XsUri('https://cyclonedx.github.io/cyclonedx-python-lib/')
    ),
    ExternalReference(
        type_=ExternalReferenceType.ISSUE_TRACKER,
        url=XsUri('https://github.com/CycloneDX/cyclonedx-python-lib/issues')
    ),
    ExternalReference(
        type_=ExternalReferenceType.LICENSE,
        url=XsUri('https://github.com/CycloneDX/cyclonedx-python-lib/blob/main/LICENSE')
    ),
    ExternalReference(
        type_=ExternalReferenceType.RELEASE_NOTES,
        url=XsUri('https://github.com/CycloneDX/cyclonedx-python-lib/blob/main/CHANGELOG.md')
    ),
    ExternalReference(
        type_=ExternalReferenceType.VCS,
        url=XsUri('https://github.com/CycloneDX/cyclonedx-python-lib')
    ),
    ExternalReference(
        type_=ExternalReferenceType.WEBSITE,
        url=XsUri('https://cyclonedx.org')
    )
])
