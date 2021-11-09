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
from enum import Enum
from typing import List, Union

from ..exception.parser import UnknownHashTypeException

"""
Uniform set of models to represent objects within a CycloneDX software bill-of-materials.

You can either create a `cyclonedx.model.bom.Bom` yourself programmatically, or generate a `cyclonedx.model.bom.Bom`
from a `cyclonedx.parser.BaseParser` implementation.
"""


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
