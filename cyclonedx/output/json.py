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
from typing import Any, Dict, List, Optional, Union

from ..exception.output import FormatNotSupportedException
from ..model.bom import Bom
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
            dep_components = self._chained_components(bom)
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
        if 'metadata' in bom_json.keys():
            if not self.bom_supports_metadata():
                del bom_json['metadata']
            else:
                if 'tools' in bom_json['metadata'].keys():
                    if not self.bom_metadata_supports_tools():
                        del bom_json['metadata']['tools']
                    else:
                        if not self.bom_metadata_supports_tools_external_references():
                            for _tool in bom_json['metadata']['tools']:
                                if 'externalReferences' in _tool.keys():
                                    del _tool['externalReferences']
                                del _tool
                if 'licenses' in bom_json['metadata'].keys() and not self.bom_metadata_supports_licenses():
                    del bom_json['metadata']['licenses']
                if 'properties' in bom_json['metadata'].keys() and not self.bom_metadata_supports_properties():
                    del bom_json['metadata']['properties']

                if self.get_bom().metadata.component:
                    bom_json['metadata'] = self._recurse_specialise_component(bom_json['metadata'], 'component')

        bom_json = self._recurse_specialise_component(bom_json)

        if 'services' in bom_json.keys():
            for _service in bom_json['services']:
                if 'properties' in _service.keys() and not self.services_supports_properties():
                    del _service['properties']
                if 'releaseNotes' in _service.keys() and not self.services_supports_release_notes():
                    del _service['releaseNotes']
                del _service

        if 'externalReferences' in bom_json.keys():
            if not self.external_references_supports_hashes():
                for _externalReference in bom_json['externalReferences']:
                    if 'hashes' in _externalReference.keys():
                        del _externalReference['hashes']
                    del _externalReference

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
            if isinstance(bom_json[base_key], dict):
                bom_json[base_key] = self._specialise_component_data(component_json=bom_json[base_key])
            else:
                for i in range(len(bom_json[base_key])):
                    bom_json[base_key][i] = self._specialise_component_data(component_json=bom_json[base_key][i])

        return bom_json

    def _specialise_component_data(self, component_json: Dict[Any, Any]) -> Dict[Any, Any]:
        if not self.component_supports_mime_type_attribute() and 'mime-type' in component_json.keys():
            del component_json['mime-type']

        if not self.component_supports_supplier() and 'supplier' in component_json.keys():
            del component_json['supplier']

        if not self.component_supports_author() and 'author' in component_json.keys():
            del component_json['author']

        if self.component_version_optional() and 'version' in component_json \
                and component_json.get('version', '') == "":
            del component_json['version']

        if not self.component_supports_pedigree() and 'pedigree' in component_json.keys():
            del component_json['pedigree']
        elif 'pedigree' in component_json.keys():
            if 'ancestors' in component_json['pedigree'].keys():
                # recurse into ancestors
                component_json['pedigree'] = self._recurse_specialise_component(
                    bom_json=component_json['pedigree'], base_key='ancestors'
                )
            if 'descendants' in component_json['pedigree'].keys():
                # recurse into descendants
                component_json['pedigree'] = self._recurse_specialise_component(
                    bom_json=component_json['pedigree'], base_key='descendants'
                )
            if 'variants' in component_json['pedigree'].keys():
                # recurse into variants
                component_json['pedigree'] = self._recurse_specialise_component(
                    bom_json=component_json['pedigree'], base_key='variants'
                )

        if not self.external_references_supports_hashes() and 'externalReferences' \
                in component_json.keys():
            for j in range(len(component_json['externalReferences'])):
                del component_json['externalReferences'][j]['hashes']

        if not self.component_supports_properties() and 'properties' in component_json.keys():
            del component_json['properties']

        # recurse
        if 'components' in component_json.keys():
            component_json = self._recurse_specialise_component(bom_json=component_json)

        if not self.component_supports_evidence() and 'evidence' in component_json.keys():
            del component_json['evidence']

        if not self.component_supports_release_notes() and 'releaseNotes' in component_json.keys():
            del component_json['releaseNotes']

        return component_json


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
