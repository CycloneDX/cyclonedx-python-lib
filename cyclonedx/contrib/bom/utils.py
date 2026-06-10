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
from itertools import chain
from typing import TYPE_CHECKING, Any

from ...model.dependency import Dependency

if TYPE_CHECKING:  # pragma: no cover
    from ...model.bom import Bom, BomRef


class BomDependencyGraphFlatMerger:

    def __init__(self, bom: 'Bom') -> None:
        self._bom = bom
        # do NOT use the getter - see `reset()` for reasons
        self._deps = self._bom._dependencies

    def __enter__(self) -> None:
        self.flatten_merge()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.reset()

    def reset(self) -> None:
        # Do NOT use the setter - this would create overhead and most importantly,
        # and this could cause deduplication of an existing malformed set.
        # Just access the internal field directly!
        self._bom._dependencies = self._deps

    def flatten_merge(self) -> None:
        self._bom.dependencies = self._merge_deps(chain.from_iterable(
            self._flatten_dep(dep) for dep in self._deps
        ))

    @staticmethod
    def _merge_deps(deps: Iterable[Dependency]) -> Iterable[Dependency]:
        merged: dict[BomRef, Dependency] = {}
        for dep in deps:
            if m := merged.get(dep.ref):
                m.dependencies.update(dep.dependencies)
            else:
                merged[dep.ref] = Dependency(dep.ref, dep.dependencies)
        return merged.values()

    @staticmethod
    def _flatten_dep(dep: Dependency) -> Iterable[Dependency]:
        if not dep.dependencies:
            return dep,
        flat: list[Dependency] = []
        todos: list[Dependency] = [dep]
        while todos:
            todo = todos.pop()
            if todo.dependencies:
                flat.append(Dependency(todo.ref, (Dependency(d.ref) for d in todo.dependencies)))
                todos.extend(todo.dependencies)
        return flat
