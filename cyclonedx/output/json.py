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

from . import BaseOutput
from .schema import BaseSchemaVersion, SchemaVersion1Dot0, SchemaVersion1Dot1, SchemaVersion1Dot2, SchemaVersion1Dot3
from ..model.component import Component


class Json(BaseOutput, BaseSchemaVersion):

    def output_as_string(self) -> str:
        return json.dumps(self._get_json())

    def _get_json(self) -> dict:
        components = list(map(self._get_component_as_dict, self.get_bom().get_components()))

        response = {
            "bomFormat": "CycloneDX",
            "specVersion": str(self.get_schema_version()),
            "serialNumber": self.get_bom().get_urn_uuid(),
            "version": 1,
            "components": components
        }

        if self.bom_supports_metadata():
            response['metadata'] = self._get_metadata_as_dict()

        return response

    def _get_component_as_dict(self, component: Component) -> dict:
        c = {
            "type": component.get_type().value,
            "name": component.get_name(),
            "version": component.get_version(),
            "purl": component.get_purl()
        }

        if component.get_namespace():
            c['group'] = component.get_namespace()

        if component.get_hashes():
            hashes = []
            for component_hash in component.get_hashes():
                hashes.append({
                    "alg": component_hash.get_algorithm().value,
                    "content": component_hash.get_hash_value()
                })
            c['hashes'] = hashes

        if component.get_license():
            c['licenses'] = [
                {
                    "license": {
                        "name": component.get_license()
                    }
                }
            ]

        if self.component_supports_author() and component.get_author():
            c['author'] = component.get_author()

        if self.component_supports_external_references() and component.get_external_references():
            c['externalReferences'] = []
            for ext_ref in component.get_external_references():
                ref = {
                    "type": ext_ref.get_reference_type().value,
                    "url": ext_ref.get_url()
                }

                if ext_ref.get_comment():
                    ref['comment'] = ext_ref.get_comment()

                if ext_ref.get_hashes():
                    ref_hashes = []
                    for ref_hash in ext_ref.get_hashes():
                        ref_hashes.append({
                            "alg": ref_hash.get_algorithm().value,
                            "content": ref_hash.get_hash_value()
                        })
                    ref['hashes'] = ref_hashes

                c['externalReferences'].append(ref)

        return c

    def _get_metadata_as_dict(self) -> dict:
        bom_metadata = self.get_bom().get_metadata()
        metadata = {
            "timestamp": bom_metadata.get_timestamp().isoformat()
        }

        if self.bom_metadata_supports_tools() and len(bom_metadata.get_tools()) > 0:
            metadata['tools'] = []
            for tool in bom_metadata.get_tools():
                tool_dict = {
                    "vendor": tool.get_vendor(),
                    "name": tool.get_name(),
                    "version": tool.get_version()
                }

                if len(tool.get_hashes()) > 0:
                    hashes = []
                    for tool_hash in tool.get_hashes():
                        hashes.append({
                            "alg": tool_hash.get_algorithm().value,
                            "content": tool_hash.get_hash_value()
                        })
                    tool_dict['hashes'] = hashes

                metadata['tools'].append(tool_dict)

        return metadata


class JsonV1Dot0(Json, SchemaVersion1Dot0):
    pass


class JsonV1Dot1(Json, SchemaVersion1Dot1):
    pass


class JsonV1Dot2(Json, SchemaVersion1Dot2):
    pass


class JsonV1Dot3(Json, SchemaVersion1Dot3):
    pass
