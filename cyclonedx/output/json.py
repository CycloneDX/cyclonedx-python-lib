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

from abc import abstractmethod
from itertools import chain
from json import dumps as json_dumps, loads as json_loads
from typing import TYPE_CHECKING, Any, Iterable, Literal, Optional, Union

from ..exception.output import FormatNotSupportedException
from ..model.dependency import Dependency
from ..schema import OutputFormat, SchemaVersion
from ..schema.schema import (
    SCHEMA_VERSIONS,
    BaseSchemaVersion,
    SchemaVersion1Dot0,
    SchemaVersion1Dot1,
    SchemaVersion1Dot2,
    SchemaVersion1Dot3,
    SchemaVersion1Dot4,
    SchemaVersion1Dot5,
    SchemaVersion1Dot6,
    SchemaVersion1Dot7,
)
from . import BaseOutput, BomRefDiscriminator

if TYPE_CHECKING:  # pragma: no cover
    from ..model.bom import Bom


class _BomDependencyGraphFlattener:
    """
    !!! THIS CLASS IS INTERNAL.
    Everything might change without any notice.
    """

    def __init__(self, bom: 'Bom'):
        self._bom = bom
        # do NOT use the getter - see `reset()` for reasons
        self._deps = self._bom._dependencies

    def __enter__(self) -> None:
        self.flatten()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.reset()

    def reset(self) -> None:
        # Do NOT use the setter - this would create overhead and most importantly,
        # and this could cause deduplication of an existing malformed set.
        # Just access the internal field directly!
        self._bom._dependencies = self._deps

    def flatten(self) -> None:
        self._bom.dependencies = chain.from_iterable(
            self.__flatten_dep(dep) for dep in self._deps
        )

    @staticmethod
    def __flatten_dep(dep: Dependency) -> Iterable[Dependency]:
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


class Json(BaseOutput, BaseSchemaVersion):

    def __init__(self, bom: 'Bom') -> None:
        super().__init__(bom=bom)
        self._bom_json: dict[str, Any] = dict()

    @property
    def schema_version(self) -> SchemaVersion:
        return self.schema_version_enum

    @property
    def output_format(self) -> Literal[OutputFormat.JSON]:
        return OutputFormat.JSON

    def generate(self, force_regeneration: bool = False) -> None:
        if self.generated and not force_regeneration:
            return

        schema_uri: Optional[str] = self._get_schema_uri()
        if not schema_uri:
            raise FormatNotSupportedException(
                f'JSON is not supported by CycloneDX in schema version {self.schema_version.to_version()}')

        _json_core = {
            '$schema': schema_uri,
            'bomFormat': 'CycloneDX',
            'specVersion': self.schema_version.to_version()
        }
        _view = SCHEMA_VERSIONS.get(self.schema_version_enum)
        bom = self.get_bom()
        bom.validate()
        # utilize contrib.dependency.flatten() somewhere here
        with BomRefDiscriminator.from_bom(bom):
            with _BomDependencyGraphFlattener(bom):
                bom_json: dict[str, Any] = json_loads(
                    bom.as_json(  # type:ignore[attr-defined]
                        view_=_view))
        bom_json.update(_json_core)
        self._bom_json = bom_json
        self.generated = True

    def output_as_string(self, *,
                         indent: Optional[Union[int, str]] = None,
                         **kwargs: Any) -> str:
        self.generate()
        return json_dumps(self._bom_json,
                          indent=indent)

    @abstractmethod
    def _get_schema_uri(self) -> Optional[str]:
        ...  # pragma: no cover


class JsonV1Dot0(Json, SchemaVersion1Dot0):

    def _get_schema_uri(self) -> None:
        return None


class JsonV1Dot1(Json, SchemaVersion1Dot1):

    def _get_schema_uri(self) -> None:
        return None


class JsonV1Dot2(Json, SchemaVersion1Dot2):

    def _get_schema_uri(self) -> str:
        return 'http://cyclonedx.org/schema/bom-1.2b.schema.json'


class JsonV1Dot3(Json, SchemaVersion1Dot3):

    def _get_schema_uri(self) -> str:
        return 'http://cyclonedx.org/schema/bom-1.3a.schema.json'


class JsonV1Dot4(Json, SchemaVersion1Dot4):

    def _get_schema_uri(self) -> str:
        return 'http://cyclonedx.org/schema/bom-1.4.schema.json'


class JsonV1Dot5(Json, SchemaVersion1Dot5):

    def _get_schema_uri(self) -> str:
        return 'http://cyclonedx.org/schema/bom-1.5.schema.json'


class JsonV1Dot6(Json, SchemaVersion1Dot6):

    def _get_schema_uri(self) -> str:
        return 'http://cyclonedx.org/schema/bom-1.6.schema.json'


class JsonV1Dot7(Json, SchemaVersion1Dot7):

    def _get_schema_uri(self) -> str:
        return 'http://cyclonedx.org/schema/bom-1.7.schema.json'


BY_SCHEMA_VERSION: dict[SchemaVersion, type[Json]] = {
    SchemaVersion.V1_7: JsonV1Dot7,
    SchemaVersion.V1_6: JsonV1Dot6,
    SchemaVersion.V1_5: JsonV1Dot5,
    SchemaVersion.V1_4: JsonV1Dot4,
    SchemaVersion.V1_3: JsonV1Dot3,
    SchemaVersion.V1_2: JsonV1Dot2,
    SchemaVersion.V1_1: JsonV1Dot1,
    SchemaVersion.V1_0: JsonV1Dot0,
}
