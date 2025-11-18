"""CycloneDX Model Card data structures.

This module introduces support for the CycloneDX `modelCard` object (schema v1.5+).
Only the top-level container (`ModelCard`) is implemented here first; nested types
will follow in subsequent TODOs to keep changes reviewable.

References:
- CycloneDX 1.5/1.6/1.7 modelCardType definitions (JSON & XSD)
"""

from __future__ import annotations

from typing import Optional, Iterable, Any, Union
from enum import Enum

import py_serializable as serializable
from sortedcontainers import SortedSet

from .._internal.bom_ref import bom_ref_from_str as _bom_ref_from_str
from .bom_ref import BomRef
from . import Property, AttachedText
from ..schema.schema import (
    SchemaVersion1Dot5,
    SchemaVersion1Dot6,
    SchemaVersion1Dot7,
)
from .._internal.compare import ComparableTuple as _ComparableTuple


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class ModelCard:
    """Internal representation of CycloneDX `modelCardType`.

    Version gating:
    - Introduced in schema 1.5
    - Unchanged structurally in 1.6 except for additional nested environmental considerations inside `considerations`
    - 1.7 retains 1.6 structure (additions in nested types only)

    NOTE: Nested complex objects (modelParameters, quantitativeAnalysis, considerations) will be
    implemented in later steps. For now they are treated as opaque objects so that `Component.model_card`
    can reference this container.
    """

    def __init__(
            self, *,
            bom_ref: Optional[Union[str, BomRef]] = None,
            model_parameters: Optional['ModelParameters'] = None,
            quantitative_analysis: Optional[Any] = None,  # will be refined
            considerations: Optional[Any] = None,  # will be refined
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
    @serializable.xml_name('bom-ref')
    @serializable.xml_attribute()
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    def bom_ref(self) -> BomRef:
        return self._bom_ref

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(1)
    @serializable.json_name('modelParameters')
    @serializable.xml_name('modelParameters')
    def model_parameters(self) -> Optional['ModelParameters']:
        return self._model_parameters

    @model_parameters.setter
    def model_parameters(self, model_parameters: Optional['ModelParameters']) -> None:
        self._model_parameters = model_parameters

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(2)
    @serializable.json_name('quantitativeAnalysis')
    @serializable.xml_name('quantitativeAnalysis')
    def quantitative_analysis(self) -> Optional['QuantitativeAnalysis']:
        return self._quantitative_analysis

    @quantitative_analysis.setter
    def quantitative_analysis(self, quantitative_analysis: Optional['QuantitativeAnalysis']) -> None:
        self._quantitative_analysis = quantitative_analysis

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(3)
    def considerations(self) -> Optional[Any]:  # placeholder type
        return self._considerations

    @considerations.setter
    def considerations(self, considerations: Optional[Any]) -> None:
        self._considerations = considerations

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(4)
    def properties(self) -> 'SortedSet[Property]':
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

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<ModelCard bom-ref={self.bom_ref!r}>'


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
            datasets: Optional[Iterable[Any]] = None,  # TODO: refine (componentData or ref)
            inputs: Optional[Iterable[InputOutputMLParameters]] = None,
            outputs: Optional[Iterable[InputOutputMLParameters]] = None,
    ) -> None:
        self.approach = approach
        self.task = task
        self.architecture_family = architecture_family
        self.model_architecture = model_architecture
        self.datasets = datasets or []
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

    @property
    # NOTE on `datasets` placeholder (to be refined with #913):
    # The CycloneDX spec allows two shapes for each dataset entry under `modelParameters.datasets`:
    # - Inline dataset information via the `componentData` object (XSD: element `dataset` of type `componentDataType`)
    # - A reference object with a single child `ref` that points to an existing data component by bom-ref
    #   (XSD: element `ref` with union type of `refLinkType` or `bomLinkElementType`).
    #
    # In JSON (1.5/1.6/1.7) this is expressed as an array with items oneOf: { componentData | { ref: ... } }.
    # In XML (1.5/1.6/1.7) this is expressed as a choice between <ref>…</ref> or <dataset>…</dataset> entries.
    #
    # The parent issue (#913) tracks adding first-class support for Component.data (`component.data`) and its
    # associated types. To avoid duplicating transient types and serializers here, we intentionally keep the
    # `datasets` field as `SortedSet[Any]` for now. Once `component.data` is modeled, we will:
    # - Introduce a concrete type (e.g., `ModelDatasetEntry`) that can represent either a `componentData` inline
    #   object or a `{ref: ...}` reference, similar to how other union-like schemas are modeled in this codebase.
    # - Provide serialization helpers that emit either the `<dataset>` element (mapped to the `componentData` type)
    #   or the `<ref>` element, and the equivalent JSON oneOf shape, based on the actual instance provided.
    # - Ensure both `component.data` and `modelParameters.datasets` reuse the same `componentData` type definition
    #   and the same normalization logic, so producers/consumers see consistent structures across the BOM.
    #
    # Until #913 lands, using `Any` here keeps the public API unblocked for the `modelCard` work, while making the
    # intended future refinement explicit and localized.
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(5)
    @serializable.json_name('datasets')
    @serializable.xml_name('datasets')
    def datasets(self) -> 'SortedSet[Any]':  # TODO: refine type
        return self._datasets

    @datasets.setter
    def datasets(self, datasets: Iterable[Any]) -> None:
        self._datasets = SortedSet(datasets)

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
            _ComparableTuple(self.datasets),
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

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<QuantitativeAnalysis metrics={len(self.performance_metrics)}>'

# TODO GraphicsCollection, Graphic (using existing AttachedText for images)

# TODO Considerations, Risk, FairnessAssessment (+ environmental considerations for >=1.6)

# TODO only for 1.6/1.7: EnvironmentalConsiderations, EnergyConsumptions, EnergyConsumption, EnergyMeasure, Co2Measure, EnergyProvider, plus the activity/unit enums per XSD.

# TODO (not in this file)
# - Add `Component.model_card` with `@serializable.view` gating for 1.5/1.6/1.7.
# - Use `@serializable.xml_sequence(26)` and ensure correct JSON name `modelCard`.
# - Add to `__comparable_tuple` for equality/hash.

# TODO (not in this file)
# - JSON tests across views; XML order validation; round-trip tests.
# - Docs & changelog updates.
