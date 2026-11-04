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
This set of classes represents the data about Citations.

.. note::
    Introduced in CycloneDX v1.7

.. note::
    See the CycloneDX Schema extension definition https://cyclonedx.org/docs/1.7/xml/#type_citationType
"""

from collections.abc import Iterable
from datetime import datetime
from typing import Any, Optional, Union

import py_serializable as serializable
from sortedcontainers import SortedSet

from .._internal.bom_ref import bom_ref_from_str as _bom_ref_from_str
from .._internal.compare import ComparableTuple as _ComparableTuple
from ..exception.model import MutuallyExclusivePropertiesException, NoPropertiesProvidedException
from .bom_ref import BomRef


@serializable.serializable_class(ignore_unknown_during_deserialization=True)
class Citation:
    """
    Details a specific attribution of data within the BOM to a contributing entity or process.

    Exactly one of `pointers` or `expressions` must be provided.
    At least one of `attributed_to` or `process` must be provided.

    .. note::
        Introduced in CycloneDX v1.7

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.7/xml/#type_citationType
    """

    def __init__(
        self, *,
        timestamp: datetime,
        bom_ref: Optional[Union[str, BomRef]] = None,
        pointers: Optional[Iterable[str]] = None,
        expressions: Optional[Iterable[str]] = None,
        attributed_to: Optional[Union[str, BomRef]] = None,
        process: Optional[Union[str, BomRef]] = None,
        note: Optional[str] = None,
        # TODO: signature
    ) -> None:
        pointers = SortedSet(pointers or ())
        expressions = SortedSet(expressions or ())
        if not pointers and not expressions:
            raise NoPropertiesProvidedException(
                'One of `pointers` or `expressions` must be supplied - neither supplied'
            )
        if pointers and expressions:
            raise MutuallyExclusivePropertiesException(
                'Only one of `pointers` or `expressions` must be supplied - both supplied'
            )
        if attributed_to is None and process is None:
            raise NoPropertiesProvidedException(
                'At least one of `attributed_to` or `process` must be supplied - neither supplied'
            )
        self._bom_ref = _bom_ref_from_str(bom_ref)
        self.pointers = pointers
        self.expressions = expressions
        self.timestamp = timestamp
        self.attributed_to = attributed_to
        self.process = process
        self.note = note
        # TODO: signature

    @property
    @serializable.type_mapping(BomRef)
    @serializable.json_name('bom-ref')
    @serializable.xml_name('bom-ref')
    @serializable.xml_attribute()
    def bom_ref(self) -> BomRef:
        """
        An optional identifier which can be used to reference the citation elsewhere in the BOM.
        Every bom-ref MUST be unique within the BOM.

        Returns:
            `BomRef`
        """
        return self._bom_ref

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'pointer')
    @serializable.xml_sequence(1)
    def pointers(self) -> 'SortedSet[str]':
        """
        One or more JSON Pointers (RFC 6901) identifying the BOM fields to which the attribution applies.
        Users of other serialization formats (e.g. XML) shall use the JSON Pointer format as well.

        Returns:
            Set of `str`
        """
        return self._pointers

    @pointers.setter
    def pointers(self, pointers: Iterable[str]) -> None:
        self._pointers = SortedSet(pointers)

    @property
    @serializable.xml_array(serializable.XmlArraySerializationType.NESTED, 'expression')
    @serializable.xml_sequence(2)
    def expressions(self) -> 'SortedSet[str]':
        """
        One or more path expressions used to locate values within a BOM.
        Use JSONPath for JSON and XPath for XML.

        Returns:
            Set of `str`
        """
        return self._expressions

    @expressions.setter
    def expressions(self, expressions: Iterable[str]) -> None:
        self._expressions = SortedSet(expressions)

    @property
    @serializable.type_mapping(serializable.helpers.XsdDateTime)
    @serializable.xml_sequence(3)
    def timestamp(self) -> datetime:
        """
        The date and time when the attribution was made or the information was supplied.

        Returns:
            `datetime`
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: datetime) -> None:
        self._timestamp = timestamp

    @property
    @serializable.type_mapping(BomRef)
    @serializable.json_name('attributedTo')
    @serializable.xml_name('attributedTo')
    @serializable.xml_sequence(4)
    def attributed_to(self) -> Optional[BomRef]:
        """
        The `bom-ref` of an object, such as a component, service, tool, organisational entity, or person
        that supplied the cited information.

        Returns:
            `BomRef` if set else `None`
        """
        return self._attributed_to

    @attributed_to.setter
    def attributed_to(self, attributed_to: Optional[Union[str, BomRef]]) -> None:
        self._attributed_to = _bom_ref_from_str(attributed_to, optional=True)

    @property
    @serializable.type_mapping(BomRef)
    @serializable.xml_sequence(5)
    def process(self) -> Optional[BomRef]:
        """
        The `bom-ref` to a process (such as a formula, workflow, task, or step) defined in the `formulation`
        section that executed or generated the attributed data.

        Returns:
            `BomRef` if set else `None`
        """
        return self._process

    @process.setter
    def process(self, process: Optional[Union[str, BomRef]]) -> None:
        self._process = _bom_ref_from_str(process, optional=True)

    @property
    @serializable.xml_sequence(6)
    def note(self) -> Optional[str]:
        """
        A description or comment about the context or quality of the data attribution.

        Returns:
            `str` if set else `None`
        """
        return self._note

    @note.setter
    def note(self, note: Optional[str]) -> None:
        self._note = note

    # @property
    # # MUST NOT RENDER FOR XML -- this is JSON only
    # def signature(self) -> ...:
    #     ...
    #
    # @signature.setter
    # def signature(self, signature: ...) -> None:
    #     ...

    def __comparable_tuple(self) -> _ComparableTuple:
        return _ComparableTuple((
            self.timestamp,
            _ComparableTuple(self.pointers), _ComparableTuple(self.expressions),
            self.attributed_to, self.process,
            self.bom_ref.value, self.note,
        ))

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Citation):
            return self.__comparable_tuple() < other.__comparable_tuple()
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Citation):
            return self.__comparable_tuple() == other.__comparable_tuple()
        return False

    def __hash__(self) -> int:
        return hash(self.__comparable_tuple())

    def __repr__(self) -> str:
        return f'<Citation bom-ref={self.bom_ref!r}, timestamp={self.timestamp!r}, ' \
            f'attributed_to={self.attributed_to!r}, process={self.process!r}>'
