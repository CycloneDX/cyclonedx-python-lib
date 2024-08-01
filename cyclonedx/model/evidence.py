# This file is part of CycloneDX Python Lib
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

from enum import Enum
from typing import Any, Dict, FrozenSet, Iterable, Optional, Type

import serializable

from ..exception.model import InvalidEvidenceConfidenceScore
from ..schema.schema import SchemaVersion1Dot5, SchemaVersion1Dot6


@serializable.serializable_enum
class EvidenceIdentityField(str, Enum):
    """
    Enum object that defines the permissable 'field' for a EvidenceIdentity according to the CycloneDX schema.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.5/xml/#type_identityFieldType
    """
    # see `_EvidenceIdentityFieldSerializationHelper.__CASES` for view/case map
    GROUP = 'group'
    NAME = 'name'
    VERSION = 'version'
    PURL = 'purl'
    CPE = 'cpe'
    SWID = 'swid'
    HASH = 'hash'


class _EvidenceIdentityFieldSerializationHelper(serializable.helpers.BaseHelper):
    """  THIS CLASS IS NON-PUBLIC API  """

    __CASES: Dict[Type[serializable.ViewType], FrozenSet[EvidenceIdentityField]] = dict()
    __CASES[SchemaVersion1Dot5] = frozenset({
        EvidenceIdentityField.GROUP,
        EvidenceIdentityField.NAME,
        EvidenceIdentityField.VERSION,
        EvidenceIdentityField.PURL,
        EvidenceIdentityField.CPE,
        EvidenceIdentityField.SWID,
        EvidenceIdentityField.HASH,
    })
    __CASES[SchemaVersion1Dot6] = __CASES[SchemaVersion1Dot5]

    @classmethod
    def __normalize(cls, cs: EvidenceIdentityField, view: Type[serializable.ViewType]) -> Optional[str]:
        return cs.value \
            if cs in cls.__CASES.get(view, ()) \
            else None

    @classmethod
    def json_normalize(cls, o: Any, *,
                       view: Optional[Type[serializable.ViewType]],
                       **__: Any) -> Optional[str]:
        assert view is not None
        return cls.__normalize(o, view)

    @classmethod
    def xml_normalize(cls, o: Any, *,
                      view: Optional[Type[serializable.ViewType]],
                      **__: Any) -> Optional[str]:
        assert view is not None
        return cls.__normalize(o, view)

    @classmethod
    def deserialize(cls, o: Any) -> EvidenceIdentityField:
        return EvidenceIdentityField(o)


@serializable.serializable_enum
class EvidenceTechnique(str, Enum):
    """
    Enum object that defines the permissable 'technique' for a EvidenceMethod according to the CycloneDX schema.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.5/xml/#type_componentEvidenceType
    """
    # see `_EvidenceTechniqueSerializationHelper.__CASES` for view/case map
    SOURCE_CODE_ANALYSIS = 'source-code-analysis'
    BINARY_ANALYSIS = 'binary-analysis'
    MANIFEST_ANALYSIS = 'manifest-analysis'
    AST_FINGERPRINT = 'ast-fingerprint'
    HASH_COMPARISON = 'hash-comparison'
    INSTRUMENTATION = 'instrumentation'
    DYNAMIC_ANALISYS = 'dynamic-analysis'
    FILENAME = 'filename'
    ATTESTATION = 'attestation'
    OTHER = 'other'


class _EvidenceTechniqueSerializationHelper(serializable.helpers.BaseHelper):
    """  THIS CLASS IS NON-PUBLIC API  """

    __CASES: Dict[Type[serializable.ViewType], FrozenSet[EvidenceTechnique]] = dict()
    __CASES[SchemaVersion1Dot5] = frozenset({
        EvidenceTechnique.SOURCE_CODE_ANALYSIS,
        EvidenceTechnique.BINARY_ANALYSIS,
        EvidenceTechnique.MANIFEST_ANALYSIS,
        EvidenceTechnique.AST_FINGERPRINT,
        EvidenceTechnique.HASH_COMPARISON,
        EvidenceTechnique.INSTRUMENTATION,
        EvidenceTechnique.DYNAMIC_ANALISYS,
        EvidenceTechnique.FILENAME,
        EvidenceTechnique.ATTESTATION,
        EvidenceTechnique.OTHER,
    })
    __CASES[SchemaVersion1Dot6] = __CASES[SchemaVersion1Dot5]

    @classmethod
    def __normalize(cls, cs: EvidenceTechnique, view: Type[serializable.ViewType]) -> Optional[str]:
        return cs.value \
            if cs in cls.__CASES.get(view, ()) \
            else None

    @classmethod
    def json_normalize(cls, o: Any, *,
                       view: Optional[Type[serializable.ViewType]],
                       **__: Any) -> Optional[str]:
        assert view is not None
        return cls.__normalize(o, view)

    @classmethod
    def xml_normalize(cls, o: Any, *,
                      view: Optional[Type[serializable.ViewType]],
                      **__: Any) -> Optional[str]:
        assert view is not None
        return cls.__normalize(o, view)

    @classmethod
    def deserialize(cls, o: Any) -> EvidenceTechnique:
        return EvidenceTechnique(o)


