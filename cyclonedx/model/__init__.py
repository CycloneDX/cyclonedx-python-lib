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

from enum import Enum

"""
Uniform set of models to represent objects within a CycloneDX software bill-of-materials.

You can either create a `cyclonedx.model.bom.Bom` yourself programmatically, or generate a `cyclonedx.model.bom.Bom`
from a `cyclonedx.parser.BaseParser` implementation.
"""


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
    This is out internal representation of the hashType complex type within the CycloneDX standard.

    .. note::
        See the CycloneDX Schema for hashType: https://cyclonedx.org/docs/1.3/#type_hashType
    """

    _algorithm: HashAlgorithm
    _value: str

    def __init__(self, algorithm: HashAlgorithm, hash_value: str):
        self._algorithm = algorithm
        self._value = hash_value

    def get_algorithm(self) -> HashAlgorithm:
        return self._algorithm

    def get_hash_value(self) -> str:
        return self._value
