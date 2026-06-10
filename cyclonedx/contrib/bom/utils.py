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

__all__ = ['BomDependencyGraphFlatMerger']

from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

from ...model.dependency import Dependency

if TYPE_CHECKING:  # pragma: no cover
    from ...model.bom import Bom
    from ...model.bom_ref import BomRef


class BomDependencyGraphFlatMerger:
    """

    """

    def __init__(self, bom: 'Bom') -> None:
        self._bom = bom
        # do NOT use the getter - see `reset()` for reasons
        self._deps = self._bom._dependencies

    def __enter__(self) -> None:
        self.flatten_merge()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.reset()

    def flatten_merge(self) -> None:
        """
        Flatten and merge all of Bom's dependencies.
        """
        self._bom.dependencies = self._flatten_merge(self._deps)

    def reset(self) -> None:
        """
        Reset Bom's dependencies to the initial state.
        """
        # Do NOT use the setter - this would create overhead,
        # and - most importantly - this could cause deduplication of an existing malformed set.
        # Just access the internal field directly!
        self._bom._dependencies = self._deps

    @staticmethod
    def _flatten_merge(deps: Iterable[Dependency]) -> Iterable[Dependency]:
        flat: dict[BomRef, list[BomRef]] = {}
        todos = list(deps)
        seen: list[int] = []
        while todos:
            todo = todos.pop()
            if (todo_id := id(todo)) in seen:
                pass  # continue
            seen.append(todo_id)
            ds = flat.setdefault(todo.ref, [])
            if todo_deps := todo.dependencies:
                ds.extend(d.ref for d in todo_deps)
                todos.extend(todo_deps)
        return (
            Dependency(br, (Dependency(d) for d in ds))
            for br, ds
            in flat.items()
        )