@serializable.serializable_class
class EvidenceMethod:
    """
    Our internal representation of the Method in `componentEvidenceType` complex type.

    Provides the ability to document method for how evidence was collected through
    various forms of extraction or analysis.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_componentEvidenceType
    """

    def __init__(self, *, technique: EvidenceTechnique, confidence: int, value: Optional[str] = None) -> None:
        self.technique = technique
        self.confidence = confidence
        self.value = value

    @property
    @serializable.type_mapping(_EvidenceTechniqueSerializationHelper)
    def technique(self) -> Optional[EvidenceTechnique]:
        """
        The evidence technique of the component which the evidence describes.

        Returns:
            `EvidenceTechnique` or `None`
        """
        return self._technique

    @technique.setter
    def technique(self, technique: Optional[EvidenceTechnique]) -> None:
        self._technique = technique

    @property
    def confidence(self) -> int:
        """
        The overall confidence of the evidence from 0 - 1, where 1 is 100% confidence.

        Confidence is specific to the technique used. Each technique of analysis can have independent confidence.

        Returns:
            `int`
        """
        return self._confidence

    @confidence.setter
    def confidence(self, confidence: int) -> None:
        if confidence < 0 or confidence > 1:
            raise InvalidEvidenceConfidenceScore(
                'Evidence confidence score must be (0 <= value <= 1)'
            )

        self._confidence = confidence

    @property
    def value(self) -> Optional[str]:
        """
        The value or contents of the evidence.

        Returns:
            `str` or `None`
        """
        return self._value

    @value.setter
    def value(self, value: Optional[str]) -> None:
        self._value = value


@serializable.serializable_class
class EvidenceIdentity:
    """
    Our internal representation of the Identity in `componentEvidenceType` complex type.

    Provides the ability to document component identity as part of the evidence collected
    through various forms of extraction or analysis.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_componentEvidenceType
    """

    def __init__(
            self, *,
            field: EvidenceIdentityField,
            confidence: Optional[int] = None,
            methods: Optional[Iterable[EvidenceMethod]] = None,
            tools: Optional[Iterable[str]]
    ) -> None:
        self.field = field
        self.confidence = confidence or None
        self.methods = methods or None
        self.tools = tools or None

    @property
    @serializable.type_mapping(_EvidenceIdentityFieldSerializationHelper)
    def field(self) -> Optional[EvidenceIdentityField]:
        """
        The identity field of the component which the evidence describes.

        Returns:
            `EvidenceIdentityField` or `None`
        """
        return self._field

    @field.setter
    def field(self, field: Optional[EvidenceIdentityField]) -> None:
        self._field = field

    @property
    def confidence(self) -> Optional[int]:
        """
        The overall confidence of the evidence from 0 - 1, where 1 is 100% confidence.

        Returns:
            `int` or `None`
        """
        return self._confidence

    @confidence.setter
    def confidence(self, confidence: Optional[int]) -> None:
        if confidence is not None and (confidence < 0 or confidence > 1):
            raise InvalidEvidenceConfidenceScore(
                'Evidence confidence score must be (0 <= value <= 1)'
            )

        self._confidence = confidence

    @property
    @serializable.type_mapping(EvidenceMethod)
    def methods(self) -> Optional[Iterable[EvidenceMethod]]:
        """
        Optional list of methods used to extract and/or analyze the evidence.

        Returns:
            `Iterable[EvidenceMethod]` or `None`
        """
        return self._methods

    @methods.setter
    def methods(self, methods: Optional[Iterable[EvidenceMethod]]) -> None:
        self._methods = methods

    @property
    def tools(self) -> Optional[Iterable[str]]:
        """
        Optional list of tools used to extract and/or analyze the evidence.

        Returns:
            `Iterable[str]` or `None`
        """
        return self._tools

    @tools.setter
    def tools(self, tools: Optional[Iterable[str]]) -> None:
        self._tools = tools
