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
from typing import cast, Any, Dict, List, Optional, Union

from . import BaseOutput, SchemaVersion
from .schema import BaseSchemaVersion, SchemaVersion1Dot0, SchemaVersion1Dot1, SchemaVersion1Dot2, SchemaVersion1Dot3, \
    SchemaVersion1Dot4
from .serializer.json import CycloneDxJSONEncoder
from ..exception.output import FormatNotSupportedException
from ..model.bom import Bom
from ..model.component import Component

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

        schema_uri: Optional[str] = self._get_schema_uri()
        if not schema_uri:
            raise FormatNotSupportedException(
                f'JSON is not supported by CycloneDX in schema version {self.schema_version.to_version()}'
            )

        vulnerabilities: Dict[str, List[Dict[Any, Any]]] = {"vulnerabilities": []}
        if self.get_bom().components:
            for component in cast(List[Component], self.get_bom().components):
                for vulnerability in component.get_vulnerabilities():
                    vulnerabilities['vulnerabilities'].append(
                        json.loads(json.dumps(vulnerability, cls=CycloneDxJSONEncoder))
                    )

        bom_json = json.loads(json.dumps(self.get_bom(), cls=CycloneDxJSONEncoder))
        bom_json = json.loads(self._specialise_output_for_schema_version(bom_json=bom_json))
        if self.bom_supports_vulnerabilities() and vulnerabilities['vulnerabilities']:
            self._json_output = json.dumps(
                {**self._create_bom_element(), **bom_json, **vulnerabilities}
            )
        else:
            self._json_output = json.dumps({**self._create_bom_element(), **bom_json})

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
        if 'components' in bom_json.keys():
            for i in range(len(bom_json['components'])):
                if self.component_version_optional() and bom_json['components'][i]['version'] == "":
                    del bom_json['components'][i]['version']

                if not self.component_supports_author() and 'author' in bom_json['components'][i].keys():
                    del bom_json['components'][i]['author']

                if not self.component_supports_mime_type_attribute() \
                        and 'mime-type' in bom_json['components'][i].keys():
                    del bom_json['components'][i]['mime-type']

                if not self.component_supports_release_notes() and 'releaseNotes' in bom_json['components'][i].keys():
                    del bom_json['components'][i]['releaseNotes']
        else:
            bom_json['components'] = []

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

        # Iterate Vulnerabilities
        if 'vulnerabilities' in bom_json.keys():
            for i in range(len(bom_json['vulnerabilities'])):
                print("Checking " + str(bom_json['vulnerabilities'][i]))

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


class JsonV1Dot0(Json, SchemaVersion1Dot0):

    def _get_schema_uri(self) -> Optional[str]:
        return None


class JsonV1Dot1(Json, SchemaVersion1Dot1):

    def _get_schema_uri(self) -> Optional[str]:
        return None


class JsonV1Dot2(Json, SchemaVersion1Dot2):

    def _get_schema_uri(self) -> Optional[str]:
        return 'http://cyclonedx.org/schema/bom-1.2a.schema.json'


class JsonV1Dot3(Json, SchemaVersion1Dot3):

    def _get_schema_uri(self) -> Optional[str]:
        return 'http://cyclonedx.org/schema/bom-1.3.schema.json'


class JsonV1Dot4(Json, SchemaVersion1Dot4):

    def _get_schema_uri(self) -> Optional[str]:
        return 'http://cyclonedx.org/schema/bom-1.4.schema.json'
