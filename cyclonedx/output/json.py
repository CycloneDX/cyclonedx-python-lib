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

from abc import abstractmethod
from json import dumps as json_dumps, loads as json_loads
from typing import TYPE_CHECKING, Any, Dict, Literal, Optional, Type, Union

from ..exception.output import FormatNotSupportedException
from ..schema import OutputFormat, SchemaVersion
from ..schema.schema import (
    SCHEMA_VERSIONS,
    BaseSchemaVersion,
    SchemaVersion1Dot0,
    SchemaVersion1Dot1,
    SchemaVersion1Dot2,
    SchemaVersion1Dot3,
    SchemaVersion1Dot4,
)
from . import BaseOutput, BomRefDiscriminator

if TYPE_CHECKING:  # pragma: no cover
    from ..model.bom import Bom


class Json(BaseOutput, BaseSchemaVersion):

    def __init__(self, bom: 'Bom') -> None:
        super().__init__(bom=bom)
        self._bom_json: Dict[str, Any] = dict()

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
        with BomRefDiscriminator.from_bom(bom):
            bom_json: Dict[str, Any] = json_loads(
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
        pass


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


BY_SCHEMA_VERSION: Dict[SchemaVersion, Type[Json]] = {
    SchemaVersion.V1_4: JsonV1Dot4,
    SchemaVersion.V1_3: JsonV1Dot3,
    SchemaVersion.V1_2: JsonV1Dot2,
    SchemaVersion.V1_1: JsonV1Dot1,
    SchemaVersion.V1_0: JsonV1Dot0,
}
