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


from collections.abc import Iterable
from decimal import Decimal
from enum import Enum
from typing import Any, List, Optional, Union

import attrs
from sortedcontainers import SortedSet

from .._internal.bom_ref import bom_ref_from_str as _bom_ref_from_str
from ..exception.model import InvalidConfidenceException, InvalidValueException
from ..serialization import (
    METADATA_KEY_JSON_NAME,
    METADATA_KEY_VERSIONS,
    METADATA_KEY_XML_ATTR,
    METADATA_KEY_XML_NAME,
    METADATA_KEY_XML_SEQUENCE,
    VERSIONS_1_5_AND_LATER,
    VERSIONS_1_6_AND_LATER,
)
from . import Copyright
from .bom_ref import BomRef
from .license import License, LicenseRepository


class IdentityField(str, Enum):
    """
    Enum object that defines the permissible field types for Identity.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/json/#components_items_evidence_identity
    """

    GROUP = 'group'
    NAME = 'name'
    VERSION = 'version'
    PURL = 'purl'
    CPE = 'cpe'
    OMNIBOR_ID = 'omniborId'
    SWHID = 'swhid'
    SWID = 'swid'
    HASH = 'hash'


class AnalysisTechnique(str, Enum):
    """
    Enum object that defines the permissible analysis techniques.
    """

    SOURCE_CODE_ANALYSIS = 'source-code-analysis'
    BINARY_ANALYSIS = 'binary-analysis'
    MANIFEST_ANALYSIS = 'manifest-analysis'
    AST_FINGERPRINT = 'ast-fingerprint'
    HASH_COMPARISON = 'hash-comparison'
    INSTRUMENTATION = 'instrumentation'
    DYNAMIC_ANALYSIS = 'dynamic-analysis'
    FILENAME = 'filename'
    ATTESTATION = 'attestation'
    OTHER = 'other'


def _validate_confidence(instance: Any, attribute: attrs.Attribute, value: Optional[Decimal]) -> None:
    """Validator for confidence field."""
    if value is not None and not (0 <= value <= 1):
        raise InvalidConfidenceException(f'confidence {value!r} is invalid')


def _validate_line(instance: Any, attribute: attrs.Attribute, value: Optional[int]) -> None:
    """Validator for line field."""
    if value is not None and value < 0:
        raise InvalidValueException(f'line {value!r} must not be lower than zero')


def _validate_offset(instance: Any, attribute: attrs.Attribute, value: Optional[int]) -> None:
    """Validator for offset field."""
    if value is not None and value < 0:
        raise InvalidValueException(f'offset {value!r} must not be lower than zero')


def _sortedset_factory() -> SortedSet:
    return SortedSet()


def _sortedset_converter(value: Any) -> SortedSet:
    if value is None:
        return SortedSet()
    if isinstance(value, SortedSet):
        return value
    # Handle single objects that aren't iterable sequences
    if hasattr(value, '__iter__') and not isinstance(value, (str, bytes)):
        return SortedSet(value)
    # Wrap single object in a list
    return SortedSet([value])


def _bom_ref_converter(value: Optional[Union[str, BomRef]]) -> BomRef:
    """Convert string or BomRef to BomRef."""
    return _bom_ref_from_str(value)


@attrs.define
class Method:
    """
    Represents a method used to extract and/or analyze evidence.

    .. note::
        See the CycloneDX Schema definition:
        https://cyclonedx.org/docs/1.7/json/#components_items_evidence_identity_oneOf_i0_items_methods
    """
    technique: AnalysisTechnique = attrs.field(
        metadata={METADATA_KEY_XML_SEQUENCE: 1}
    )
    confidence: Decimal = attrs.field(
        validator=_validate_confidence,
        metadata={METADATA_KEY_XML_SEQUENCE: 2}
    )
    value: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 3}
    )

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Method):
            return (self.technique, self.confidence, self.value) < (
                other.technique, other.confidence, other.value)
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.technique, self.confidence, self.value))

    def __repr__(self) -> str:
        return f'<Method technique={self.technique}, confidence={self.confidence}, value={self.value}>'


