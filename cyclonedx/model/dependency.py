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


from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any, Optional

import attrs
from sortedcontainers import SortedSet

from ..serialization import METADATA_KEY_JSON_NAME, METADATA_KEY_XML_ATTR
from .bom_ref import BomRef


def _sortedset_factory() -> SortedSet:
    return SortedSet()


def _sortedset_converter(value: Any) -> SortedSet:
    if value is None:
        return SortedSet()
    if isinstance(value, SortedSet):
        return value
    return SortedSet(value)


@attrs.define
class Dependency:
    """
    Models a Dependency within a BOM.

    .. note::
        See https://cyclonedx.org/docs/1.7/xml/#type_dependencyType
    """
    ref: BomRef = attrs.field(
        metadata={METADATA_KEY_XML_ATTR: True}
    )
    dependencies: 'SortedSet[Dependency]' = attrs.field(
        factory=_sortedset_factory,
        converter=_sortedset_converter,
        metadata={METADATA_KEY_JSON_NAME: 'dependsOn'}
    )

    def dependencies_as_bom_refs(self) -> set[BomRef]:
        return set(map(lambda d: d.ref, self.dependencies))

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Dependency):
            return (self.ref, tuple(self.dependencies)) < (other.ref, tuple(other.dependencies))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.ref, tuple(self.dependencies)))

    def __repr__(self) -> str:
        return f'<Dependency ref={self.ref!r}, targets={len(self.dependencies)}>'


class Dependable(ABC):
    """
    Dependable objects can be part of the Dependency Graph
    """

    @property
    @abstractmethod
    def bom_ref(self) -> BomRef:
        ...  # pragma: no cover
