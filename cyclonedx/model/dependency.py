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

from typing import Iterable, Optional

from sortedcontainers import SortedSet

from .bom_ref import BomRef


class Dependency:
    """
    This is our internal representation of a Dependency for a Component.

    .. note::
        See the CycloneDX Schema definition: https://cyclonedx.org/docs/1.4/xml/#type_dependencyType
    """

    def __init__(self, *, ref: BomRef, depends_on: Optional[Iterable[BomRef]] = None) -> None:
        self._ref = ref
        self.depends_on = SortedSet(depends_on or [])

    @property
    def ref(self) -> BomRef:
        return self._ref

    @property
    def depends_on(self) -> "SortedSet[BomRef]":
        return self._depends_on

    @depends_on.setter
    def depends_on(self, depends_on: Iterable[BomRef]) -> None:
        self._depends_on = SortedSet(depends_on)