@attrs.define
class Identity:
    """
    Our internal representation of the `identityType` complex type.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/json/#components_items_evidence_identity
    """
    field: IdentityField = attrs.field(
        metadata={METADATA_KEY_XML_SEQUENCE: 1}
    )
    confidence: Optional[Decimal] = attrs.field(
        default=None,
        validator=attrs.validators.optional(_validate_confidence),
        metadata={METADATA_KEY_XML_SEQUENCE: 2}
    )
    concluded_value: Optional[str] = attrs.field(
        default=None,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_6_AND_LATER,
            METADATA_KEY_XML_SEQUENCE: 3,
        }
    )
    methods: 'SortedSet[Method]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={METADATA_KEY_XML_SEQUENCE: 4}
    )
    tools: 'SortedSet[BomRef]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={METADATA_KEY_XML_SEQUENCE: 5}
    )

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Identity):
            return (
                self.field, self.confidence, self.concluded_value,
                tuple(self.methods), tuple(self.tools)
            ) < (
                other.field, other.confidence, other.concluded_value,
                tuple(other.methods), tuple(other.tools)
            )
        return NotImplemented

    def __hash__(self) -> int:
        return hash((
            self.field, self.confidence, self.concluded_value,
            tuple(self.methods), tuple(self.tools)
        ))

    def __repr__(self) -> str:
        return (f'<Identity field={self.field}, confidence={self.confidence},'
                f' concludedValue={self.concluded_value},'
                f' methods={self.methods}, tools={self.tools}>')


@attrs.define
class Occurrence:
    """
    Our internal representation of the `occurrenceType` complex type.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/json/#components_items_evidence_occurrences
    """
    location: str = attrs.field(
        metadata={METADATA_KEY_XML_SEQUENCE: 1}
    )
    bom_ref: BomRef = attrs.field(
        factory=BomRef,
        converter=_bom_ref_converter,
        metadata={
            METADATA_KEY_JSON_NAME: 'bom-ref',
            METADATA_KEY_XML_NAME: 'bom-ref',
            METADATA_KEY_XML_ATTR: True,
        }
    )
    line: Optional[int] = attrs.field(
        default=None,
        validator=attrs.validators.optional(_validate_line),
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_6_AND_LATER,
            METADATA_KEY_XML_SEQUENCE: 2,
        }
    )
    offset: Optional[int] = attrs.field(
        default=None,
        validator=attrs.validators.optional(_validate_offset),
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_6_AND_LATER,
            METADATA_KEY_XML_SEQUENCE: 3,
        }
    )
    symbol: Optional[str] = attrs.field(
        default=None,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_6_AND_LATER,
            METADATA_KEY_XML_SEQUENCE: 4,
        }
    )
    additional_context: Optional[str] = attrs.field(
        default=None,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_6_AND_LATER,
            METADATA_KEY_XML_SEQUENCE: 5,
        }
    )

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Occurrence):
            return (
                self.bom_ref, self.location, self.line, self.offset,
                self.symbol, self.additional_context
            ) < (
                other.bom_ref, other.location, other.line, other.offset,
                other.symbol, other.additional_context
            )
        return NotImplemented

    def __hash__(self) -> int:
        return hash((
            self.bom_ref, self.location, self.line, self.offset,
            self.symbol, self.additional_context
        ))

    def __repr__(self) -> str:
        return f'<Occurrence location={self.location}, line={self.line}, symbol={self.symbol}>'


