# encoding: utf-8

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

from abc import ABC, abstractmethod
from typing import Any, Iterable, Optional, Set

import serializable
from sortedcontainers import SortedSet

from cyclonedx.serialization import BomRefHelper

from .bom_ref import BomRef


@serializable.serializable_class
class Dependency:
    """
    Models a Dependency within a BOM.

    .. note::
        See https://cyclonedx.org/docs/1.4/xml/#type_dependencyType
    """

    def __init__(self, ref: BomRef, dependencies: Optional[Iterable["Dependency"]] = None) -> None:
        self.ref = ref
        self.dependencies = dependencies or []  # type: ignore

    @property  # type: ignore[misc]
    @serializable.type_mapping(BomRefHelper)
    @serializable.xml_attribute()
    def ref(self) -> BomRef:
        return self._ref

    @ref.setter
    def ref(self, ref: BomRef) -> None:
        self._ref = ref

    @property  # type: ignore[misc]
    @serializable.json_name('dependsOn')
    @serializable.xml_array(serializable.XmlArraySerializationType.FLAT, 'dependency')
    def dependencies(self) -> "SortedSet[Dependency]":
        return self._dependencies

    @dependencies.setter
    def dependencies(self, dependencies: Iterable["Dependency"]) -> None:
        self._dependencies = SortedSet(dependencies)

    def dependencies_as_bom_refs(self) -> Set[BomRef]:
        return set(map(lambda d: d.ref, self.dependencies))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Dependency):
            return hash(other) == hash(self)
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Dependency):
            return hash(self) < hash(other)
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.ref, tuple(self.dependencies)))

    def __repr__(self) -> str:
        return f'<Dependency ref={self.ref}, targets={len(self.dependencies)}>'


class Dependable(ABC):
    """
    Dependable objects can be part of the Dependency Graph
    """

    @property
    @abstractmethod
    def bom_ref(self) -> BomRef:
        pass
