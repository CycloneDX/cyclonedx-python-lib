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

from abc import ABC, abstractmethod


class BaseSchemaVersion(ABC):

    def bom_metadata_supports_tools(self) -> bool:
        return True

    def bom_supports_metadata(self) -> bool:
        return True

    def component_supports_author(self) -> bool:
        return True

    def component_supports_bom_ref(self) -> bool:
        return True

    def component_supports_external_references(self) -> bool:
        return True

    @abstractmethod
    def get_schema_version(self) -> str:
        raise NotImplementedError


class SchemaVersion1Dot3(BaseSchemaVersion):

    def get_schema_version(self) -> str:
        return '1.3'


class SchemaVersion1Dot2(BaseSchemaVersion):

    def get_schema_version(self) -> str:
        return '1.2'


class SchemaVersion1Dot1(BaseSchemaVersion):

    def bom_metadata_supports_tools(self) -> bool:
        return False

    def bom_supports_metadata(self) -> bool:
        return False

    def component_supports_author(self) -> bool:
        return False

    def get_schema_version(self) -> str:
        return '1.1'


class SchemaVersion1Dot0(BaseSchemaVersion):

    def bom_metadata_supports_tools(self) -> bool:
        return False

    def bom_supports_metadata(self) -> bool:
        return False

    def component_supports_author(self) -> bool:
        return False

    def component_supports_bom_ref(self) -> bool:
        return False

    def component_supports_external_references(self) -> bool:
        return False

    def get_schema_version(self) -> str:
        return '1.0'
