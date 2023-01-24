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

import json
from abc import abstractmethod
from typing import Optional

from ..exception.output import FormatNotSupportedException
from ..model.bom import Bom
from ..schema import SchemaVersion
from ..schema.schema import (
    SCHEMA_VERSIONS,
    BaseSchemaVersion,
    SchemaVersion1Dot0,
    SchemaVersion1Dot1,
    SchemaVersion1Dot2,
    SchemaVersion1Dot3,
    SchemaVersion1Dot4,
)
from . import BaseOutput


class Json(BaseOutput, BaseSchemaVersion):

    def __init__(self, bom: Bom) -> None:
        super().__init__(bom=bom)
        self._json_output: str = ''

    @property
    def schema_version(self) -> SchemaVersion:
        return self.schema_version_enum

    def generate(self, force_regeneration: bool = False) -> None:
        # New Way
        schema_uri: Optional[str] = self._get_schema_uri()
        if not schema_uri:
            raise FormatNotSupportedException(
                f'JSON is not supported by CycloneDX in schema version {self.schema_version.to_version()}')

        _json_core = {
            '$schema': schema_uri,
            'bomFormat': 'CycloneDX',
            'specVersion': self.schema_version.to_version()
        }
        _view = SCHEMA_VERSIONS.get(self.get_schema_version())
        if self.generated and force_regeneration:
            self.get_bom().validate()
            bom_json = json.loads(self.get_bom().as_json(view_=_view))  # type: ignore
            bom_json.update(_json_core)
            self._json_output = json.dumps(bom_json)
            self.generated = True
            return
        elif self.generated:
            return
        else:
            self.get_bom().validate()
            bom_json = json.loads(self.get_bom().as_json(view_=_view))  # type: ignore
            bom_json.update(_json_core)
            self._json_output = json.dumps(bom_json)
            self.generated = True
            return

    def output_as_string(self) -> str:
        self.generate()
        return self._json_output

    @abstractmethod
    def _get_schema_uri(self) -> Optional[str]:
        pass


class JsonV1Dot0(Json, SchemaVersion1Dot0):

    def _get_schema_uri(self) -> Optional[str]:
        return None


class JsonV1Dot1(Json, SchemaVersion1Dot1):

    def _get_schema_uri(self) -> Optional[str]:
        return None


class JsonV1Dot2(Json, SchemaVersion1Dot2):

    def _get_schema_uri(self) -> Optional[str]:
        return 'http://cyclonedx.org/schema/bom-1.2b.schema.json'


class JsonV1Dot3(Json, SchemaVersion1Dot3):

    def _get_schema_uri(self) -> Optional[str]:
        return 'http://cyclonedx.org/schema/bom-1.3a.schema.json'


class JsonV1Dot4(Json, SchemaVersion1Dot4):

    def _get_schema_uri(self) -> Optional[str]:
        return 'http://cyclonedx.org/schema/bom-1.4.schema.json'