@attrs.define
class CallStackFrame:
    """
    Represents an individual frame in a call stack.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/json/#components_items_evidence_callstack
    """
    module: str = attrs.field(
        metadata={METADATA_KEY_XML_SEQUENCE: 2}
    )
    package: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 1}
    )
    function: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 3}
    )
    parameters: 'SortedSet[str]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={METADATA_KEY_XML_SEQUENCE: 4}
    )
    line: Optional[int] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 5}
    )
    column: Optional[int] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 6}
    )
    full_filename: Optional[str] = attrs.field(
        default=None,
        metadata={METADATA_KEY_XML_SEQUENCE: 7}
    )

    def __lt__(self, other: object) -> bool:
        if isinstance(other, CallStackFrame):
            return (
                self.package, self.module, self.function, tuple(self.parameters),
                self.line, self.column, self.full_filename
            ) < (
                other.package, other.module, other.function, tuple(other.parameters),
                other.line, other.column, other.full_filename
            )
        return NotImplemented

    def __hash__(self) -> int:
        return hash((
            self.package, self.module, self.function, tuple(self.parameters),
            self.line, self.column, self.full_filename
        ))

    def __repr__(self) -> str:
        return (f'<CallStackFrame package={self.package}, module={self.module},'
                f' function={self.function}, parameters={self.parameters!r},'
                f' line={self.line}, column={self.column}, full_filename={self.full_filename}>')


@attrs.define
class CallStack:
    """
    Our internal representation of the `callStackType` complex type.
    Contains an array of stack frames describing a call stack from when a component was identified.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/json/#components_items_evidence_callstack
    """
    frames: list[CallStackFrame] = attrs.field(
        factory=list,
        metadata={METADATA_KEY_XML_SEQUENCE: 1}
    )

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, CallStack):
            return tuple(self.frames) < tuple(other.frames)
        return NotImplemented

    def __hash__(self) -> int:
        return hash(tuple(self.frames))

    def __repr__(self) -> str:
        return f'<CallStack frames={len(self.frames)}>'


def _license_repository_factory() -> LicenseRepository:
    return LicenseRepository()


def _license_repository_converter(value: Any) -> LicenseRepository:
    """Convert a value to LicenseRepository."""
    if value is None:
        return LicenseRepository()
    if isinstance(value, LicenseRepository):
        return value
    # Convert generators, lists, etc. to LicenseRepository
    return LicenseRepository(value)


@attrs.define
class ComponentEvidence:
    """
    Our internal representation of the `componentEvidenceType` complex type.

    Provides the ability to document evidence collected through various forms of extraction or analysis.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_componentEvidenceType
    """
    identity: 'SortedSet[Identity]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_5_AND_LATER,
            METADATA_KEY_XML_SEQUENCE: 1,
        }
    )
    occurrences: 'SortedSet[Occurrence]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_5_AND_LATER,
            METADATA_KEY_XML_SEQUENCE: 2,
        }
    )
    callstack: Optional[CallStack] = attrs.field(
        default=None,
        metadata={
            METADATA_KEY_VERSIONS: VERSIONS_1_5_AND_LATER,
            METADATA_KEY_XML_SEQUENCE: 3,
        }
    )
    licenses: LicenseRepository = attrs.field(
        factory=_license_repository_factory,
        converter=_license_repository_converter,
        metadata={METADATA_KEY_XML_SEQUENCE: 4}
    )
    copyright: 'SortedSet[Copyright]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={METADATA_KEY_XML_SEQUENCE: 5}
    )

    def __lt__(self, other: object) -> bool:
        if isinstance(other, ComponentEvidence):
            return (
                tuple(self.licenses), tuple(self.copyright), self.callstack,
                tuple(self.identity), tuple(self.occurrences)
            ) < (
                tuple(other.licenses), tuple(other.copyright), other.callstack,
                tuple(other.identity), tuple(other.occurrences)
            )
        return NotImplemented

    def __hash__(self) -> int:
        return hash((
            tuple(self.licenses), tuple(self.copyright), self.callstack,
            tuple(self.identity), tuple(self.occurrences)
        ))

    def __repr__(self) -> str:
        return f'<ComponentEvidence id={id(self)}>'
