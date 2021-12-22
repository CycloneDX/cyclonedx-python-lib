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
#

import hashlib
import re
from enum import Enum
from typing import List, Optional, Union

from ..exception.model import InvalidLocaleTypeException, InvalidUriException
from ..exception.parser import UnknownHashTypeException

"""
Uniform set of models to represent objects within a CycloneDX software bill-of-materials.

You can either create a `cyclonedx.model.bom.Bom` yourself programmatically, or generate a `cyclonedx.model.bom.Bom`
from a `cyclonedx.parser.BaseParser` implementation.
"""

LOCALE_TYPE_REGEX = re.compile(r'^([a-z]{2})(-[A-Z]{2})?$')


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


class Encoding(Enum):
    """
    This is out internal representation of the encoding simple type within the CycloneDX standard.

    .. note::
        See the CycloneDX Schema: https://cyclonedx.org/docs/1.4/#type_encoding
    """
    BASE_64 = 'base64'


class HashAlgorithm(Enum):
    """
    This is out internal representation of the hashAlg simple type within the CycloneDX standard.

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
                algorithm=HashAlgorithm.MD5,
                hash_value=parts[1].lower()
            )
        elif algorithm_prefix[0:3] == 'sha':
            return HashType(
                algorithm=getattr(HashAlgorithm, 'SHA_{}'.format(algorithm_prefix[3:])),
                hash_value=parts[1].lower()
            )
        elif algorithm_prefix[0:6] == 'blake2':
            return HashType(
                algorithm=getattr(HashAlgorithm, 'BLAKE2b_{}'.format(algorithm_prefix[6:])),
                hash_value=parts[1].lower()
            )

        raise UnknownHashTypeException(f"Unable to determine hash type from '{composite_hash}'")

    def __init__(self, algorithm: HashAlgorithm, hash_value: str) -> None:
        self._algorithm = algorithm
        self._value = hash_value

    def get_algorithm(self) -> HashAlgorithm:
        return self._algorithm

    def get_hash_value(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f'<Hash {self._algorithm.value}:{self._value}>'


class ExternalReferenceType(Enum):
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
    SOCIAL = 'social'
    SCM = 'vcs'
    SUPPORT = 'support'
    VCS = 'vcs'
    WEBSITE = 'website'


class XsUri:
    """
    Helper class that allows us to perform validation on data strings that are defined as xs:anyURI
    in CycloneDX schema.

    .. note::
        See XSD definition for xsd:anyURI: http://www.datypic.com/sc/xsd/t-xsd_anyURI.html
    """

    invalid_uri_regex = re.compile("(%(?![0-9A-F]{2})|#.*#)", re.IGNORECASE + re.MULTILINE)

    def __init__(self, uri: str) -> None:
        if re.search(XsUri.invalid_uri_regex, uri):
            raise InvalidUriException(
                f"Supplied value '{uri}' does not appear to be a valid URI."
            )
        self._uri = uri

    def __repr__(self) -> str:
        return self._uri


class ExternalReference:
    """
    This is out internal representation of an ExternalReference complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.3/#type_externalReference
    """

    def __init__(self, reference_type: ExternalReferenceType, url: str, comment: str = '',
                 hashes: Union[List[HashType], None] = None) -> None:
        self._reference_type: ExternalReferenceType = reference_type
        self._url = url
        self._comment = comment
        self._hashes: List[HashType] = hashes if hashes else []

    def add_hash(self, our_hash: HashType) -> None:
        """
        Adds a hash that pins/identifies this External Reference.

        Args:
            our_hash:
                `HashType` instance
        """
        self._hashes.append(our_hash)

    def get_comment(self) -> Union[str, None]:
        """
        Get the comment for this External Reference.

        Returns:
            Any comment as a `str` else `None`.
        """
        return self._comment

    def get_hashes(self) -> List[HashType]:
        """
        List of cryptographic hashes that identify this External Reference.

        Returns:
            `List` of `HashType` objects where there are any hashes, else an empty `List`.
        """
        return self._hashes

    def get_reference_type(self) -> ExternalReferenceType:
        """
        Get the type of this External Reference.

        Returns:
            `ExternalReferenceType` that represents the type of this External Reference.
        """
        return self._reference_type

    def get_url(self) -> str:
        """
        Get the URL/URI for this External Reference.

        Returns:
            URI as a `str`.
        """
        return self._url

    def __repr__(self) -> str:
        return f'<ExternalReference {self._reference_type.name}, {self._url}> {self._hashes}'


class IssueClassification(Enum):
    """
    This is out internal representation of the enum `issueClassification`.

    .. note::
        See the CycloneDX Schema definition: hhttps://cyclonedx.org/docs/1.4/xml/#type_issueClassification
    """
    DEFECT = 'defect'
    ENHANCEMENT = 'enhancement'
    SECURITY = 'security'


class IssueType:
    """
    This is out internal representation of an IssueType complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_issueType
    """

    def __init__(self, classification: IssueClassification, id: Optional[str] = None, name: Optional[str] = None,
                 description: Optional[str] = None, source_name: Optional[str] = None,
                 source_url: Optional[XsUri] = None, references: Optional[List[XsUri]] = None) -> None:
        self._classification: IssueClassification = classification
        self._id: Optional[str] = id
        self._name: Optional[str] = name
        self._description: Optional[str] = description
        self._source_name: Optional[str] = source_name
        self._source_url: Optional[XsUri] = source_url
        self._references: Optional[List[XsUri]] = references


class Property:
    """
    This is out internal representation of `propertyType` complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_propertyType

    Specifies an individual property with a name and value.
    """

    def __init__(self, name: str, value: str) -> None:
        self._name = name
        self._value = value

    def get_name(self) -> str:
        """
        Get the name of this Property.

        Returns:
            Name of this Property as `str`.
        """
        return self._name

    def get_value(self) -> str:
        """
        Get the value of this Property.

        Returns:
            Value of this Property as `str`.
        """
        return self._value


class Properties:
    """
    This is out internal representation of `propertiesType` complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_propertiesType

    Provides the ability to document properties in a key/value store. This provides flexibility to include data not
    officially supported in the standard without having to use additional namespaces or create extensions.
    """

    def __init__(self, properties: Optional[List[Property]] = None) -> None:
        if properties:
            self._properties = properties
        else:
            self._properties = []

    def add_property(self, prop: Property) -> None:
        """
        Add a Property to this list of Properties.

        Args:
            prop:
                `Property` to add

        Returns:
            None
        """
        self._properties.append(prop)

    def get_properties(self) -> List[Property]:
        """
        Get all Property instances in this List.

        Returns:
             List of `Property` objects, or an empty List.
        """
        return self._properties


class Note:
    """
    This is out internal representation of the Note complex type that can be used in multiple places within
    a CycloneDX BOM document.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_releaseNotesType
    """

    def __init__(self, text: str, locale: Optional[str] = None, content_type: Optional[str] = None,
                 content_encoding: Optional[Encoding] = None) -> None:
        self._text: str = text
        self._locale: Optional[str] = None
        self._content_type: Optional[str] = content_type
        self._content_encoding: Optional[Encoding] = content_encoding
        if locale:
            if re.search(LOCALE_TYPE_REGEX, locale):
                # Valid locale
                self._locale = locale
            else:
                raise InvalidLocaleTypeException(
                    f"Supplied locale '{locale}' is not a valid locale according to ISO-639 format."
                )
