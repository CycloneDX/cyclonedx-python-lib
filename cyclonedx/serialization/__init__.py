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
Serialization infrastructure for CycloneDX models using attrs and cattrs.

This module provides converters and utilities for serializing/deserializing
CycloneDX models to/from JSON and XML formats.
"""

import sys
from typing import Any, Optional
from uuid import UUID

from packageurl import PackageURL

if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated

from ..exception.serialization import CycloneDxDeserializationException, SerializationOfUnexpectedValueException
from ._converters import (
    ALL_VERSIONS,
    METADATA_KEY_INCLUDE_NONE,
    METADATA_KEY_JSON_NAME,
    METADATA_KEY_TYPE_MAPPING,
    METADATA_KEY_VERSIONS,
    METADATA_KEY_XML_ARRAY,
    METADATA_KEY_XML_ATTR,
    METADATA_KEY_XML_NAME,
    METADATA_KEY_XML_SEQUENCE,
    VERSIONS_1_0_THROUGH_1_3,
    VERSIONS_1_1_AND_LATER,
    VERSIONS_1_2_AND_LATER,
    VERSIONS_1_3_AND_LATER,
    VERSIONS_1_4_AND_LATER,
    VERSIONS_1_5_AND_LATER,
    VERSIONS_1_6_AND_LATER,
    VERSIONS_1_7_AND_LATER,
    CycloneDxConverter,
    XmlArrayConfig,
    make_converter,
    versions,
)


class PackageUrl:
    """Helper for PackageURL serialization."""

    @classmethod
    def serialize(cls, o: Any) -> str:
        if isinstance(o, PackageURL):
            return str(o.to_string())
        raise SerializationOfUnexpectedValueException(
            f'Attempt to serialize a non-PackageURL: {o!r}')

    @classmethod
    def deserialize(cls, o: Any) -> PackageURL:
        try:
            return PackageURL.from_string(purl=str(o))
        except ValueError as err:
            raise CycloneDxDeserializationException(
                f'PURL string supplied does not parse: {o!r}'
            ) from err


class UrnUuidHelper:
    """Helper for UUID serialization as URN."""

    @classmethod
    def serialize(cls, o: Any) -> str:
        if isinstance(o, UUID):
            return o.urn
        raise SerializationOfUnexpectedValueException(
            f'Attempt to serialize a non-UUID: {o!r}')

    @classmethod
    def deserialize(cls, o: Any) -> UUID:
        try:
            return UUID(str(o))
        except ValueError as err:
            raise CycloneDxDeserializationException(
                f'UUID string supplied does not parse: {o!r}'
            ) from err


# Re-export from _converters for public API
__all__ = [
    # Converter
    'CycloneDxConverter',
    'make_converter',
    # Metadata keys
    'METADATA_KEY_VERSIONS',
    'METADATA_KEY_JSON_NAME',
    'METADATA_KEY_XML_NAME',
    'METADATA_KEY_XML_ATTR',
    'METADATA_KEY_XML_SEQUENCE',
    'METADATA_KEY_XML_ARRAY',
    'METADATA_KEY_INCLUDE_NONE',
    'METADATA_KEY_TYPE_MAPPING',
    # Version sets
    'ALL_VERSIONS',
    'VERSIONS_1_1_AND_LATER',
    'VERSIONS_1_2_AND_LATER',
    'VERSIONS_1_3_AND_LATER',
    'VERSIONS_1_4_AND_LATER',
    'VERSIONS_1_5_AND_LATER',
    'VERSIONS_1_6_AND_LATER',
    'VERSIONS_1_7_AND_LATER',
    'versions',
    # Configs
    'XmlArrayConfig',
    # Helpers
    'PackageUrl',
    'UrnUuidHelper',
]
