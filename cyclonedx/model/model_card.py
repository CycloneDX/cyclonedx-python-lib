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
from . import Property
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
    def quantitative_analysis(self) -> Optional[Any]:  # placeholder type
        return self._quantitative_analysis

    @quantitative_analysis.setter
    def quantitative_analysis(self, quantitative_analysis: Optional[Any]) -> None:
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
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
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
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
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
    @serializable.xml_string(serializable.XmlStringSerializationType.NORMALIZED_STRING)
    def model_architecture(self) -> Optional[str]:
        return self._model_architecture

    @model_architecture.setter
    def model_architecture(self, model_architecture: Optional[str]) -> None:
        self._model_architecture = model_architecture

    @property
    @serializable.view(SchemaVersion1Dot5)
    @serializable.view(SchemaVersion1Dot6)
    @serializable.view(SchemaVersion1Dot7)
    @serializable.xml_sequence(5)
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
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'input')
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
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'output')
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

# TODO PerformanceMetric, ConfidenceInterval

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
