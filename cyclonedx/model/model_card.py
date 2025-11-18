"""CycloneDX Model Card data structures.

This module introduces support for the CycloneDX `modelCard` object (schema v1.5+).
Only the top-level container (`ModelCard`) is implemented here first; nested types
will follow in subsequent TODOs to keep changes reviewable.

References:
- CycloneDX 1.5/1.6/1.7 modelCardType definitions (JSON & XSD)
"""

from __future__ import annotations

from typing import Optional, Iterable, Any, Union

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
		model_parameters: Optional[Any] = None,  # will be refined
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
	def model_parameters(self) -> Optional[Any]:  # placeholder type
		return self._model_parameters

	@model_parameters.setter
	def model_parameters(self, model_parameters: Optional[Any]) -> None:
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


# TODO ModelParameters, MachineLearningApproach enum, InputOutputMLParameters

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