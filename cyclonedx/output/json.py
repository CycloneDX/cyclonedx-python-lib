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
from typing import Any, Dict, Iterable, List, Optional, Union

from ..exception.output import FormatNotSupportedException
from ..model.bom import Bom
from ..model.component import Component
from . import BaseOutput, SchemaVersion
from .schema import (
    BaseSchemaVersion,
    SchemaVersion1Dot0,
    SchemaVersion1Dot1,
    SchemaVersion1Dot2,
    SchemaVersion1Dot3,
    SchemaVersion1Dot4,
)
from .serializer.json import CycloneDxJSONEncoder

ComponentDict = Dict[str, Union[
    str,
    List[Dict[str, str]],
    List[Dict[str, Dict[str, str]]],
    List[Dict[str, Union[str, List[Dict[str, str]]]]]]]


class Json(BaseOutput, BaseSchemaVersion):

    def __init__(self, bom: Bom) -> None:
        super().__init__(bom=bom)
        self._json_output: str = ''

    @property
    def schema_version(self) -> SchemaVersion:
        return self.schema_version_enum

    def generate(self, force_regeneration: bool = False) -> None:
        if self.generated and not force_regeneration:
            return

        bom = self.get_bom()
        bom.validate()

        schema_uri: Optional[str] = self._get_schema_uri()
        if not schema_uri:
            raise FormatNotSupportedException(
                f'JSON is not supported by CycloneDX in schema version {self.schema_version.to_version()}')

        extras = {}
        if self.bom_supports_dependencies():
            dep_components: Iterable[Component] = bom.components
            if bom.metadata.component:
                dep_components = [bom.metadata.component, *dep_components]
            dependencies = []
            for component in dep_components:
                dependencies.append({
                    'ref': str(component.bom_ref),
                    'dependsOn': [*map(str, component.dependencies)]
                })
            if dependencies:
                extras["dependencies"] = dependencies
            del dep_components

        if self.bom_supports_vulnerabilities():
            vulnerabilities: List[Dict[Any, Any]] = []
            if bom.components:
                for component in bom.components:
                    for vulnerability in component.get_vulnerabilities():
                        vulnerabilities.append(
                            json.loads(json.dumps(vulnerability, cls=CycloneDxJSONEncoder))
                        )
            if vulnerabilities:
                extras["vulnerabilities"] = vulnerabilities

        bom_json = json.loads(json.dumps(bom, cls=CycloneDxJSONEncoder))
        bom_json = json.loads(self._specialise_output_for_schema_version(bom_json=bom_json))
        self._json_output = json.dumps({**self._create_bom_element(), **bom_json, **extras})

        self.generated = True

    def _specialise_output_for_schema_version(self, bom_json: Dict[Any, Any]) -> str:
        if not self.bom_supports_metadata():
            if 'metadata' in bom_json.keys():
                del bom_json['metadata']

        if not self.bom_metadata_supports_tools():
            del bom_json['metadata']['tools']
        elif not self.bom_metadata_supports_tools_external_references():
            for i in range(len(bom_json['metadata']['tools'])):
                if 'externalReferences' in bom_json['metadata']['tools'][i].keys():
                    del bom_json['metadata']['tools'][i]['externalReferences']

        if not self.bom_metadata_supports_licenses() and 'licenses' in bom_json['metadata'].keys():
            del bom_json['metadata']['licenses']

        if not self.bom_metadata_supports_properties() and 'properties' in bom_json['metadata'].keys():
            del bom_json['metadata']['properties']

        # Iterate Components
        bom_json = self._recurse_specialise_component(bom_json=bom_json)

        # Iterate Services
        if 'services' in bom_json.keys():
            for i in range(len(bom_json['services'])):
                if not self.services_supports_properties() and 'properties' in bom_json['services'][i].keys():
                    del bom_json['services'][i]['properties']

                if not self.services_supports_release_notes() and 'releaseNotes' in bom_json['services'][i].keys():
                    del bom_json['services'][i]['releaseNotes']

        # Iterate externalReferences
        if 'externalReferences' in bom_json.keys():
            for i in range(len(bom_json['externalReferences'])):
                if not self.external_references_supports_hashes() \
                        and 'hashes' in bom_json['externalReferences'][i].keys():
                    del bom_json['externalReferences'][i]['hashes']

        return json.dumps(bom_json)

    def output_as_string(self) -> str:
        self.generate()
        return self._json_output

    # Builder Methods
    def _create_bom_element(self) -> Dict[str, Union[str, int]]:
        return {
            "$schema": str(self._get_schema_uri()),
            "bomFormat": "CycloneDX",
            "specVersion": str(self.get_schema_version()),
            "serialNumber": self.get_bom().get_urn_uuid(),
            "version": 1
        }

    @abstractmethod
    def _get_schema_uri(self) -> Optional[str]:
        pass

    def _recurse_specialise_component(self, bom_json: Dict[Any, Any], base_key: str = 'components') -> Dict[Any, Any]:
        if base_key in bom_json.keys():
            for i in range(len(bom_json[base_key])):
                if not self.component_supports_mime_type_attribute() \
                        and 'mime-type' in bom_json[base_key][i].keys():
                    del bom_json[base_key][i]['mime-type']

                if not self.component_supports_supplier() and 'supplier' in bom_json[base_key][i].keys():
                    del bom_json[base_key][i]['supplier']

                if not self.component_supports_author() and 'author' in bom_json[base_key][i].keys():
                    del bom_json[base_key][i]['author']

                if self.component_version_optional() and 'version' in bom_json[base_key][i] \
                        and bom_json[base_key][i].get('version', '') == "":
                    del bom_json[base_key][i]['version']

                if not self.component_supports_pedigree() and 'pedigree' in bom_json[base_key][i].keys():
                    del bom_json[base_key][i]['pedigree']
                elif 'pedigree' in bom_json[base_key][i].keys():
                    if 'ancestors' in bom_json[base_key][i]['pedigree'].keys():
                        # recurse into ancestors
                        bom_json[base_key][i]['pedigree'] = self._recurse_specialise_component(
                            bom_json=bom_json[base_key][i]['pedigree'], base_key='ancestors'
                        )
                    if 'descendants' in bom_json[base_key][i]['pedigree'].keys():
                        # recurse into descendants
                        bom_json[base_key][i]['pedigree'] = self._recurse_specialise_component(
                            bom_json=bom_json[base_key][i]['pedigree'], base_key='descendants'
                        )
                    if 'variants' in bom_json[base_key][i]['pedigree'].keys():
                        # recurse into variants
                        bom_json[base_key][i]['pedigree'] = self._recurse_specialise_component(
                            bom_json=bom_json[base_key][i]['pedigree'], base_key='variants'
                        )

                if not self.external_references_supports_hashes() and 'externalReferences' \
                        in bom_json[base_key][i].keys():
                    for j in range(len(bom_json[base_key][i]['externalReferences'])):
                        del bom_json[base_key][i]['externalReferences'][j]['hashes']

                if not self.component_supports_properties() and 'properties' in bom_json[base_key][i].keys():
                    del bom_json[base_key][i]['properties']

                # recurse
                if 'components' in bom_json[base_key][i].keys():
                    bom_json[base_key][i] = self._recurse_specialise_component(bom_json=bom_json[base_key][i])

                if not self.component_supports_evidence() and 'evidence' in bom_json[base_key][i].keys():
                    del bom_json[base_key][i]['evidence']

                if not self.component_supports_release_notes() and 'releaseNotes' in bom_json[base_key][i].keys():
                    del bom_json[base_key][i]['releaseNotes']

        return bom_json


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
