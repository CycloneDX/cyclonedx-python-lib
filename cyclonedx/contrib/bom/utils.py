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

"""Bom related utilities"""

__all__ = ['BomRefDiscriminator']

from collections.abc import Iterable
from itertools import chain
from random import random
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover
    from ...model.bom import Bom
    from ...model.bom_ref import BomRef


class BomRefDiscriminator:
    """
    Utility to give BomRefs unique values.
    """

    def __init__(self, bomrefs: Iterable['BomRef'], prefix: str = 'BomRef') -> None:
        # do not use dict/set here, different BomRefs with same value have same hash and would shadow each other
        self._bomrefs = tuple((bomref, bomref.value) for bomref in bomrefs)
        self._prefix = prefix

    def __enter__(self) -> None:
        self.discriminate()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.reset()

    def discriminate(self) -> None:
        """
        Check BomRefs' values for uniqueness.
        Duplications will be assigned a unique value.
        """
        known_values = []
        for bomref, _ in self._bomrefs:
            value = bomref.value
            if value is None or value in known_values:
                value = self._make_unique()
                bomref.value = value
            known_values.append(value)

    def reset(self) -> None:
        """
        Set BomRefs' values to the initial state.
        """
        for bomref, original_value in self._bomrefs:
            bomref.value = original_value

    def _make_unique(self) -> str:
        return f'{self._prefix}{str(random())[1:]}{str(random())[1:]}'  # nosec B311

    @classmethod
    def from_bom(cls, bom: 'Bom', prefix: str = 'BomRef') -> 'BomRefDiscriminator':
        return cls(chain(
            map(lambda c: c.bom_ref, bom._get_all_components()),
            map(lambda s: s.bom_ref, bom.services),
            map(lambda v: v.bom_ref, bom.vulnerabilities)
        ), prefix)
