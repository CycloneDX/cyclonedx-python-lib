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
Graphics types of the CycloneDX standard, shared by model cards and component data.

.. note::
    See the CycloneDX Schema for graphics:\n
    - XML: https://cyclonedx.org/docs/1.7/xml/#type_graphicsCollection\n
    - JSON: https://cyclonedx.org/docs/1.7/json/#components_items_modelCard_quantitativeAnalysis_graphics
"""

from collections.abc import Iterable
from typing import Any, Optional

import py_serializable as serializable
from sortedcontainers import SortedSet

from .._internal.compare import ComparableTuple as _ComparableTuple
from ..schema.schema import SchemaVersion1Dot5, SchemaVersion1Dot6, SchemaVersion1Dot7
from . import AttachedText


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
    def name(self) -> Optional[str]:
        """
        The name of the graphic.

        Returns:
            `str` if set else `None`
        """
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
        """
        The graphic (vector or raster). Base64 encoding must be specified for binary images.

        Returns:
            `AttachedText` if set else `None`
        """
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
    def description(self) -> Optional[str]:
        """
        A description of this collection of graphics.

        Returns:
            `str` if set else `None`
        """
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
        """
        A collection of graphics.

        Returns:
            Set of `Graphic`
        """
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
