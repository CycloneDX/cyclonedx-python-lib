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
This set of classes represents the model card types in the CycloneDX standard.

.. note::
    Introduced in CycloneDX v1.5. Environmental considerations were added in v1.6.

.. note::
    See the CycloneDX Schema for model cards:\n
    - XML: https://cyclonedx.org/docs/1.7/xml/#type_modelCardType\n
    - JSON: https://cyclonedx.org/docs/1.7/json/#components_items_modelCard
"""

from collections.abc import Iterable
from enum import Enum
from json import loads as json_loads  # add this near the top
from typing import Any, Optional, Union
from xml.etree.ElementTree import Element  # nosec B405

import py_serializable as serializable
from py_serializable import ViewType
from py_serializable.helpers import BaseHelper
from sortedcontainers import SortedSet

from .._internal.bom_ref import bom_ref_from_str as _bom_ref_from_str
from .._internal.compare import ComparableTuple as _ComparableTuple
from ..exception.serialization import CycloneDxDeserializationException
from ..schema.schema import SchemaVersion1Dot5, SchemaVersion1Dot6, SchemaVersion1Dot7
from . import AttachedText, ExternalReference, Property
from .bom_ref import BomRef
from .contact import OrganizationalEntity


@serializable.serializable_enum
class MachineLearningApproach(str, Enum):
    """Enumeration for `machineLearningApproachType`.

    Values are stable across 1.5–1.7.
    """
    SUPERVISED = 'supervised'
    UNSUPERVISED = 'unsupervised'
    REINFORCEMENT_LEARNING = 'reinforcement-learning'
    SEMI_SUPERVISED = 'semi-supervised'
    SELF_SUPERVISED = 'self-supervised'


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class Approach:
    """Container for the `approach` element within `modelParameters`."""

    def __init__(self, *, type: Optional[MachineLearningApproach] = None) -> None:
        self.type = type

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(1)
    def type(self) -> Optional[MachineLearningApproach]:
        return self._type

    @type.setter
    def type(self, type: Optional[MachineLearningApproach]) -> None:
        self._type = type

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((self.type,))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Approach):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Approach):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, Approach):
            return self.__comparable_tuple() <= other.__comparable_tuple()
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, Approach):
            return self.__comparable_tuple() >= other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<Approach type={self.type}>'


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class InputOutputMLParameters:
    """Definition for items under `modelParameters.inputs[]` and `outputs[]`."""

    def __init__(self, *, format: str) -> None:
        self.format = format

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(1)
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def format(self) -> str:
        return self._format

    @format.setter
    def format(self, format: str) -> None:
        self._format = format

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((self.format,))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, InputOutputMLParameters):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, InputOutputMLParameters):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, InputOutputMLParameters):
            return self.__comparable_tuple() <= other.__comparable_tuple()
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, InputOutputMLParameters):
            return self.__comparable_tuple() >= other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<IOParam format={self.format!r}>'


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class ModelParameters:
    """`modelParameters` block within `modelCard`."""

    def __init__(
            self, *,
            approach: Optional[Approach] = None,
            task: Optional[str] = None,
            architecture_family: Optional[str] = None,
            model_architecture: Optional[str] = None,
            datasets: Optional[Iterable[Any]] = None,  # Unsupported placeholder until #913 lands.
            inputs: Optional[Iterable[InputOutputMLParameters]] = None,
            outputs: Optional[Iterable[InputOutputMLParameters]] = None,
    ) -> None:
        self.approach = approach
        self.task = task
        self.architecture_family = architecture_family
        self.model_architecture = model_architecture
        # datasets: The CycloneDX spec allows inline componentData or ref entries.
        # This library has not yet implemented component.data (#913). To avoid emitting
        # invalid or partial structures, any attempt to populate datasets is rejected.
        if datasets is not None:
            datasets_list = list(datasets)
            if len(datasets_list) > 0:
                raise NotImplementedError(
                    'modelParameters.datasets is not yet supported. Tracked by issue #913.'
                )
        self._datasets: 'SortedSet[Any]' = SortedSet()  # always empty until implemented
        self.inputs = inputs or []
        self.outputs = outputs or []

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(1)
    def approach(self) -> Optional[Approach]:
        return self._approach

    @approach.setter
    def approach(self, approach: Optional[Approach]) -> None:
        self._approach = approach

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(2)
    @serializable.json_name('task')
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    @serializable.xml_name('task')
    def task(self) -> Optional[str]:
        return self._task

    @task.setter
    def task(self, task: Optional[str]) -> None:
        self._task = task

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(3)
    @serializable.json_name('architectureFamily')
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    @serializable.xml_name('architectureFamily')
    def architecture_family(self) -> Optional[str]:
        return self._architecture_family

    @architecture_family.setter
    def architecture_family(self, architecture_family: Optional[str]) -> None:
        self._architecture_family = architecture_family

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(4)
    @serializable.json_name('modelArchitecture')
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    @serializable.xml_name('modelArchitecture')
    def model_architecture(self) -> Optional[str]:
        return self._model_architecture

    @model_architecture.setter
    def model_architecture(self, model_architecture: Optional[str]) -> None:
        self._model_architecture = model_architecture

    # datasets intentionally omitted from serialization until #913 implemented.
    # A future implementation will add a concrete union type and proper annotations.

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(6)
    @serializable.json_name('inputs')
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'input')
    @serializable.xml_name('inputs')
    def inputs(self) -> 'SortedSet[InputOutputMLParameters]':
        return self._inputs

    @inputs.setter
    def inputs(self, inputs: Iterable[InputOutputMLParameters]) -> None:
        self._inputs = SortedSet(inputs)

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(7)
    @serializable.json_name('outputs')
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'output')
    @serializable.xml_name('outputs')
    def outputs(self) -> 'SortedSet[InputOutputMLParameters]':
        return self._outputs

    @outputs.setter
    def outputs(self, outputs: Iterable[InputOutputMLParameters]) -> None:
        self._outputs = SortedSet(outputs)

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((
            self.approach,
            self.task,
            self.architecture_family,
            self.model_architecture,
            _ComparableTuple(self._datasets),
            _ComparableTuple(self.inputs),
            _ComparableTuple(self.outputs),
        ))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ModelParameters):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, ModelParameters):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, ModelParameters):
            return self.__comparable_tuple() <= other.__comparable_tuple()
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, ModelParameters):
            return self.__comparable_tuple() >= other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<ModelParameters task={self.task!r} arch={self.model_architecture!r}>'


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class ConfidenceInterval:
    """Confidence interval with lower/upper bounds."""

    def __init__(self, *, lower_bound: Optional[str] = None, upper_bound: Optional[str] = None) -> None:
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(1)
    @serializable.json_name('lowerBound')
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    @serializable.xml_name('lowerBound')
    def lower_bound(self) -> Optional[str]:
        return self._lower_bound

    @lower_bound.setter
    def lower_bound(self, lower_bound: Optional[str]) -> None:
        self._lower_bound = lower_bound

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(2)
    @serializable.json_name('upperBound')
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    @serializable.xml_name('upperBound')
    def upper_bound(self) -> Optional[str]:
        return self._upper_bound

    @upper_bound.setter
    def upper_bound(self, upper_bound: Optional[str]) -> None:
        self._upper_bound = upper_bound

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((self.lower_bound, self.upper_bound))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ConfidenceInterval):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, ConfidenceInterval):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, ConfidenceInterval):
            return self.__comparable_tuple() <= other.__comparable_tuple()
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, ConfidenceInterval):
            return self.__comparable_tuple() >= other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<ConfidenceInterval {self.lower_bound},{self.upper_bound}>'


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class PerformanceMetric:
    """A single performance metric entry."""

    def __init__(
        self, *,
        type: Optional[str] = None,
        value: Optional[str] = None,
        slice: Optional[str] = None,
        confidence_interval: Optional[ConfidenceInterval] = None,
    ) -> None:
        self.type = type
        self.value = value
        self.slice = slice
        self.confidence_interval = confidence_interval

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(1)
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def type(self) -> Optional[str]:
        return self._type

    @type.setter
    def type(self, type: Optional[str]) -> None:
        self._type = type

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(2)
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def value(self) -> Optional[str]:
        return self._value

    @value.setter
    def value(self, value: Optional[str]) -> None:
        self._value = value

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(3)
    @serializable.json_name('slice')
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    @serializable.xml_name('slice')
    def slice(self) -> Optional[str]:
        return self._slice

    @slice.setter
    def slice(self, slice: Optional[str]) -> None:
        self._slice = slice

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(4)
    @serializable.json_name('confidenceInterval')
    @serializable.xml_name('confidenceInterval')
    def confidence_interval(self) -> Optional[ConfidenceInterval]:
        return self._confidence_interval

    @confidence_interval.setter
    def confidence_interval(self, confidence_interval: Optional[ConfidenceInterval]) -> None:
        self._confidence_interval = confidence_interval

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((self.type, self.value, self.slice, self.confidence_interval))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, PerformanceMetric):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, PerformanceMetric):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, PerformanceMetric):
            return self.__comparable_tuple() <= other.__comparable_tuple()
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, PerformanceMetric):
            return self.__comparable_tuple() >= other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<PerformanceMetric type={self.type!r} value={self.value!r}>'


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class Graphic:
    """Graphic entry with optional name and image (AttachedText)."""

    def __init__(self, *, name: Optional[str] = None, image: Optional[AttachedText] = None) -> None:
        self.name = name
        self.image = image

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(1)
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, name: Optional[str]) -> None:
        self._name = name

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(2)
    def image(self) -> Optional[AttachedText]:
        return self._image

    @image.setter
    def image(self, image: Optional[AttachedText]) -> None:
        self._image = image

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((self.name, self.image))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Graphic):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Graphic):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, Graphic):
            return self.__comparable_tuple() <= other.__comparable_tuple()
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, Graphic):
            return self.__comparable_tuple() >= other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<Graphic name={self.name!r}>'


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class GraphicsCollection:
    """A collection of graphics with optional description."""

    def __init__(self, *, description: Optional[str] = None, collection: Optional[Iterable[Graphic]] = None) -> None:
        self.description = description
        self.collection = collection or []

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(1)
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, description: Optional[str]) -> None:
        self._description = description

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(2)
    @serializable.json_name('collection')
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'graphic')
    @serializable.xml_name('collection')
    def collection(self) -> 'SortedSet[Graphic]':
        return self._collection

    @collection.setter
    def collection(self, collection: Iterable[Graphic]) -> None:
        self._collection = SortedSet(collection)

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((self.description, _ComparableTuple(self.collection)))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, GraphicsCollection):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, GraphicsCollection):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, GraphicsCollection):
            return self.__comparable_tuple() <= other.__comparable_tuple()
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, GraphicsCollection):
            return self.__comparable_tuple() >= other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<GraphicsCollection count={len(self.collection)}>'


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class QuantitativeAnalysis:
    """`quantitativeAnalysis` block within `modelCard`."""

    def __init__(
        self, *,
        performance_metrics: Optional[Iterable[PerformanceMetric]] = None,
        graphics: Optional[GraphicsCollection] = None,
    ) -> None:
        self.performance_metrics = performance_metrics or []
        self.graphics = graphics

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(1)
    @serializable.json_name('performanceMetrics')
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'performanceMetric')
    @serializable.xml_name('performanceMetrics')
    def performance_metrics(self) -> 'SortedSet[PerformanceMetric]':
        return self._performance_metrics

    @performance_metrics.setter
    def performance_metrics(self, performance_metrics: Iterable[PerformanceMetric]) -> None:
        self._performance_metrics = SortedSet(performance_metrics)

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(2)
    def graphics(self) -> Optional[GraphicsCollection]:
        return self._graphics

    @graphics.setter
    def graphics(self, graphics: Optional[GraphicsCollection]) -> None:
        self._graphics = graphics

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((_ComparableTuple(self.performance_metrics), self.graphics))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, QuantitativeAnalysis):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, QuantitativeAnalysis):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, QuantitativeAnalysis):
            return self.__comparable_tuple() <= other.__comparable_tuple()
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, QuantitativeAnalysis):
            return self.__comparable_tuple() >= other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<QuantitativeAnalysis metrics={len(self.performance_metrics)}>'


# Considerations and nested structures

@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class EthicalConsideration:
    """Entry in `ethicalConsiderations` with name and mitigation strategy."""

    def __init__(self, *, name: Optional[str] = None, mitigation_strategy: Optional[str] = None) -> None:
        self.name = name
        self.mitigation_strategy = mitigation_strategy

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(1)
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, name: Optional[str]) -> None:
        self._name = name

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(2)
    @serializable.json_name('mitigationStrategy')
    @serializable.xml_name('mitigationStrategy')
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def mitigation_strategy(self) -> Optional[str]:
        return self._mitigation_strategy

    @mitigation_strategy.setter
    def mitigation_strategy(self, mitigation_strategy: Optional[str]) -> None:
        self._mitigation_strategy = mitigation_strategy

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((self.name, self.mitigation_strategy))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, EthicalConsideration):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, EthicalConsideration):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, EthicalConsideration):
            return self.__comparable_tuple() <= other.__comparable_tuple()
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, EthicalConsideration):
            return self.__comparable_tuple() >= other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<EthicalConsideration name={self.name!r}>'


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class FairnessAssessment:
    """Entry in `fairnessAssessments`."""

    def __init__(
        self, *,
        group_at_risk: Optional[str] = None,
        benefits: Optional[str] = None,
        harms: Optional[str] = None,
        mitigation_strategy: Optional[str] = None,
    ) -> None:
        self.group_at_risk = group_at_risk
        self.benefits = benefits
        self.harms = harms
        self.mitigation_strategy = mitigation_strategy

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(1)
    @serializable.json_name('groupAtRisk')
    @serializable.xml_name('groupAtRisk')
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def group_at_risk(self) -> Optional[str]:
        return self._group_at_risk

    @group_at_risk.setter
    def group_at_risk(self, group_at_risk: Optional[str]) -> None:
        self._group_at_risk = group_at_risk

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(2)
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def benefits(self) -> Optional[str]:
        return self._benefits

    @benefits.setter
    def benefits(self, benefits: Optional[str]) -> None:
        self._benefits = benefits

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(3)
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def harms(self) -> Optional[str]:
        return self._harms

    @harms.setter
    def harms(self, harms: Optional[str]) -> None:
        self._harms = harms

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(4)
    @serializable.json_name('mitigationStrategy')
    @serializable.xml_name('mitigationStrategy')
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def mitigation_strategy(self) -> Optional[str]:
        return self._mitigation_strategy

    @mitigation_strategy.setter
    def mitigation_strategy(self, mitigation_strategy: Optional[str]) -> None:
        self._mitigation_strategy = mitigation_strategy

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((self.group_at_risk, self.benefits, self.harms, self.mitigation_strategy))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, FairnessAssessment):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, FairnessAssessment):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, FairnessAssessment):
            return self.__comparable_tuple() <= other.__comparable_tuple()
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, FairnessAssessment):
            return self.__comparable_tuple() >= other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<FairnessAssessment group_at_risk={self.group_at_risk!r}>'


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class EnvironmentalConsiderations:
    """Environmental considerations (1.6+). Energy consumptions and properties.

    NOTE: Prior revisions kept `energy_consumptions` opaque. This has been replaced by
    concrete types that match CycloneDX 1.6+/1.7 schema: `EnergyConsumption`, `EnergyMeasure`,
    `Co2Measure`, `EnergyProvider`, and enumerations for `activity` and `energySource`.
    """

    def __init__(
        self, *,
        energy_consumptions: Optional[Iterable['EnergyConsumption']] = None,
        properties: Optional[Iterable[Property]] = None,
    ) -> None:
        self.energy_consumptions = energy_consumptions or []
        self.properties = properties or []

    @property
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(1)
    @serializable.json_name('energyConsumptions')
    @serializable.xml_name('energyConsumptions')
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'energyConsumption')
    def energy_consumptions(self) -> 'SortedSet[EnergyConsumption]':
        return self._energy_consumptions

    @energy_consumptions.setter
    def energy_consumptions(self, energy_consumptions: Iterable['EnergyConsumption']) -> None:
        self._energy_consumptions = SortedSet(energy_consumptions)

    @property
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(2)
    @serializable.xml_name('properties')
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'property')
    def properties(self) -> 'SortedSet[Property]':
        return self._properties

    @properties.setter
    def properties(self, properties: Iterable[Property]) -> None:
        self._properties = SortedSet(properties)

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((_ComparableTuple(self.energy_consumptions), _ComparableTuple(self.properties)))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, EnvironmentalConsiderations):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, EnvironmentalConsiderations):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, EnvironmentalConsiderations):
            return self.__comparable_tuple() <= other.__comparable_tuple()
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, EnvironmentalConsiderations):
            return self.__comparable_tuple() >= other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<EnvironmentalConsiderations energies={len(self.energy_consumptions)}>'


@serializable.serializable_enum
class EnergyActivity(str, Enum):
    """Enumeration for lifecycle activity in `energyConsumption.activity` (1.6+)."""
    DESIGN = 'design'
    DATA_COLLECTION = 'data-collection'
    DATA_PREPARATION = 'data-preparation'
    TRAINING = 'training'
    FINE_TUNING = 'fine-tuning'
    VALIDATION = 'validation'
    DEPLOYMENT = 'deployment'
    INFERENCE = 'inference'
    OTHER = 'other'


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class EnergyMeasure:
    """A measure of energy. Schema `energyMeasure` (1.6+): value + unit (kWh)."""

    def __init__(self, *, value: float, unit: str = 'kWh') -> None:
        self.value = value
        self.unit = unit

    @property
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(1)
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value: float) -> None:
        self._value = value

    @property
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(2)
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def unit(self) -> str:
        return self._unit

    @unit.setter
    def unit(self, unit: str) -> None:
        # Spec allows only "kWh"
        self._unit = unit

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((self.value, self.unit))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, EnergyMeasure):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, EnergyMeasure):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, EnergyMeasure):
            return self.__comparable_tuple() <= other.__comparable_tuple()
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, EnergyMeasure):
            return self.__comparable_tuple() >= other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<EnergyMeasure {self.value} {self.unit}>'


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class Co2Measure:
    """A measure of CO2. Schema `co2Measure` (1.6+): value + unit (tCO2eq)."""

    def __init__(self, *, value: float, unit: str = 'tCO2eq') -> None:
        self.value = value
        self.unit = unit

    @property
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(1)
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value: float) -> None:
        self._value = value

    @property
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(2)
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def unit(self) -> str:
        return self._unit

    @unit.setter
    def unit(self, unit: str) -> None:
        # Spec allows only "tCO2eq"
        self._unit = unit

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((self.value, self.unit))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Co2Measure):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Co2Measure):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, Co2Measure):
            return self.__comparable_tuple() <= other.__comparable_tuple()
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, Co2Measure):
            return self.__comparable_tuple() >= other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<Co2Measure {self.value} {self.unit}>'


@serializable.serializable_enum
class EnergySource(str, Enum):
    """Enumeration for provider `energySource` (1.6+)."""
    COAL = 'coal'
    OIL = 'oil'
    NATURAL_GAS = 'natural-gas'
    NUCLEAR = 'nuclear'
    WIND = 'wind'
    SOLAR = 'solar'
    GEOTHERMAL = 'geothermal'
    HYDROPOWER = 'hydropower'
    BIOFUEL = 'biofuel'
    UNKNOWN = 'unknown'
    OTHER = 'other'


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class EnergyProvider:
    """Energy provider per schema `energyProvider` (1.6+)."""

    def __init__(
        self, *,
        organization: OrganizationalEntity,
        energy_source: EnergySource,
        energy_provided: EnergyMeasure,
        bom_ref: Optional[Union[str, BomRef]] = None,
        description: Optional[str] = None,
        external_references: Optional[Iterable[ExternalReference]] = None,
    ) -> None:
        self._bom_ref = _bom_ref_from_str(bom_ref) if bom_ref is not None else _bom_ref_from_str(None)
        self.description = description
        self.organization = organization
        self.energy_source = energy_source
        self.energy_provided = energy_provided
        self.external_references = external_references or []

    @property
    @serializable.json_name('bom-ref')
    @serializable.type_mapping(BomRef)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_attribute()
    @serializable.xml_name('bom-ref')
    def bom_ref(self) -> BomRef:
        return self._bom_ref

    @property
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(1)
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, description: Optional[str]) -> None:
        self._description = description

    @property
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(2)
    def organization(self) -> OrganizationalEntity:
        return self._organization

    @organization.setter
    def organization(self, organization: OrganizationalEntity) -> None:
        self._organization = organization

    @property
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(3)
    @serializable.json_name('energySource')
    @serializable.xml_name('energySource')
    def energy_source(self) -> EnergySource:
        return self._energy_source

    @energy_source.setter
    def energy_source(self, energy_source: EnergySource) -> None:
        self._energy_source = energy_source

    @property
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(4)
    @serializable.json_name('energyProvided')
    @serializable.xml_name('energyProvided')
    def energy_provided(self) -> EnergyMeasure:
        return self._energy_provided

    @energy_provided.setter
    def energy_provided(self, energy_provided: EnergyMeasure) -> None:
        self._energy_provided = energy_provided

    @property
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(5)
    @serializable.xml_name('externalReferences')
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'reference')
    def external_references(self) -> 'SortedSet[ExternalReference]':
        return self._external_references

    @external_references.setter
    def external_references(self, external_references: Iterable[ExternalReference]) -> None:
        self._external_references = SortedSet(external_references)

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((
            self._bom_ref.value,
            self.description,
            self.organization,
            self.energy_source,
            self.energy_provided,
            _ComparableTuple(self.external_references),
        ))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, EnergyProvider):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, EnergyProvider):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, EnergyProvider):
            return self.__comparable_tuple() <= other.__comparable_tuple()
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, EnergyProvider):
            return self.__comparable_tuple() >= other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<EnergyProvider org={self.organization.name!r} source={self.energy_source}>'


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class EnergyConsumption:
    """Energy consumption entry. Matches schema `energyConsumption` (1.6+)."""

    def __init__(
        self, *,
        activity: EnergyActivity,
        energy_providers: Iterable[EnergyProvider],
        activity_energy_cost: EnergyMeasure,
        co2_cost_equivalent: Optional[Co2Measure] = None,
        co2_cost_offset: Optional[Co2Measure] = None,
        properties: Optional[Iterable[Property]] = None,
    ) -> None:
        self.activity = activity
        self.energy_providers = energy_providers
        self.activity_energy_cost = activity_energy_cost
        self.co2_cost_equivalent = co2_cost_equivalent
        self.co2_cost_offset = co2_cost_offset
        self.properties = properties or []

    @property
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(1)
    def activity(self) -> EnergyActivity:
        return self._activity

    @activity.setter
    def activity(self, activity: EnergyActivity) -> None:
        self._activity = activity

    @property
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(2)
    @serializable.json_name('energyProviders')
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'energyProviders')
    def energy_providers(self) -> 'SortedSet[EnergyProvider]':
        return self._energy_providers

    @energy_providers.setter
    def energy_providers(self, energy_providers: Iterable[EnergyProvider]) -> None:
        self._energy_providers = SortedSet(energy_providers)

    @property
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(3)
    @serializable.json_name('activityEnergyCost')
    @serializable.xml_name('activityEnergyCost')
    def activity_energy_cost(self) -> EnergyMeasure:
        return self._activity_energy_cost

    @activity_energy_cost.setter
    def activity_energy_cost(self, activity_energy_cost: EnergyMeasure) -> None:
        self._activity_energy_cost = activity_energy_cost

    @property
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(4)
    @serializable.json_name('co2CostEquivalent')
    @serializable.xml_name('co2CostEquivalent')
    def co2_cost_equivalent(self) -> Optional[Co2Measure]:
        return self._co2_cost_equivalent

    @co2_cost_equivalent.setter
    def co2_cost_equivalent(self, co2_cost_equivalent: Optional[Co2Measure]) -> None:
        self._co2_cost_equivalent = co2_cost_equivalent

    @property
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(5)
    @serializable.json_name('co2CostOffset')
    @serializable.xml_name('co2CostOffset')
    def co2_cost_offset(self) -> Optional[Co2Measure]:
        return self._co2_cost_offset

    @co2_cost_offset.setter
    def co2_cost_offset(self, co2_cost_offset: Optional[Co2Measure]) -> None:
        self._co2_cost_offset = co2_cost_offset

    @property
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(6)
    @serializable.xml_name('properties')
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'property')
    def properties(self) -> 'SortedSet[Property]':
        return self._properties

    @properties.setter
    def properties(self, properties: Iterable[Property]) -> None:
        self._properties = SortedSet(properties)

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((
            self.activity,
            _ComparableTuple(self.energy_providers),
            self.activity_energy_cost,
            self.co2_cost_equivalent,
            self.co2_cost_offset,
            _ComparableTuple(self.properties),
        ))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, EnergyConsumption):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, EnergyConsumption):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, EnergyConsumption):
            return self.__comparable_tuple() <= other.__comparable_tuple()
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, EnergyConsumption):
            return self.__comparable_tuple() >= other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return (
            f'<EnergyConsumption activity={self.activity} providers={len(self.energy_providers)} '
            f'energy={self.activity_energy_cost}>'
        )


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class Considerations:
    """`considerations` block within `modelCard`."""

    def __init__(
        self, *,
        users: Optional[Iterable[str]] = None,
        use_cases: Optional[Iterable[str]] = None,
        technical_limitations: Optional[Iterable[str]] = None,
        performance_tradeoffs: Optional[Iterable[str]] = None,
        ethical_considerations: Optional[Iterable[EthicalConsideration]] = None,
        environmental_considerations: Optional[EnvironmentalConsiderations] = None,
        fairness_assessments: Optional[Iterable[FairnessAssessment]] = None,
    ) -> None:
        self.users = users or []
        self.use_cases = use_cases or []
        self.technical_limitations = technical_limitations or []
        self.performance_tradeoffs = performance_tradeoffs or []
        self.ethical_considerations = ethical_considerations or []
        self.environmental_considerations = environmental_considerations
        self.fairness_assessments = fairness_assessments or []

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(1)
    @serializable.xml_name('users')
    @serializable.json_name('users')
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'user')
    def users(self) -> 'SortedSet[str]':
        return self._users

    @users.setter
    def users(self, users: Iterable[str]) -> None:
        self._users = SortedSet(users)

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(2)
    @serializable.json_name('useCases')
    @serializable.xml_name('useCases')
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'useCase')
    def use_cases(self) -> 'SortedSet[str]':
        return self._use_cases

    @use_cases.setter
    def use_cases(self, use_cases: Iterable[str]) -> None:
        self._use_cases = SortedSet(use_cases)

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(3)
    @serializable.json_name('technicalLimitations')
    @serializable.xml_name('technicalLimitations')
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'technicalLimitation')
    def technical_limitations(self) -> 'SortedSet[str]':
        return self._technical_limitations

    @technical_limitations.setter
    def technical_limitations(self, technical_limitations: Iterable[str]) -> None:
        self._technical_limitations = SortedSet(technical_limitations)

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(4)
    @serializable.json_name('performanceTradeoffs')
    @serializable.xml_name('performanceTradeoffs')
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'performanceTradeoff')
    def performance_tradeoffs(self) -> 'SortedSet[str]':
        return self._performance_tradeoffs

    @performance_tradeoffs.setter
    def performance_tradeoffs(self, performance_tradeoffs: Iterable[str]) -> None:
        self._performance_tradeoffs = SortedSet(performance_tradeoffs)

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(5)
    @serializable.json_name('ethicalConsiderations')
    @serializable.xml_name('ethicalConsiderations')
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'ethicalConsideration')
    def ethical_considerations(self) -> 'SortedSet[EthicalConsideration]':
        return self._ethical_considerations

    @ethical_considerations.setter
    def ethical_considerations(self, ethical_considerations: Iterable[EthicalConsideration]) -> None:
        self._ethical_considerations = SortedSet(ethical_considerations)

    @property
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(6)
    @serializable.json_name('environmentalConsiderations')
    @serializable.xml_name('environmentalConsiderations')
    def environmental_considerations(self) -> Optional[EnvironmentalConsiderations]:
        return self._environmental_considerations

    @environmental_considerations.setter
    def environmental_considerations(self, environmental_considerations: Optional[EnvironmentalConsiderations]) -> None:
        self._environmental_considerations = environmental_considerations

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(7)
    @serializable.json_name('fairnessAssessments')
    @serializable.xml_name('fairnessAssessments')
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'fairnessAssessment')
    def fairness_assessments(self) -> 'SortedSet[FairnessAssessment]':
        return self._fairness_assessments

    @fairness_assessments.setter
    def fairness_assessments(self, fairness_assessments: Iterable[FairnessAssessment]) -> None:
        self._fairness_assessments = SortedSet(fairness_assessments)

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((
            _ComparableTuple(self.users),
            _ComparableTuple(self.use_cases),
            _ComparableTuple(self.technical_limitations),
            _ComparableTuple(self.performance_tradeoffs),
            _ComparableTuple(self.ethical_considerations),
            self.environmental_considerations,
            _ComparableTuple(self.fairness_assessments),
        ))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Considerations):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Considerations):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, Considerations):
            return self.__comparable_tuple() <= other.__comparable_tuple()
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, Considerations):
            return self.__comparable_tuple() >= other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return (
            f'<Considerations users={len(self.users)} useCases={len(self.use_cases)} '
            f'ethics={len(self.ethical_considerations)} fairness={len(self.fairness_assessments)}>'
        )


class _ModelCardPropertiesSerializationHelper(BaseHelper):
    """THIS CLASS IS NON-PUBLIC API

    Handles asymmetric serialization for ModelCard.properties:
        - JSON: emits a list of property objects.
        - XML: omits the element entirely (until spec discrepancy is fixed).
            See: https://github.com/CycloneDX/specification/issues/726
    """

    # Done this similar to LicenseRepositorySerializationHelper
    @classmethod
    def json_normalize(cls, o: Iterable[Property], *,
                       view: Optional[type[ViewType]],
                       **__: Any) -> Optional[list[dict[str, Any]]]:
        # Normalize each Property by parsing its as_json(view_=view) output back into a dict
        assert view is not None
        o_list = list(o)
        if not o_list:
            return None
        return [json_loads(p.as_json(view_=view)) for p in o_list]  # type: ignore[attr-defined]

    @classmethod
    def json_denormalize(cls, o: list[dict[str, Any]], **__: Any) -> SortedSet[Property]:
        return SortedSet(Property(name=it.get('name', ''), value=it.get('value')) for it in o)

    @classmethod
    def xml_normalize(cls, o: Iterable[Property], *,
                      element_name: str,
                      view: Optional[type[ViewType]],
                      xmlns: Optional[str],
                      **__: Any) -> Optional[Element]:
        # Intentionally omit due to XML spec gap (spec issue #726)
        return None

    @classmethod
    def xml_denormalize(cls, o: Optional[Element],
                        default_ns: Optional[str],
                        **__: Any) -> SortedSet[Property]:
        # Accept properties if present even though we currently do not emit them in XML
        if o is None:
            return SortedSet()

        ns_prefix = f'{{{default_ns}}}' if default_ns else None
        properties: list[Property] = []

        for child in o:
            tag = child.tag
            if ns_prefix and tag.startswith(ns_prefix):
                tag = tag[len(ns_prefix):]

            if tag != 'property':
                raise CycloneDxDeserializationException(f'unexpected: {child!r}')

            properties.append(Property(
                name=child.attrib.get('name', ''),
                value=child.text
            ))

        return SortedSet(properties)


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class ModelCard:
    """Internal representation of CycloneDX `modelCardType`.

    Version gating:
    - Introduced in schema 1.5
    - Unchanged structurally in 1.6 except for additional nested environmental considerations inside `considerations`
    - 1.7 retains 1.6 structure (additions in nested types only)
    """

    def __init__(
            self, *,
            bom_ref: Optional[Union[str, BomRef]] = None,
            model_parameters: Optional[ModelParameters] = None,
            quantitative_analysis: Optional[QuantitativeAnalysis] = None,
            considerations: Optional[Considerations] = None,
            properties: Optional[Iterable[Property]] = None,
    ) -> None:
        self._bom_ref = _bom_ref_from_str(bom_ref) if bom_ref is not None else _bom_ref_from_str(None)
        self.model_parameters = model_parameters
        self.quantitative_analysis = quantitative_analysis
        self.considerations = considerations
        self.properties = properties or []

    # bom-ref attribute
    @property
    @serializable.json_name('bom-ref')
    @serializable.type_mapping(BomRef)
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_attribute()
    @serializable.xml_name('bom-ref')
    def bom_ref(self) -> BomRef:
        return self._bom_ref

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(1)
    @serializable.json_name('modelParameters')
    @serializable.xml_name('modelParameters')
    def model_parameters(self) -> Optional[ModelParameters]:
        return self._model_parameters

    @model_parameters.setter
    def model_parameters(self, model_parameters: Optional[ModelParameters]) -> None:
        self._model_parameters = model_parameters

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(2)
    @serializable.json_name('quantitativeAnalysis')
    @serializable.xml_name('quantitativeAnalysis')
    def quantitative_analysis(self) -> Optional[QuantitativeAnalysis]:
        return self._quantitative_analysis

    @quantitative_analysis.setter
    def quantitative_analysis(self, quantitative_analysis: Optional[QuantitativeAnalysis]) -> None:
        self._quantitative_analysis = quantitative_analysis

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(3)
    @serializable.json_name('considerations')
    @serializable.xml_name('considerations')
    def considerations(self) -> Optional[Considerations]:
        return self._considerations

    @considerations.setter
    def considerations(self, considerations: Optional[Considerations]) -> None:
        self._considerations = considerations

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.type_mapping(_ModelCardPropertiesSerializationHelper)
    def properties(self) -> 'SortedSet[Property]':
        """
        Provides the ability to document properties in a key/value store. This provides flexibility to include data not
        officially supported in the standard without having to use additional namespaces or create extensions.

        Return:
            Set of `Property`
        """
        return self._properties

    @properties.setter
    def properties(self, properties: Iterable[Property]) -> None:
        self._properties = SortedSet(properties)

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((
            self.bom_ref.value,
            self.model_parameters,
            self.quantitative_analysis,
            self.considerations,
            _ComparableTuple(self.properties),
        ))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ModelCard):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, ModelCard):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, ModelCard):
            return self.__comparable_tuple() <= other.__comparable_tuple()
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, ModelCard):
            return self.__comparable_tuple() >= other.__comparable_tuple()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<ModelCard bom-ref={self.bom_ref!r}>'
