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
from typing import Dict, Literal, Type

from serializable import ViewType

from ..schema import SchemaVersion


class BaseSchemaVersion(ABC, ViewType):

    @property
    @abstractmethod
    def schema_version_enum(self) -> SchemaVersion:
        ...

    def get_schema_version(self) -> str:
        return self.schema_version_enum.to_version()


class SchemaVersion1Dot4(BaseSchemaVersion):

    @property
    def schema_version_enum(self) -> Literal[SchemaVersion.V1_4]:
        return SchemaVersion.V1_4


class SchemaVersion1Dot3(BaseSchemaVersion):

    @property
    def schema_version_enum(self) -> Literal[SchemaVersion.V1_3]:
        return SchemaVersion.V1_3


class SchemaVersion1Dot2(BaseSchemaVersion):

    @property
    def schema_version_enum(self) -> Literal[SchemaVersion.V1_2]:
        return SchemaVersion.V1_2


class SchemaVersion1Dot1(BaseSchemaVersion):

    @property
    def schema_version_enum(self) -> Literal[SchemaVersion.V1_1]:
        return SchemaVersion.V1_1


class SchemaVersion1Dot0(BaseSchemaVersion):

    @property
    def schema_version_enum(self) -> Literal[SchemaVersion.V1_0]:
        return SchemaVersion.V1_0


SCHEMA_VERSIONS: Dict[SchemaVersion, Type[BaseSchemaVersion]] = {
    SchemaVersion.V1_4: SchemaVersion1Dot4,
    SchemaVersion.V1_3: SchemaVersion1Dot3,
    SchemaVersion.V1_2: SchemaVersion1Dot2,
    SchemaVersion.V1_1: SchemaVersion1Dot1,
    SchemaVersion.V1_0: SchemaVersion1Dot0,
}
