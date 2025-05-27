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
from typing import Any, Optional, Union
from xml.etree.ElementTree import Element  # nosec B405

# See https://github.com/package-url/packageurl-python/issues/65
import py_serializable as serializable
from sortedcontainers import SortedSet

from .._internal.compare import ComparableTuple as _ComparableTuple
from ..exception.serialization import CycloneDxDeserializationException
from ..schema.schema import SchemaVersion1Dot6
from . import Copyright, XsUri
from .bom_ref import BomRef
from .license import License, LicenseRepository, _LicenseRepositorySerializationHelper


@serializable.serializable_enum
class IdentityFieldType(str, Enum):
    """
    Enum object that defines the permissible field types for Identity.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.6/json/#components_items_evidence_identity
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


@serializable.serializable_enum
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


@serializable.serializable_class
class Method:
    """
    Represents a method used to extract and/or analyze evidence.
    """

    def __init__(
        self, *,
        technique: Union[AnalysisTechnique, str],
        confidence: Decimal,
        value: Optional[str] = None,
    ) -> None:
        self.technique = technique
        self.confidence = confidence
        self.value = value

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'technique')
    @serializable.json_name('technique')
    @serializable.xml_sequence(1)
    def technique(self) -> str:
        return self._technique.value

    @technique.setter
    def technique(self, technique: Union[AnalysisTechnique, str]) -> None:
        if isinstance(technique, str):
            try:
                technique = AnalysisTechnique(technique)
            except ValueError:
                raise ValueError(
                    f'Technique must be one of: {", ".join(t.value for t in AnalysisTechnique)}'
                )
        self._technique = technique

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'confidence')
    @serializable.json_name('confidence')
    @serializable.xml_sequence(2)
    def confidence(self) -> Decimal:
        return self._confidence

    @confidence.setter
    def confidence(self, confidence: Decimal) -> None:
        if not 0 <= confidence <= 1:
            raise ValueError('Confidence must be between 0 and 1')
        self._confidence = confidence

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'value')
    @serializable.json_name('value')
    @serializable.xml_sequence(3)
    def value(self) -> Optional[str]:
        return self._value

    @value.setter
    def value(self, value: Optional[str]) -> None:
        self._value = value

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple(
            (
                self.technique,
                self.confidence,
                self.value,
            )
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Method):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Method):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<Method technique={self.technique}, confidence={self.confidence}, value={self.value}>'


class _ToolsSerializationHelper(serializable.helpers.BaseHelper):
    """  THIS CLASS IS NON-PUBLIC API  """

    @classmethod
    def json_normalize(cls, o: Any, *,
                       view: Optional[type[serializable.ViewType]],
                       **__: Any) -> Any:
        if isinstance(o, SortedSet):
            return [str(t) for t in o]  # Convert BomRef to string
        return o

    @classmethod
    def xml_normalize(cls, o: Any, *,
                      element_name: str,
                      view: Optional[type[serializable.ViewType]],
                      xmlns: Optional[str],
                      **__: Any) -> Optional[Element]:
        if len(o) == 0:
            return None

        # Create tools element with namespace if provided
        tools_elem = Element(f'{{{xmlns}}}tools' if xmlns else 'tools')
        for tool in o:
            tool_elem = Element(f'{{{xmlns}}}tool' if xmlns else 'tool')
            tool_elem.set(f'{{{xmlns}}}ref' if xmlns else 'ref', str(tool))
            tools_elem.append(tool_elem)
        return tools_elem

    @classmethod
    def json_denormalize(cls, o: Any, **kwargs: Any) -> SortedSet[BomRef]:
        if isinstance(o, (list, set, tuple)):
            return SortedSet(BomRef(str(t)) for t in o)
        return SortedSet()

    @classmethod
    def xml_denormalize(cls, o: Element,
                        default_ns: Optional[str],
                        **__: Any) -> SortedSet[BomRef]:
        repo = []
        tool_tag = f'{{{default_ns}}}tool' if default_ns else 'tool'
        ref_attr = f'{{{default_ns}}}ref' if default_ns else 'ref'
        for tool_elem in o.findall(f'.//{tool_tag}'):
            ref = tool_elem.get(ref_attr) or tool_elem.get('ref')
            if ref:
                repo.append(BomRef(str(ref)))
            else:
                raise CycloneDxDeserializationException(f'unexpected: {tool_elem!r}')
        return SortedSet(repo)


@serializable.serializable_class
class Identity:
    """
    Our internal representation of the `identityType` complex type.

    .. note::
        See the CycloneDX Schema definition: hhttps://cyclonedx.org/docs/1.6/json/#components_items_evidence_identity
    """

    def __init__(
        self, *,
        field: Union[IdentityFieldType, str],  # Accept either enum or string
        confidence: Optional[Decimal] = None,
        concluded_value: Optional[str] = None,
        methods: Optional[Iterable[Method]] = None,  # Updated type
        tools: Optional[Iterable[Union[str, BomRef]]] = None,
    ) -> None:
        self.field = field
        self.confidence = confidence
        self.concluded_value = concluded_value
        self.methods = methods or []  # type: ignore[assignment]
        self.tools = tools or []  # type: ignore[assignment]

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'field')
    @serializable.xml_sequence(1)
    def field(self) -> str:
        return self._field.value

    @field.setter
    def field(self, field: Union[IdentityFieldType, str]) -> None:
        if isinstance(field, str):
            try:
                field = IdentityFieldType(field)
            except ValueError:
                raise ValueError(
                    f'Field must be one of: {", ".join(f.value for f in IdentityFieldType)}'
                )
        self._field = field

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'confidence')
    @serializable.xml_sequence(2)
    def confidence(self) -> Optional[Decimal]:
        """
        Returns the confidence value if set, otherwise None.
        """
        return self._confidence

    @confidence.setter
    def confidence(self, confidence: Optional[Decimal]) -> None:
        """
        Sets the confidence value. Ensures it is between 0 and 1 if provided.
        """
        if confidence is not None and not 0 <= confidence <= 1:
            raise ValueError('Confidence must be between 0 and 1')
        self._confidence = confidence

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'concludedValue')
    @serializable.xml_sequence(3)
    def concluded_value(self) -> Optional[str]:
        return self._concluded_value

    @concluded_value.setter
    def concluded_value(self, concluded_value: Optional[str]) -> None:
        self._concluded_value = concluded_value

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'method')
    @serializable.xml_sequence(4)
    def methods(self) -> 'SortedSet[Method]':  # Updated return type
        return self._methods

    @methods.setter
    def methods(self, methods: Iterable[Method]) -> None:  # Updated parameter type
        self._methods = SortedSet(methods)

    @property
    @serializable.type_mapping(_ToolsSerializationHelper)
    @serializable.xml_sequence(5)
    def tools(self) -> 'SortedSet[BomRef]':
        """
        References to the tools used to perform analysis and collect evidence.
        Can be either a string reference (refLinkType) or a BOM reference (bomLinkType).
        All references are stored and serialized as strings.

        Returns:
            Set of tool references as BomRef
        """
        return self._tools

    @tools.setter
    def tools(self, tools: Iterable[Union[str, BomRef]]) -> None:
        """Convert all inputs to BomRef for consistent storage"""
        validated = []
        for t in tools:
            ref_str = str(t)
            if not (XsUri(ref_str).is_bom_link() or len(ref_str) >= 1):
                raise ValueError(
                    f'Invalid tool reference: {ref_str}. Must be a valid BOM reference or BOM-Link.'
                )
            validated.append(BomRef(ref_str))
        self._tools = SortedSet(validated)

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple(
            (
                self.field,
                self.confidence,
                self.concluded_value,
                _ComparableTuple(self.methods),
                _ComparableTuple(self.tools),
            )
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Identity):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Identity):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<Identity field={self.field}, confidence={self.confidence}>'


@serializable.serializable_class
class Occurrence:
    """
    Our internal representation of the `occurrenceType` complex type.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.6/json/#components_items_evidence_occurrences
    """

    def __init__(
        self, *,
        bom_ref: Optional[Union[str, BomRef]] = None,
        location: str,
        line: Optional[int] = None,
        offset: Optional[int] = None,
        symbol: Optional[str] = None,
        additional_context: Optional[str] = None,
    ) -> None:
        self.bom_ref = bom_ref  # type: ignore[assignment]
        self.location = location
        self.line = line
        self.offset = offset
        self.symbol = symbol
        self.additional_context = additional_context

    @property
    @serializable.json_name('bom-ref')
    @serializable.type_mapping(BomRef)
    @serializable.xml_attribute()
    @serializable.xml_name('bom-ref')
    def bom_ref(self) -> Optional[BomRef]:
        """
        Reference to a component defined in the BOM.
        """
        return self._bom_ref

    @bom_ref.setter
    def bom_ref(self, bom_ref: Optional[Union[str, BomRef]]) -> None:
        if bom_ref is None:
            self._bom_ref = None
            return
        bom_ref_str = str(bom_ref)
        if len(bom_ref_str) < 1:
            raise ValueError('bom_ref must be at least 1 character long')
        if XsUri(bom_ref_str).is_bom_link():
            raise ValueError("bom_ref SHOULD NOT start with 'urn:cdx:' to avoid conflicts with BOM-Links")
        self._bom_ref = BomRef(bom_ref_str)

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'location')
    @serializable.xml_sequence(1)
    def location(self) -> str:
        """
        Location can be a file path, URL, or a unique identifier from a component discovery tool
        """
        return self._location

    @location.setter
    def location(self, location: str) -> None:
        if location is None:
            raise TypeError('location is required and cannot be None')
        self._location = location

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'line')
    @serializable.xml_sequence(2)
    def line(self) -> Optional[int]:
        """
        The line number in the file where the dependency or reference was detected.
        """
        return self._line

    @line.setter
    def line(self, line: Optional[int]) -> None:
        self._line = line

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'offset')
    @serializable.xml_sequence(3)
    def offset(self) -> Optional[int]:
        """
        The offset location within the file where the dependency or reference was detected.
        """
        return self._offset

    @offset.setter
    def offset(self, offset: Optional[int]) -> None:
        self._offset = offset

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'symbol')
    @serializable.xml_sequence(4)
    def symbol(self) -> Optional[str]:
        """
        Programming language symbol or import name.
        """
        return self._symbol

    @symbol.setter
    def symbol(self, symbol: Optional[str]) -> None:
        self._symbol = symbol

    @property
    @serializable.json_name('additionalContext')
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'additionalContext')
    @serializable.xml_sequence(5)
    def additional_context(self) -> Optional[str]:
        """
        Additional context about the occurrence of the component.
        """
        return self._additional_context

    @additional_context.setter
    def additional_context(self, additional_context: Optional[str]) -> None:
        self._additional_context = additional_context

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple(
            (
                self.bom_ref,
                self.location,
                self.line,
                self.offset,
                self.symbol,
                self.additional_context,
            )
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Occurrence):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Occurrence):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<Occurrence location={self.location}, line={self.line}, symbol={self.symbol}>'


@serializable.serializable_class
class StackFrame:
    """
    Represents an individual frame in a call stack.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.6/json/#components_items_evidence_callstack
    """

    def __init__(
        self, *,
        package: Optional[str] = None,
        module: str,  # module is required
        function: Optional[str] = None,
        parameters: Optional[Iterable[str]] = None,
        line: Optional[int] = None,
        column: Optional[int] = None,
        full_filename: Optional[str] = None,
    ) -> None:
        self.package = package
        self.module = module
        self.function = function
        self.parameters = parameters or []  # type: ignore[assignment]
        self.line = line
        self.column = column
        self.full_filename = full_filename

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'package')
    @serializable.xml_sequence(1)
    def package(self) -> Optional[str]:
        """
        The package name.
        """
        return self._package

    @package.setter
    def package(self, package: Optional[str]) -> None:
        """
        Sets the package name.
        """
        self._package = package

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'module')
    @serializable.xml_sequence(2)
    def module(self) -> str:
        """
        The module name
        """
        return self._module

    @module.setter
    def module(self, module: str) -> None:
        if module is None:
            raise TypeError('module is required and cannot be None')
        self._module = module

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'function')
    @serializable.xml_sequence(3)
    def function(self) -> Optional[str]:
        """
        The function name.
        """
        return self._function

    @function.setter
    def function(self, function: Optional[str]) -> None:
        """
        Sets the function name.
        """
        self._function = function

    @property
    @serializable.json_name('parameters')
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'parameter')
    @serializable.xml_sequence(4)
    def parameters(self) -> 'SortedSet[str]':
        """
        Function parameters
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters: Iterable[str]) -> None:
        self._parameters = SortedSet(parameters)

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'line')
    @serializable.xml_sequence(5)
    def line(self) -> Optional[int]:
        """
        The line number
        """
        return self._line

    @line.setter
    def line(self, line: Optional[int]) -> None:
        self._line = line

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'column')
    @serializable.xml_sequence(6)
    def column(self) -> Optional[int]:
        """
        The column number
        """
        return self._column

    @column.setter
    def column(self, column: Optional[int]) -> None:
        self._column = column

    @property
    @serializable.json_name('fullFilename')
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'fullFilename')
    @serializable.xml_sequence(7)
    def full_filename(self) -> Optional[str]:
        """
        The full file path
        """
        return self._full_filename

    @full_filename.setter
    def full_filename(self, full_filename: Optional[str]) -> None:
        self._full_filename = full_filename

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple(
            (
                self.package,
                self.module,
                self.function,
                _ComparableTuple(self.parameters),
                self.line,
                self.column,
                self.full_filename,
            )
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, StackFrame):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, StackFrame):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<StackFrame package={self.package}, module={self.module}, function={self.function}>'


