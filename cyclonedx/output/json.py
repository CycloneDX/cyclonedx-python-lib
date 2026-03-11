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

from abc import abstractmethod
from json import dumps as json_dumps
from typing import TYPE_CHECKING, Any, Literal, Optional, Union

from ..exception.output import FormatNotSupportedException
from ..schema import OutputFormat, SchemaVersion
from ..schema.schema import (
    BaseSchemaVersion,
    SchemaVersion1Dot0,
    SchemaVersion1Dot1,
    SchemaVersion1Dot2,
    SchemaVersion1Dot3,
    SchemaVersion1Dot4,
    SchemaVersion1Dot5,
    SchemaVersion1Dot6,
    SchemaVersion1Dot7,
)
from ..serialization import make_converter
from . import BaseOutput, BomRefDiscriminator

if TYPE_CHECKING:  # pragma: no cover
    from ..model.bom import Bom


class Json(BaseOutput, BaseSchemaVersion):

    def __init__(self, bom: 'Bom') -> None:
        super().__init__(bom=bom)
        self._bom_json: dict[str, Any] = dict()

    @property
    def schema_version(self) -> SchemaVersion:
        return self.schema_version_enum

    @property
    def output_format(self) -> Literal[OutputFormat.JSON]:
        return OutputFormat.JSON

    def _validate_component_types(self, bom: 'Bom') -> None:
        """Validate that all component types are supported by the schema version."""
        from ..exception.serialization import SerializationOfUnsupportedComponentTypeException
        from ..serialization._converters import _get_component_type_versions

        type_versions = _get_component_type_versions()

        def check_component(comp: Any) -> None:
            if comp.type:
                supported_versions = type_versions.get(comp.type.value, set())
                if self.schema_version_enum not in supported_versions:
                    raise SerializationOfUnsupportedComponentTypeException(
                        f"Component type '{comp.type.value}' is not supported in schema version {self.schema_version_enum.value}"
                    )
            # Check nested components
            if comp.components:
                for nested in comp.components:
                    check_component(nested)

        # Check top-level components
        for comp in bom.components:
            check_component(comp)

        # Check metadata component
        if bom.metadata and bom.metadata.component:
            check_component(bom.metadata.component)

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
        bom = self.get_bom()
        bom.validate()

        # Validate component types
        self._validate_component_types(bom)

        # Create a converter for this schema version
        converter = make_converter(self.schema_version_enum)

        with BomRefDiscriminator.from_bom(bom):
            bom_json: dict[str, Any] = converter.unstructure(bom)

        # Post-process to wrap licenses for JSON format
        self._wrap_json_licenses(bom_json)

        # Post-process evidence identity for 1.5 (single object, not array)
        if self.schema_version_enum == SchemaVersion.V1_5:
            self._transform_evidence_identity_for_1_5(bom_json)

        # Filter out enum values not supported in this schema version
        self._filter_unsupported_enum_values(bom_json)

        bom_json.update(_json_core)
        self._bom_json = bom_json

    def _wrap_json_licenses(self, data: Any) -> None:
        """Recursively wrap licenses in JSON format.

        CycloneDX JSON wraps licenses: {"license": {...}} or {"expression": "..."}
        """
        if isinstance(data, dict):
            if 'licenses' in data and isinstance(data['licenses'], list):
                wrapped = []
                for lic in data['licenses']:
                    if isinstance(lic, dict):
                        if 'expression' in lic:
                            # License expression - already in correct format from unstructure
                            wrapped.append(lic)
                        elif 'value' in lic:
                            # License expression (old format) - wrap it
                            new_lic = {'expression': lic['value']}
                            if 'bom-ref' in lic:
                                new_lic['bom-ref'] = lic['bom-ref']
                            if 'acknowledgement' in lic:
                                new_lic['acknowledgement'] = lic['acknowledgement']
                            wrapped.append(new_lic)
                        elif 'id' in lic or 'name' in lic:
                            # Disjunctive license - wrap in {"license": {...}}
                            wrapped.append({'license': lic})
                        else:
                            wrapped.append(lic)
                    else:
                        wrapped.append(lic)
                data['licenses'] = wrapped

            # Recurse into all values
            for value in data.values():
                self._wrap_json_licenses(value)
        elif isinstance(data, list):
            for item in data:
                self._wrap_json_licenses(item)
        self.generated = True

    def _transform_evidence_identity_for_1_5(self, data: Any) -> None:
        """Transform evidence.identity from array to single object for schema 1.5.

        In CycloneDX 1.5, evidence.identity is a single object.
        In 1.6+, it became an array.
        """
        if isinstance(data, dict):
            # Check for evidence.identity
            if 'evidence' in data and isinstance(data['evidence'], dict):
                evidence = data['evidence']
                if 'identity' in evidence and isinstance(evidence['identity'], list):
                    # Convert array to single object (first element)
                    identity_list = evidence['identity']
                    if identity_list:
                        evidence['identity'] = identity_list[0]
                    else:
                        del evidence['identity']

            # Recurse into all values
            for value in data.values():
                self._transform_evidence_identity_for_1_5(value)
        elif isinstance(data, list):
            for item in data:
                self._transform_evidence_identity_for_1_5(item)

    def _filter_unsupported_enum_values(self, data: Any) -> None:
        """Recursively filter out enum values not supported in this schema version."""
        from ..model import EXTREF_TYPE_VERSIONS, HASH_ALG_VERSIONS, ExternalReferenceType, HashAlgorithm
        from ..model.component import COMPONENT_SCOPE_VERSIONS, ComponentScope
        from ..model.issue import ISSUE_CLASSIFICATION_VERSIONS, IssueClassification
        from ..model.vulnerability import VULNERABILITY_SCORE_SOURCE_VERSIONS, VulnerabilityScoreSource

        if isinstance(data, dict):
            # Filter hashes
            if 'hashes' in data and isinstance(data['hashes'], list):
                data['hashes'] = [
                    h for h in data['hashes']
                    if not isinstance(h, dict) or 'alg' not in h or
                    self.schema_version_enum in HASH_ALG_VERSIONS.get(
                        HashAlgorithm(h['alg']), set())
                ]

            # Filter external references by type
            if 'externalReferences' in data and isinstance(data['externalReferences'], list):
                data['externalReferences'] = [
                    er for er in data['externalReferences']
                    if not isinstance(er, dict) or 'type' not in er or
                    self.schema_version_enum in EXTREF_TYPE_VERSIONS.get(
                        ExternalReferenceType(er['type']), set())
                ]

            # Filter issues by classification
            if 'issues' in data and isinstance(data['issues'], list):
                data['issues'] = [
                    issue for issue in data['issues']
                    if not isinstance(issue, dict) or 'classification' not in issue or
                    self.schema_version_enum in ISSUE_CLASSIFICATION_VERSIONS.get(
                        IssueClassification(issue['classification']), set())
                ]

            # Filter vulnerability ratings by method
            if 'ratings' in data and isinstance(data['ratings'], list):
                data['ratings'] = [
                    r for r in data['ratings']
                    if not isinstance(r, dict) or 'method' not in r or
                    self.schema_version_enum in VULNERABILITY_SCORE_SOURCE_VERSIONS.get(
                        VulnerabilityScoreSource(r['method']), set())
                ]

            # Filter out unsupported component scope values
            if 'scope' in data and data['scope'] is not None:
                try:
                    scope = ComponentScope(data['scope'])
                    if self.schema_version_enum not in COMPONENT_SCOPE_VERSIONS.get(scope, set()):
                        del data['scope']
                except (ValueError, KeyError):
                    pass

            # Recurse into all values
            for value in data.values():
                self._filter_unsupported_enum_values(value)
        elif isinstance(data, list):
            for item in data:
                self._filter_unsupported_enum_values(item)

    def output_as_string(self, *,
                         indent: Optional[Union[int, str]] = None,
                         **kwargs: Any) -> str:
        self.generate()
        return json_dumps(self._bom_json,
                          indent=indent)

    @abstractmethod
    def _get_schema_uri(self) -> Optional[str]:
        ...  # pragma: no cover


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


class JsonV1Dot5(Json, SchemaVersion1Dot5):

    def _get_schema_uri(self) -> str:
        return 'http://cyclonedx.org/schema/bom-1.5.schema.json'


class JsonV1Dot6(Json, SchemaVersion1Dot6):

    def _get_schema_uri(self) -> str:
        return 'http://cyclonedx.org/schema/bom-1.6.schema.json'


class JsonV1Dot7(Json, SchemaVersion1Dot7):

    def _get_schema_uri(self) -> str:
        return 'http://cyclonedx.org/schema/bom-1.7.schema.json'


BY_SCHEMA_VERSION: dict[SchemaVersion, type[Json]] = {
    SchemaVersion.V1_7: JsonV1Dot7,
    SchemaVersion.V1_6: JsonV1Dot6,
    SchemaVersion.V1_5: JsonV1Dot5,
    SchemaVersion.V1_4: JsonV1Dot4,
    SchemaVersion.V1_3: JsonV1Dot3,
    SchemaVersion.V1_2: JsonV1Dot2,
    SchemaVersion.V1_1: JsonV1Dot1,
    SchemaVersion.V1_0: JsonV1Dot0,
}
