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

from . import SchemaVersion


class BaseSchemaVersion(ABC):

    @property
    @abstractmethod
    def schema_version_enum(self) -> SchemaVersion:
        pass

    def bom_supports_metadata(self) -> bool:
        return True

    def bom_metadata_supports_tools(self) -> bool:
        return True

    def bom_metadata_supports_tools_external_references(self) -> bool:
        return True

    def bom_metadata_supports_licenses(self) -> bool:
        return True

    def bom_metadata_supports_properties(self) -> bool:
        return True

    def bom_supports_services(self) -> bool:
        return True

    def bom_supports_external_references(self) -> bool:
        return True

    def services_supports_properties(self) -> bool:
        return True

    def services_supports_release_notes(self) -> bool:
        return True

    def bom_supports_vulnerabilities(self) -> bool:
        return True

    def bom_supports_vulnerabilities_via_extension(self) -> bool:
        return False

    def bom_requires_modified(self) -> bool:
        return False

    def component_supports_author(self) -> bool:
        return True

    def component_supports_bom_ref_attribute(self) -> bool:
        return True

    def component_supports_mime_type_attribute(self) -> bool:
        return True

    def license_supports_expression(self) -> bool:
        return True

    def component_version_optional(self) -> bool:
        return False

    def component_supports_swid(self) -> bool:
        return True

    def component_supports_pedigree(self) -> bool:
        return True

    def pedigree_supports_patches(self) -> bool:
        return True

    def component_supports_external_references(self) -> bool:
        return True

    def component_supports_release_notes(self) -> bool:
        return True

    def external_references_supports_hashes(self) -> bool:
        return True

    @abstractmethod
    def get_schema_version(self) -> str:
        raise NotImplementedError


class SchemaVersion1Dot4(BaseSchemaVersion):

    @property
    def schema_version_enum(self) -> SchemaVersion:
        return SchemaVersion.V1_4

    def get_schema_version(self) -> str:
        return '1.4'

    def component_version_optional(self) -> bool:
        return True


class SchemaVersion1Dot3(BaseSchemaVersion):

    @property
    def schema_version_enum(self) -> SchemaVersion:
        return SchemaVersion.V1_3

    def bom_metadata_supports_tools_external_references(self) -> bool:
        return False

    def services_supports_release_notes(self) -> bool:
        return False

    def bom_supports_vulnerabilities(self) -> bool:
        return False

    def bom_supports_vulnerabilities_via_extension(self) -> bool:
        return True

    def component_supports_mime_type_attribute(self) -> bool:
        return False

    def component_supports_release_notes(self) -> bool:
        return False

    def get_schema_version(self) -> str:
        return '1.3'


class SchemaVersion1Dot2(BaseSchemaVersion):

    @property
    def schema_version_enum(self) -> SchemaVersion:
        return SchemaVersion.V1_2

    def bom_metadata_supports_tools_external_references(self) -> bool:
        return False

    def bom_metadata_supports_licenses(self) -> bool:
        return False

    def bom_metadata_supports_properties(self) -> bool:
        return False

    def services_supports_properties(self) -> bool:
        return False

    def services_supports_release_notes(self) -> bool:
        return False

    def bom_supports_vulnerabilities(self) -> bool:
        return False

    def bom_supports_vulnerabilities_via_extension(self) -> bool:
        return True

    def component_supports_mime_type_attribute(self) -> bool:
        return False

    def component_supports_release_notes(self) -> bool:
        return False

    def external_references_supports_hashes(self) -> bool:
        return False

    def get_schema_version(self) -> str:
        return '1.2'


class SchemaVersion1Dot1(BaseSchemaVersion):

    @property
    def schema_version_enum(self) -> SchemaVersion:
        return SchemaVersion.V1_1

    def bom_metadata_supports_tools(self) -> bool:
        return False

    def bom_metadata_supports_tools_external_references(self) -> bool:
        return False

    def bom_supports_services(self) -> bool:
        return False

    def services_supports_properties(self) -> bool:
        return False

    def pedigree_supports_patches(self) -> bool:
        return False

    def services_supports_release_notes(self) -> bool:
        return False

    def bom_supports_vulnerabilities(self) -> bool:
        return False

    def bom_supports_vulnerabilities_via_extension(self) -> bool:
        return True

    def bom_supports_metadata(self) -> bool:
        return False

    def component_supports_mime_type_attribute(self) -> bool:
        return False

    def component_supports_author(self) -> bool:
        return False

    def component_supports_swid(self) -> bool:
        return False

    def component_supports_release_notes(self) -> bool:
        return False

    def external_references_supports_hashes(self) -> bool:
        return False

    def get_schema_version(self) -> str:
        return '1.1'


class SchemaVersion1Dot0(BaseSchemaVersion):

    @property
    def schema_version_enum(self) -> SchemaVersion:
        return SchemaVersion.V1_0

    def bom_metadata_supports_tools(self) -> bool:
        return False

    def bom_metadata_supports_tools_external_references(self) -> bool:
        return False

    def bom_supports_services(self) -> bool:
        return False

    def bom_supports_external_references(self) -> bool:
        return False

    def services_supports_properties(self) -> bool:
        return False

    def services_supports_release_notes(self) -> bool:
        return False

    def bom_supports_vulnerabilities(self) -> bool:
        return False

    def bom_supports_metadata(self) -> bool:
        return False

    def bom_requires_modified(self) -> bool:
        return True

    def component_supports_author(self) -> bool:
        return False

    def component_supports_bom_ref_attribute(self) -> bool:
        return False

    def license_supports_expression(self) -> bool:
        return False

    def component_supports_mime_type_attribute(self) -> bool:
        return False

    def component_supports_swid(self) -> bool:
        return False

    def component_supports_pedigree(self) -> bool:
        return False

    def component_supports_external_references(self) -> bool:
        return False

    def component_supports_release_notes(self) -> bool:
        return False

    def external_references_supports_hashes(self) -> bool:
        return False

    def get_schema_version(self) -> str:
        return '1.0'