@serializable.serializable_class
class CallStack:
    """
    Our internal representation of the `callStackType` complex type.
    Contains an array of stack frames describing a call stack from when a component was identified.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.6/json/#components_items_evidence_callstack
    """

    def __init__(
        self, *,
        frames: Optional[Iterable[StackFrame]] = None,
    ) -> None:
        self.frames = frames or []  # type:ignore[assignment]

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'frame')
    def frames(self) -> 'SortedSet[StackFrame]':
        """
        Array of stack frames
        """
        return self._frames

    @frames.setter
    def frames(self, frames: Iterable[StackFrame]) -> None:
        self._frames = SortedSet(frames)

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple(
            (
                _ComparableTuple(self.frames),
            )
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CallStack):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, CallStack):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<CallStack frames={len(self.frames)}>'


@serializable.serializable_class
class ComponentEvidence:
    """
    Our internal representation of the `componentEvidenceType` complex type.

    Provides the ability to document evidence collected through various forms of extraction or analysis.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.6/xml/#type_componentEvidenceType
    """

    def __init__(
        self, *,
        identity: Optional[Iterable[Identity]] = None,
        occurrences: Optional[Iterable[Occurrence]] = None,
        callstack: Optional[CallStack] = None,
        licenses: Optional[Iterable[License]] = None,
        copyright: Optional[Iterable[Copyright]] = None,
    ) -> None:
        self.identity = identity or []  # type:ignore[assignment]
        self.occurrences = occurrences or []  # type:ignore[assignment]
        self.callstack = callstack
        self.licenses = licenses or []  # type:ignore[assignment]
        self.copyright = copyright or []  # type:ignore[assignment]

    @property
    @serializable.view(SchemaVersion1Dot6)
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'identity')
    @serializable.xml_sequence(1)
    def identity(self) -> 'SortedSet[Identity]':
        """
        Provides a way to identify components via various methods.
        Returns SortedSet of identities.
        """
        return self._identity

    @identity.setter
    def identity(self, identity: Iterable[Identity]) -> None:
        self._identity = SortedSet(identity)

    @property
    # @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'occurrence')
    @serializable.xml_sequence(2)
    def occurrences(self) -> 'SortedSet[Occurrence]':
        """A list of locations where evidence was obtained from."""
        return self._occurrences

    @occurrences.setter
    def occurrences(self, occurrences: Iterable[Occurrence]) -> None:
        self._occurrences = SortedSet(occurrences)

    @property
    # @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.xml_sequence(3)
    def callstack(self) -> Optional[CallStack]:
        """
        A representation of a call stack from when the component was identified.
        """
        return self._callstack

    @callstack.setter
    def callstack(self, callstack: Optional[CallStack]) -> None:
        self._callstack = callstack

    @property
    @serializable.type_mapping(_LicenseRepositorySerializationHelper)
    @serializable.xml_sequence(4)
    def licenses(self) -> LicenseRepository:
        """
        Optional list of licenses obtained during analysis.

        Returns:
            Set of `LicenseChoice`
        """
        return self._licenses

    @licenses.setter
    def licenses(self, licenses: Iterable[License]) -> None:
        self._licenses = LicenseRepository(licenses)

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'text')
    @serializable.xml_sequence(5)
    def copyright(self) -> 'SortedSet[Copyright]':
        """
        Optional list of copyright statements.

        Returns:
             Set of `Copyright`
        """
        return self._copyright

    @copyright.setter
    def copyright(self, copyright: Iterable[Copyright]) -> None:
        self._copyright = SortedSet(copyright)

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple(
            (
                _ComparableTuple(self.licenses),
                _ComparableTuple(self.copyright),
                self.callstack,
                _ComparableTuple(self.identity),
                _ComparableTuple(self.occurrences),
            ))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ComponentEvidence):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<ComponentEvidence id={id(self)}>'
