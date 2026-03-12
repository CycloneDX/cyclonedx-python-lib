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
from typing import Literal

from . import SchemaVersion


class SchemaDeprecationWarning(DeprecationWarning, ABC):
    @property
    @abstractmethod
    def schema_version_enum(self) -> SchemaVersion:
        ...  # pragma: no cover

    def get_schema_version(self) -> str:
        return self.schema_version_enum.to_version()


class DeprecationWarning1Dot7(SchemaDeprecationWarning):
    @property
    def schema_version_enum(self) -> Literal[SchemaVersion.V1_7]:
        return SchemaVersion.V1_7


class DeprecationWarning1Dot6(SchemaDeprecationWarning):
    @property
    def schema_version_enum(self) -> Literal[SchemaVersion.V1_6]:
        return SchemaVersion.V1_6


class DeprecationWarning1Dot5(SchemaDeprecationWarning):
    @property
    def schema_version_enum(self) -> Literal[SchemaVersion.V1_5]:
        return SchemaVersion.V1_5


class DeprecationWarning1Dot4(SchemaDeprecationWarning):
    @property
    def schema_version_enum(self) -> Literal[SchemaVersion.V1_4]:
        return SchemaVersion.V1_4


class DeprecationWarning1Dot3(SchemaDeprecationWarning):
    @property
    def schema_version_enum(self) -> Literal[SchemaVersion.V1_3]:
        return SchemaVersion.V1_3


class DeprecationWarning1Dot2(SchemaDeprecationWarning):
    @property
    def schema_version_enum(self) -> Literal[SchemaVersion.V1_2]:
        return SchemaVersion.V1_2


class DeprecationWarning1Dot1(SchemaDeprecationWarning):
    @property
    def schema_version_enum(self) -> Literal[SchemaVersion.V1_1]:
        return SchemaVersion.V1_1
