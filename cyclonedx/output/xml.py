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


from typing import TYPE_CHECKING, Any, Literal, Optional, Union
from xml.dom.minidom import parseString as dom_parseString  # nosec B408
from xml.etree.ElementTree import Element as XmlElement, tostring as xml_dumps  # nosec B405

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


class Xml(BaseSchemaVersion, BaseOutput):
    def __init__(self, bom: 'Bom') -> None:
        super().__init__(bom=bom)
        self._bom_xml: str = ''

    @property
    def schema_version(self) -> SchemaVersion:
        return self.schema_version_enum

    @property
    def output_format(self) -> Literal[OutputFormat.XML]:
        return OutputFormat.XML

    # Fields that should be serialized as XML attributes (not child elements)
    _XML_ATTR_FIELDS = {
        'dependency': {'ref'},
        'component': {'bom-ref', 'type'},
        'service': {'bom-ref'},
        'vulnerability': {'bom-ref'},
        'license': {'bom-ref'},
        'hash': {'alg'},
        'issue': {'type'},
        'patch': {'type'},
        'swid': {'tagId', 'name', 'version', 'tagVersion', 'patch'},
        'identifiableAction': {'timestamp'},
        'attachment': {'content-type', 'encoding'},
        'property': {'name'},
        'reference': {'type'},  # External reference type is an attribute
        'text': {'content-type', 'encoding'},  # AttachedText attributes
        'standard': {'bom-ref'},
        'requirement': {'bom-ref'},
        'level': {'bom-ref'},
    }

    # Element ordering for CycloneDX XML schema (field name -> sequence number)
    _XML_ELEMENT_ORDER = {
        'component': ['type', 'bom-ref', 'supplier', 'manufacturer', 'authors', 'author', 'publisher',
                      'group', 'name', 'version', 'description', 'scope', 'hashes', 'licenses',
                      'copyright', 'patentAssertions', 'cpe', 'purl', 'omniborId', 'swhid', 'swid', 'modified',
                      'pedigree', 'externalReferences', 'properties', 'components', 'evidence', 'releaseNotes',
                      'modelCard', 'data', 'cryptoProperties', 'tags', 'signature'],
        'metadata': ['timestamp', 'lifecycles', 'tools', 'authors', 'component', 'manufacture',
                     'manufacturer', 'supplier', 'licenses', 'properties'],
        'service': ['bom-ref', 'provider', 'group', 'name', 'version', 'description', 'endpoints',
                    'authenticated', 'x-trust-boundary', 'trustZone', 'data', 'licenses',
                    'patentAssertions', 'externalReferences', 'properties', 'services', 'releaseNotes', 'tags'],
        'releaseNotes': ['type', 'title', 'featuredImage', 'socialImage', 'description', 'timestamp',
                         'aliases', 'tags', 'resolves', 'notes', 'properties'],
        'note': ['locale', 'text'],
        'issue': ['type', 'id', 'name', 'description', 'source', 'references'],
        'pedigree': ['ancestors', 'descendants', 'variants', 'commits', 'patches', 'notes'],
        'diff': ['text', 'url'],
        'patch': ['type', 'diff', 'resolves'],
        'frame': ['package', 'module', 'function', 'parameters', 'line', 'column', 'fullFilename'],
        'identity': ['field', 'confidence', 'concludedValue', 'methods', 'tools'],
        'method': ['technique', 'confidence', 'value'],
        'occurrence': ['bom-ref', 'location', 'line', 'offset', 'symbol', 'additionalContext'],
        'evidence': ['identity', 'occurrences', 'callstack', 'licenses', 'copyright'],
        'algorithmProperties': ['primitive', 'algorithmFamily', 'parameterSetIdentifier', 'curve', 'ellipticCurve',
                                'executionEnvironment', 'implementationPlatform', 'certificationLevel', 'mode',
                                'padding', 'cryptoFunctions', 'classicalSecurityLevel', 'nistQuantumSecurityLevel'],
        'cryptoProperties': ['assetType', 'algorithmProperties', 'certificateProperties', 'relatedCryptoMaterialProperties',
                             'protocolProperties', 'oid'],
        'protocolProperties': ['type', 'version', 'cipherSuites', 'ikev2TransformTypes', 'cryptoRefArray'],
        'cipherSuite': ['name', 'algorithms', 'identifiers'],
        'vulnerability': ['id', 'source', 'references', 'ratings', 'cwes', 'description', 'detail',
                          'recommendation', 'workaround', 'proofOfConcept', 'advisories', 'created',
                          'published', 'updated', 'rejected', 'credits', 'tools', 'analysis',
                          'affects', 'properties'],
        'rating': ['source', 'score', 'severity', 'method', 'vector', 'justification'],
        'advisory': ['title', 'url'],
        'standard': ['bom-ref', 'name', 'version', 'description', 'owner', 'requirements', 'levels', 'externalReferences'],
        'requirement': ['bom-ref', 'identifier', 'title', 'text', 'descriptions', 'openCre', 'parent', 'properties', 'externalReferences'],
        'level': ['bom-ref', 'identifier', 'title', 'description', 'requirements'],
        'target': ['ref', 'versions'],
        'version': ['version', 'range', 'status'],
        'analysis': ['state', 'justification', 'response', 'detail', 'firstIssued', 'lastUpdated'],
        'organization': ['name', 'address', 'url', 'contact'],
        'individual': ['name', 'email', 'phone'],
        'contact': ['name', 'email', 'phone'],
        'address': ['country', 'region', 'locality', 'postOfficeBoxNumber', 'postalCode', 'streetAddress'],
    }

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

    def _ensure_modified_field(self, comp: dict) -> None:
        """Recursively ensure 'modified' field is present in component dicts for 1.0/1.1 schemas."""
        if 'modified' not in comp:
            comp['modified'] = False
        # Handle nested components
        if 'components' in comp and comp['components']:
            for nested_comp in comp['components']:
                self._ensure_modified_field(nested_comp)

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

    def _bom_to_xml(self, bom: 'Bom', xmlns: str) -> XmlElement:
        """Convert a Bom object to XML Element using the new serialization."""
        from ..serialization._xml import CycloneDxXmlSerializer

        # Validate component types first
        self._validate_component_types(bom)

        serializer = CycloneDxXmlSerializer(self.schema_version_enum)

        # Create root bom element with namespace-qualified tag
        def ns_tag(name): return f'{{{xmlns}}}{name}'
        root = XmlElement(ns_tag('bom'), {
            'version': str(bom.version),
        })

        # serialNumber was introduced in 1.1
        if bom.serial_number and self.schema_version_enum != SchemaVersion.V1_0:
            root.set('serialNumber', serializer.serialize_uuid(bom.serial_number))

        # Convert bom to dict using cattrs, then convert to XML
        converter = make_converter(self.schema_version_enum)
        bom_dict = converter.unstructure(bom)

        # Filter out enum values not supported in this schema version
        self._filter_unsupported_enum_values(bom_dict)

        # Add metadata if present
        if 'metadata' in bom_dict and bom_dict['metadata']:
            self._dict_to_xml(bom_dict['metadata'], root, 'metadata', xmlns)

        # Add components if present (or empty element for 1.0/1.1 which require it)
        has_components = 'components' in bom_dict and bom_dict['components']
        requires_components = self.schema_version_enum in (SchemaVersion.V1_0, SchemaVersion.V1_1)
        if has_components or requires_components:
            components_elem = XmlElement(ns_tag('components'))
            if has_components:
                for comp in bom_dict['components']:
                    # For 1.0/1.1, ensure 'modified' field is present (required in these schemas)
                    if self.schema_version_enum in (SchemaVersion.V1_0, SchemaVersion.V1_1):
                        self._ensure_modified_field(comp)
                    self._dict_to_xml(comp, components_elem, 'component', xmlns)
            root.append(components_elem)

        # Add services if present
        if 'services' in bom_dict and bom_dict['services']:
            services_elem = XmlElement(ns_tag('services'))
            for svc in bom_dict['services']:
                self._dict_to_xml(svc, services_elem, 'service', xmlns)
            root.append(services_elem)

        # Add externalReferences if present
        if 'externalReferences' in bom_dict and bom_dict['externalReferences']:
            refs_elem = XmlElement(ns_tag('externalReferences'))
            for ref in bom_dict['externalReferences']:
                self._dict_to_xml(ref, refs_elem, 'reference', xmlns)
            root.append(refs_elem)

        # Add dependencies if present
        if 'dependencies' in bom_dict and bom_dict['dependencies']:
            deps_elem = XmlElement(ns_tag('dependencies'))
            for dep in bom_dict['dependencies']:
                self._dependency_to_xml(dep, deps_elem, xmlns)
            root.append(deps_elem)

        # Add compositions if present
        if 'compositions' in bom_dict and bom_dict['compositions']:
            comp_elem = XmlElement(ns_tag('compositions'))
            for composition in bom_dict['compositions']:
                self._dict_to_xml(composition, comp_elem, 'composition', xmlns)
            root.append(comp_elem)

        # Add properties if present (comes before vulnerabilities)
        if 'properties' in bom_dict and bom_dict['properties']:
            props_elem = XmlElement(ns_tag('properties'))
            for prop in bom_dict['properties']:
                self._property_to_xml(prop, props_elem, xmlns)
            root.append(props_elem)

        # Add vulnerabilities if present
        if 'vulnerabilities' in bom_dict and bom_dict['vulnerabilities']:
            vulns_elem = XmlElement(ns_tag('vulnerabilities'))
            for vuln in bom_dict['vulnerabilities']:
                self._dict_to_xml(vuln, vulns_elem, 'vulnerability', xmlns)
            root.append(vulns_elem)

        # Add annotations if present
        if 'annotations' in bom_dict and bom_dict['annotations']:
            annot_elem = XmlElement(ns_tag('annotations'))
            for annotation in bom_dict['annotations']:
                self._dict_to_xml(annotation, annot_elem, 'annotation', xmlns)
            root.append(annot_elem)

        # Add formulation if present
        if 'formulation' in bom_dict and bom_dict['formulation']:
            form_elem = XmlElement(ns_tag('formulation'))
            for formula in bom_dict['formulation']:
                self._dict_to_xml(formula, form_elem, 'formula', xmlns)
            root.append(form_elem)

        # Add definitions if present (introduced in 1.5)
        if 'definitions' in bom_dict and bom_dict['definitions']:
            defs_elem = XmlElement(ns_tag('definitions'))
            definitions = bom_dict['definitions']
            # Handle standards
            if 'standards' in definitions and definitions['standards']:
                stds_elem = XmlElement(ns_tag('standards'))
                for std in definitions['standards']:
                    self._dict_to_xml(std, stds_elem, 'standard', xmlns)
                defs_elem.append(stds_elem)
            root.append(defs_elem)

        return root

    def _dependency_to_xml(self, dep: dict, parent: XmlElement, xmlns: str) -> None:
        """Convert a dependency dict to XML with ref as attribute."""
        def ns_tag(n): return f'{{{xmlns}}}{n}'
        elem = XmlElement(ns_tag('dependency'))

        # ref is an attribute
        if 'ref' in dep:
            elem.set('ref', str(dep['ref']))

        # dependsOn becomes nested dependency elements
        if 'dependsOn' in dep and dep['dependsOn']:
            for nested_ref in dep['dependsOn']:
                nested = XmlElement(ns_tag('dependency'))
                nested.set('ref', str(nested_ref))
                elem.append(nested)

        parent.append(elem)

    def _property_to_xml(self, prop: dict, parent: XmlElement, xmlns: str) -> None:
        """Convert a property dict to XML with name as attribute and value as text."""
        def ns_tag(n): return f'{{{xmlns}}}{n}'
        elem = XmlElement(ns_tag('property'))

        if 'name' in prop:
            elem.set('name', str(prop['name']))
        if 'value' in prop:
            elem.text = str(prop['value'])

        parent.append(elem)

    def _dict_to_xml(self, data: Any, parent: XmlElement, name: str, xmlns: str) -> None:
        """Recursively convert a dict to XML elements."""
        if data is None:
            return

        def ns_tag(n): return f'{{{xmlns}}}{n}'

        # Get attribute fields for this element type
        attr_fields = self._XML_ATTR_FIELDS.get(name, set())
        # Get element order for this element type
        element_order = self._XML_ELEMENT_ORDER.get(name, [])

        if isinstance(data, dict):
            elem = XmlElement(ns_tag(name))

            # First, handle attribute fields
            for key in list(data.keys()):
                if key in attr_fields and data[key] is not None:
                    elem.set(key, str(data[key]))

            # Sort remaining keys by element order if specified
            remaining_keys = [k for k in data.keys() if k not in attr_fields]
            if element_order:
                def sort_key(k):
                    try:
                        return element_order.index(k)
                    except ValueError:
                        return 999  # Unknown keys go at the end
                remaining_keys = sorted(remaining_keys, key=sort_key)

            # Then handle child elements
            for key in remaining_keys:
                value = data[key]
                if value is not None:
                    # Special handling for specific nested structures
                    if key == 'hashes' and isinstance(value, list):
                        hashes_elem = XmlElement(ns_tag('hashes'))
                        for h in value:
                            self._hash_to_xml(h, hashes_elem, xmlns)
                        if len(hashes_elem) > 0:
                            elem.append(hashes_elem)
                    elif key == 'licenses' and isinstance(value, list):
                        licenses_elem = XmlElement(ns_tag('licenses'))
                        for lic in value:
                            self._license_to_xml(lic, licenses_elem, xmlns)
                        if len(licenses_elem) > 0:
                            elem.append(licenses_elem)
                    elif key == 'externalReferences' and isinstance(value, list):
                        refs_elem = XmlElement(ns_tag('externalReferences'))
                        for ref in value:
                            self._dict_to_xml(ref, refs_elem, 'reference', xmlns)
                        if len(refs_elem) > 0:
                            elem.append(refs_elem)
                    elif key == 'properties' and isinstance(value, list):
                        props_elem = XmlElement(ns_tag('properties'))
                        for prop in value:
                            self._property_to_xml(prop, props_elem, xmlns)
                        if len(props_elem) > 0:
                            elem.append(props_elem)
                    elif key == 'components' and isinstance(value, list):
                        comps_elem = XmlElement(ns_tag('components'))
                        for comp in value:
                            self._dict_to_xml(comp, comps_elem, 'component', xmlns)
                        if len(comps_elem) > 0:
                            elem.append(comps_elem)
                    elif key == 'tools' and isinstance(value, dict):
                        # Tools can have tools, components, services (newer format)
                        tools_elem = XmlElement(ns_tag('tools'))
                        if 'tools' in value and value['tools']:
                            for t in value['tools']:
                                self._dict_to_xml(t, tools_elem, 'tool', xmlns)
                        if 'components' in value and value['components']:
                            comps = XmlElement(ns_tag('components'))
                            for c in value['components']:
                                self._dict_to_xml(c, comps, 'component', xmlns)
                            tools_elem.append(comps)
                        if 'services' in value and value['services']:
                            svcs = XmlElement(ns_tag('services'))
                            for s in value['services']:
                                self._dict_to_xml(s, svcs, 'service', xmlns)
                            tools_elem.append(svcs)
                        if len(tools_elem) > 0:
                            elem.append(tools_elem)
                    elif key == 'tools' and isinstance(value, list) and name == 'metadata':
                        # Metadata tools as flat list - wrap each in <tool>
                        tools_elem = XmlElement(ns_tag('tools'))
                        for t in value:
                            self._dict_to_xml(t, tools_elem, 'tool', xmlns)
                        if len(tools_elem) > 0:
                            elem.append(tools_elem)
                    elif key == 'tools' and isinstance(value, list) and name == 'identity':
                        # Identity tools - container with <tool ref="..."/> children
                        tools_elem = XmlElement(ns_tag('tools'))
                        for ref in value:
                            tool_elem = XmlElement(ns_tag('tool'))
                            tool_elem.set('ref', str(ref))
                            tools_elem.append(tool_elem)
                        if len(tools_elem) > 0:
                            elem.append(tools_elem)
                    elif key == 'tools' and isinstance(value, list) and name == 'vulnerability':
                        # Vulnerability tools - container with <tool> children
                        tools_elem = XmlElement(ns_tag('tools'))
                        for t in value:
                            self._dict_to_xml(t, tools_elem, 'tool', xmlns)
                        if len(tools_elem) > 0:
                            elem.append(tools_elem)
                    elif key == 'tools' and isinstance(value, dict) and name == 'vulnerability':
                        # Vulnerability tools as single dict
                        tools_elem = XmlElement(ns_tag('tools'))
                        self._dict_to_xml(value, tools_elem, 'tool', xmlns)
                        elem.append(tools_elem)
                    elif key == 'data' and isinstance(value, list) and name == 'service':
                        # Service data is a container with classification children
                        data_elem = XmlElement(ns_tag('data'))
                        for dc in value:
                            self._data_classification_to_xml(dc, data_elem, xmlns)
                        if len(data_elem) > 0:
                            elem.append(data_elem)
                    elif key == 'services' and isinstance(value, list) and name == 'service':
                        # Nested services within a service - container with <service> children
                        services_elem = XmlElement(ns_tag('services'))
                        for svc in value:
                            self._dict_to_xml(svc, services_elem, 'service', xmlns)
                        if len(services_elem) > 0:
                            elem.append(services_elem)
                    elif key == 'endpoints' and isinstance(value, list):
                        # Endpoints - container with <endpoint> children
                        endpoints_elem = XmlElement(ns_tag('endpoints'))
                        for ep in value:
                            ep_elem = XmlElement(ns_tag('endpoint'))
                            ep_elem.text = str(ep)
                            endpoints_elem.append(ep_elem)
                        if len(endpoints_elem) > 0:
                            elem.append(endpoints_elem)
                    elif key == 'authors' and isinstance(value, list):
                        authors_elem = XmlElement(ns_tag('authors'))
                        for author in value:
                            self._dict_to_xml(author, authors_elem, 'author', xmlns)
                        if len(authors_elem) > 0:
                            elem.append(authors_elem)
                    elif key == 'lifecycles' and isinstance(value, list):
                        lc_elem = XmlElement(ns_tag('lifecycles'))
                        for lc in value:
                            self._dict_to_xml(lc, lc_elem, 'lifecycle', xmlns)
                        if len(lc_elem) > 0:
                            elem.append(lc_elem)
                    elif key == 'tags' and isinstance(value, list):
                        tags_elem = XmlElement(ns_tag('tags'))
                        for tag in value:
                            tag_elem = XmlElement(ns_tag('tag'))
                            tag_elem.text = str(tag)
                            tags_elem.append(tag_elem)
                        if len(tags_elem) > 0:
                            elem.append(tags_elem)
                    elif key == 'levels' and isinstance(value, list):
                        # Standard levels - wrap each in <level>
                        levels_elem = XmlElement(ns_tag('levels'))
                        for level in value:
                            self._dict_to_xml(level, levels_elem, 'level', xmlns)
                        if len(levels_elem) > 0:
                            elem.append(levels_elem)
                    elif key == 'requirements' and isinstance(value, list) and name == 'standard':
                        # Standard requirements - wrap each in <requirement>
                        reqs_elem = XmlElement(ns_tag('requirements'))
                        for req in value:
                            self._dict_to_xml(req, reqs_elem, 'requirement', xmlns)
                        if len(reqs_elem) > 0:
                            elem.append(reqs_elem)
                    elif key == 'requirements' and isinstance(value, list) and name == 'level':
                        # Level requirements are BomRefs - text content (refLinkType)
                        reqs_elem = XmlElement(ns_tag('requirements'))
                        for ref in value:
                            req_elem = XmlElement(ns_tag('requirement'))
                            req_elem.text = str(ref)
                            reqs_elem.append(req_elem)
                        if len(reqs_elem) > 0:
                            elem.append(reqs_elem)
                    elif key == 'descriptions' and isinstance(value, list):
                        # Requirement descriptions - container with <description> children
                        descs_elem = XmlElement(ns_tag('descriptions'))
                        for desc in value:
                            desc_elem = XmlElement(ns_tag('description'))
                            desc_elem.text = str(desc)
                            descs_elem.append(desc_elem)
                        if len(descs_elem) > 0:
                            elem.append(descs_elem)
                    elif key == 'openCre' and isinstance(value, list):
                        # openCre - multiple <openCre> elements directly
                        for cre in value:
                            cre_elem = XmlElement(ns_tag('openCre'))
                            cre_elem.text = str(cre)
                            elem.append(cre_elem)
                    elif key in ('ancestors', 'descendants', 'variants') and isinstance(value, list):
                        # Pedigree component lists - wrap each in <component>
                        container_elem = XmlElement(ns_tag(key))
                        for comp in value:
                            self._dict_to_xml(comp, container_elem, 'component', xmlns)
                        if len(container_elem) > 0:
                            elem.append(container_elem)
                    elif key == 'patches' and isinstance(value, list):
                        # Pedigree patches - wrap each in <patch>
                        patches_elem = XmlElement(ns_tag('patches'))
                        for patch in value:
                            self._dict_to_xml(patch, patches_elem, 'patch', xmlns)
                        if len(patches_elem) > 0:
                            elem.append(patches_elem)
                    elif key == 'resolves' and isinstance(value, list) and name == 'patch':
                        # Patch resolves - container with <issue> children
                        resolves_elem = XmlElement(ns_tag('resolves'))
                        for issue in value:
                            self._dict_to_xml(issue, resolves_elem, 'issue', xmlns)
                        if len(resolves_elem) > 0:
                            elem.append(resolves_elem)
                    elif key == 'commits' and isinstance(value, list):
                        # Pedigree commits - wrap each in <commit>
                        commits_elem = XmlElement(ns_tag('commits'))
                        for commit in value:
                            self._dict_to_xml(commit, commits_elem, 'commit', xmlns)
                        if len(commits_elem) > 0:
                            elem.append(commits_elem)
                    elif key == 'frames' and isinstance(value, list):
                        # Callstack frames - wrap each in <frame>
                        frames_elem = XmlElement(ns_tag('frames'))
                        for frame in value:
                            self._dict_to_xml(frame, frames_elem, 'frame', xmlns)
                        if len(frames_elem) > 0:
                            elem.append(frames_elem)
                    elif key == 'occurrences' and isinstance(value, list):
                        # Evidence occurrences - wrap each in <occurrence>
                        occ_elem = XmlElement(ns_tag('occurrences'))
                        for occ in value:
                            self._dict_to_xml(occ, occ_elem, 'occurrence', xmlns)
                        if len(occ_elem) > 0:
                            elem.append(occ_elem)
                    elif key == 'identity' and isinstance(value, list):
                        # Evidence identity - in 1.5, single object; in 1.6+, array
                        if self.schema_version_enum == SchemaVersion.V1_5:
                            # Only output first identity for 1.5
                            if value:
                                self._dict_to_xml(value[0], elem, 'identity', xmlns)
                        else:
                            # Output each directly for 1.6+
                            for ident in value:
                                self._dict_to_xml(ident, elem, 'identity', xmlns)
                    elif key == 'methods' and isinstance(value, list):
                        # Evidence methods - wrap each in <method>
                        methods_elem = XmlElement(ns_tag('methods'))
                        for method in value:
                            self._dict_to_xml(method, methods_elem, 'method', xmlns)
                        if len(methods_elem) > 0:
                            elem.append(methods_elem)
                    elif key == 'parameters' and isinstance(value, list) and name == 'frame':
                        # Frame parameters - container with <parameter> children
                        params_elem = XmlElement(ns_tag('parameters'))
                        for param in value:
                            param_elem = XmlElement(ns_tag('parameter'))
                            param_elem.text = str(param)
                            params_elem.append(param_elem)
                        if len(params_elem) > 0:
                            elem.append(params_elem)
                    elif key == 'cryptoFunctions' and isinstance(value, list):
                        # CryptoFunctions - container with <cryptoFunction> children
                        funcs_elem = XmlElement(ns_tag('cryptoFunctions'))
                        for func in value:
                            func_elem = XmlElement(ns_tag('cryptoFunction'))
                            func_elem.text = str(func)
                            funcs_elem.append(func_elem)
                        if len(funcs_elem) > 0:
                            elem.append(funcs_elem)
                    elif key == 'certificationLevel' and isinstance(value, list):
                        # CertificationLevel is a list of strings
                        for level in value:
                            level_elem = XmlElement(ns_tag('certificationLevel'))
                            level_elem.text = str(level)
                            elem.append(level_elem)
                    elif key == 'cipherSuites' and isinstance(value, list):
                        # CipherSuites - container with <cipherSuite> children
                        suites_elem = XmlElement(ns_tag('cipherSuites'))
                        for suite in value:
                            self._dict_to_xml(suite, suites_elem, 'cipherSuite', xmlns)
                        if len(suites_elem) > 0:
                            elem.append(suites_elem)
                    elif key == 'algorithms' and isinstance(value, list) and name == 'cipherSuite':
                        # CipherSuite algorithms - container with <algorithm> ref children
                        algs_elem = XmlElement(ns_tag('algorithms'))
                        for alg in value:
                            alg_elem = XmlElement(ns_tag('algorithm'))
                            alg_elem.set('ref', str(alg))
                            algs_elem.append(alg_elem)
                        if len(algs_elem) > 0:
                            elem.append(algs_elem)
                    elif key == 'ikev2TransformTypes' and isinstance(value, dict):
                        # ikev2TransformTypes - output as-is
                        self._dict_to_xml(value, elem, 'ikev2TransformTypes', xmlns)
                    elif key == 'cryptoRef' and isinstance(value, str):
                        # cryptoRef is a bom-ref string
                        ref_elem = XmlElement(ns_tag('cryptoRef'))
                        ref_elem.text = str(value)
                        elem.append(ref_elem)
                    elif key == 'cryptoRefArray' and isinstance(value, list):
                        # cryptoRefArray should output multiple cryptoRef elements (no container)
                        for ref in value:
                            ref_elem = XmlElement(ns_tag('cryptoRef'))
                            ref_elem.text = str(ref)
                            elem.append(ref_elem)
                    elif key == 'identifiers' and isinstance(value, list):
                        # Identifiers - container with <identifier> children
                        ids_elem = XmlElement(ns_tag('identifiers'))
                        for ident in value:
                            id_elem = XmlElement(ns_tag('identifier'))
                            id_elem.text = str(ident)
                            ids_elem.append(id_elem)
                        if len(ids_elem) > 0:
                            elem.append(ids_elem)
                    elif key == 'ratings' and isinstance(value, list) and name == 'vulnerability':
                        # Vulnerability ratings - container with <rating> children
                        ratings_elem = XmlElement(ns_tag('ratings'))
                        for rating in value:
                            self._dict_to_xml(rating, ratings_elem, 'rating', xmlns)
                        if len(ratings_elem) > 0:
                            elem.append(ratings_elem)
                    elif key == 'cwes' and isinstance(value, list) and name == 'vulnerability':
                        # Vulnerability cwes - container with <cwe> children
                        cwes_elem = XmlElement(ns_tag('cwes'))
                        for cwe in value:
                            cwe_elem = XmlElement(ns_tag('cwe'))
                            cwe_elem.text = str(cwe)
                            cwes_elem.append(cwe_elem)
                        if len(cwes_elem) > 0:
                            elem.append(cwes_elem)
                    elif key == 'references' and isinstance(value, list) and name == 'vulnerability':
                        # Vulnerability references - container with <reference> children
                        refs_elem = XmlElement(ns_tag('references'))
                        for ref in value:
                            self._dict_to_xml(ref, refs_elem, 'reference', xmlns)
                        if len(refs_elem) > 0:
                            elem.append(refs_elem)
                    elif key == 'affects' and isinstance(value, list):
                        # Vulnerability affects - container with <target> children
                        affects_elem = XmlElement(ns_tag('affects'))
                        for target in value:
                            self._dict_to_xml(target, affects_elem, 'target', xmlns)
                        if len(affects_elem) > 0:
                            elem.append(affects_elem)
                    elif key == 'advisories' and isinstance(value, list):
                        # Advisories - container with <advisory> children
                        adv_elem = XmlElement(ns_tag('advisories'))
                        for adv in value:
                            self._dict_to_xml(adv, adv_elem, 'advisory', xmlns)
                        if len(adv_elem) > 0:
                            elem.append(adv_elem)
                    elif key == 'credits' and isinstance(value, dict):
                        # Credits container
                        credits_elem = XmlElement(ns_tag('credits'))
                        if 'organizations' in value and value['organizations']:
                            orgs_elem = XmlElement(ns_tag('organizations'))
                            for org in value['organizations'] if isinstance(value['organizations'], list) else [value['organizations']]:
                                self._dict_to_xml(org, orgs_elem, 'organization', xmlns)
                            if len(orgs_elem) > 0:
                                credits_elem.append(orgs_elem)
                        if 'individuals' in value and value['individuals']:
                            indiv_elem = XmlElement(ns_tag('individuals'))
                            for indiv in value['individuals'] if isinstance(value['individuals'], list) else [value['individuals']]:
                                self._dict_to_xml(indiv, indiv_elem, 'individual', xmlns)
                            if len(indiv_elem) > 0:
                                credits_elem.append(indiv_elem)
                        if len(credits_elem) > 0:
                            elem.append(credits_elem)
                    elif key == 'versions' and isinstance(value, list) and name == 'target':
                        # Target versions - container with <version> children
                        versions_elem = XmlElement(ns_tag('versions'))
                        for ver in value:
                            self._dict_to_xml(ver, versions_elem, 'version', xmlns)
                        if len(versions_elem) > 0:
                            elem.append(versions_elem)
                    elif key == 'response' and isinstance(value, list) and name == 'analysis':
                        # Analysis responses - container with <response> children
                        responses_elem = XmlElement(ns_tag('responses'))
                        for resp in value:
                            resp_elem = XmlElement(ns_tag('response'))
                            resp_elem.text = str(resp)
                            responses_elem.append(resp_elem)
                        if len(responses_elem) > 0:
                            elem.append(responses_elem)
                    elif key == 'notes' and isinstance(value, list) and name == 'releaseNotes':
                        # ReleaseNotes notes - wrap each in <note>
                        notes_elem = XmlElement(ns_tag('notes'))
                        for note in value:
                            self._dict_to_xml(note, notes_elem, 'note', xmlns)
                        if len(notes_elem) > 0:
                            elem.append(notes_elem)
                    elif key == 'resolves' and isinstance(value, list) and name == 'releaseNotes':
                        # ReleaseNotes resolves - wrap each in <issue>
                        resolves_elem = XmlElement(ns_tag('resolves'))
                        for issue in value:
                            self._dict_to_xml(issue, resolves_elem, 'issue', xmlns)
                        if len(resolves_elem) > 0:
                            elem.append(resolves_elem)
                    elif key == 'aliases' and isinstance(value, list):
                        # Aliases container with <alias> children
                        aliases_elem = XmlElement(ns_tag('aliases'))
                        for alias in value:
                            alias_elem = XmlElement(ns_tag('alias'))
                            alias_elem.text = str(alias)
                            aliases_elem.append(alias_elem)
                        if len(aliases_elem) > 0:
                            elem.append(aliases_elem)
                    elif key == 'references' and isinstance(value, list) and name == 'issue':
                        # Issue references - container with <url> children
                        refs_elem = XmlElement(ns_tag('references'))
                        for ref in value:
                            url_elem = XmlElement(ns_tag('url'))
                            url_elem.text = str(ref)
                            refs_elem.append(url_elem)
                        if len(refs_elem) > 0:
                            elem.append(refs_elem)
                    elif key == 'copyright' and isinstance(value, list) and name == 'evidence':
                        # Evidence copyright - single element with <text> children
                        copyright_elem = XmlElement(ns_tag('copyright'))
                        for cp in value:
                            if isinstance(cp, dict) and 'text' in cp:
                                text_elem = XmlElement(ns_tag('text'))
                                text_elem.text = str(cp['text'])
                                copyright_elem.append(text_elem)
                            elif isinstance(cp, str):
                                text_elem = XmlElement(ns_tag('text'))
                                text_elem.text = str(cp)
                                copyright_elem.append(text_elem)
                        if len(copyright_elem) > 0:
                            elem.append(copyright_elem)
                    elif key == 'text' and isinstance(value, dict):
                        # AttachedText - content as text, contentType and encoding as attributes
                        self._attached_text_to_xml(value, elem, xmlns)
                    elif isinstance(value, dict):
                        self._dict_to_xml(value, elem, key, xmlns)
                    elif isinstance(value, list):
                        for item in value:
                            self._dict_to_xml(item, elem, key, xmlns)
                    else:
                        child = XmlElement(ns_tag(key))
                        # Handle boolean values (XML Schema expects lowercase true/false)
                        if isinstance(value, bool):
                            child.text = 'true' if value else 'false'
                        else:
                            child.text = str(value)
                        elem.append(child)

            if len(elem) > 0 or elem.text or len(elem.attrib) > 0:
                parent.append(elem)
        elif isinstance(data, list):
            for item in data:
                self._dict_to_xml(item, parent, name, xmlns)
        else:
            elem = XmlElement(ns_tag(name))
            # Handle boolean values (XML Schema expects lowercase true/false)
            if isinstance(data, bool):
                elem.text = 'true' if data else 'false'
            else:
                elem.text = str(data)
            parent.append(elem)

    def _hash_to_xml(self, hash_data: dict, parent: XmlElement, xmlns: str) -> None:
        """Convert a hash dict to XML with alg as attribute."""
        def ns_tag(n): return f'{{{xmlns}}}{n}'
        elem = XmlElement(ns_tag('hash'))

        if 'alg' in hash_data:
            elem.set('alg', str(hash_data['alg']))
        if 'content' in hash_data:
            elem.text = str(hash_data['content'])

        parent.append(elem)

    def _license_to_xml(self, lic_data: dict, parent: XmlElement, xmlns: str) -> None:
        """Convert a license dict to XML."""
        def ns_tag(n): return f'{{{xmlns}}}{n}'

        # Check if it's an expression or a license
        if 'expression' in lic_data or 'value' in lic_data:
            # License expression
            elem = XmlElement(ns_tag('expression'))
            elem.text = str(lic_data.get('expression') or lic_data.get('value', ''))
            # Add acknowledgement attribute if present (1.6+)
            if 'acknowledgement' in lic_data and lic_data['acknowledgement']:
                elem.set('acknowledgement', str(lic_data['acknowledgement']))
            # Add bom-ref attribute if present
            if 'bom-ref' in lic_data and lic_data['bom-ref']:
                elem.set('bom-ref', str(lic_data['bom-ref']))
            parent.append(elem)
        else:
            # Disjunctive license
            wrapper = XmlElement(ns_tag('license'))
            if 'bom-ref' in lic_data:
                wrapper.set('bom-ref', str(lic_data['bom-ref']))
            # Add acknowledgement attribute if present (1.6+)
            if 'acknowledgement' in lic_data and lic_data['acknowledgement']:
                wrapper.set('acknowledgement', str(lic_data['acknowledgement']))

            # Add id or name
            if 'id' in lic_data and lic_data['id']:
                id_elem = XmlElement(ns_tag('id'))
                id_elem.text = str(lic_data['id'])
                wrapper.append(id_elem)
            elif 'name' in lic_data and lic_data['name']:
                name_elem = XmlElement(ns_tag('name'))
                name_elem.text = str(lic_data['name'])
                wrapper.append(name_elem)

            # Add other fields
            for key in ['text', 'url']:
                if key in lic_data and lic_data[key]:
                    child = XmlElement(ns_tag(key))
                    if isinstance(lic_data[key], dict):
                        # AttachedText
                        if 'content' in lic_data[key]:
                            child.text = str(lic_data[key]['content'])
                        if 'contentType' in lic_data[key]:
                            child.set('content-type', str(lic_data[key]['contentType']))
                        if 'encoding' in lic_data[key]:
                            child.set('encoding', str(lic_data[key]['encoding']))
                    else:
                        child.text = str(lic_data[key])
                    wrapper.append(child)

            parent.append(wrapper)

    def _data_classification_to_xml(self, dc_data: dict, parent: XmlElement, xmlns: str) -> None:
        """Convert a DataClassification dict to XML with flow as attribute."""
        def ns_tag(n): return f'{{{xmlns}}}{n}'
        elem = XmlElement(ns_tag('classification'))

        if 'flow' in dc_data:
            elem.set('flow', str(dc_data['flow']))
        if 'classification' in dc_data:
            elem.text = str(dc_data['classification'])

        parent.append(elem)

    def _attached_text_to_xml(self, text_data: dict, parent: XmlElement, xmlns: str) -> None:
        """Convert an AttachedText dict to XML with attributes and text content."""
        def ns_tag(n): return f'{{{xmlns}}}{n}'
        elem = XmlElement(ns_tag('text'))

        # Set attributes
        if 'contentType' in text_data and text_data['contentType']:
            elem.set('content-type', str(text_data['contentType']))
        if 'encoding' in text_data and text_data['encoding']:
            elem.set('encoding', str(text_data['encoding']))

        # Set text content
        if 'content' in text_data and text_data['content']:
            elem.text = str(text_data['content'])

        parent.append(elem)

    def generate(self, force_regeneration: bool = False) -> None:
        if self.generated and not force_regeneration:
            return

        bom = self.get_bom()
        bom.validate()
        xmlns = self.get_target_namespace()

        with BomRefDiscriminator.from_bom(bom):
            xml_elem = self._bom_to_xml(bom, xmlns)
            # Register the namespace as empty prefix so it becomes the default
            from xml.etree.ElementTree import register_namespace
            register_namespace('', xmlns)
            self._bom_xml = '<?xml version="1.0" ?>\n' + xml_dumps(
                xml_elem,
                method='xml', encoding='unicode',
                xml_declaration=False)

        self.generated = True

    @staticmethod
    def __make_indent(v: Optional[Union[int, str]]) -> str:
        if isinstance(v, int):
            return ' ' * v
        if isinstance(v, str):
            return v
        return ''

    def output_as_string(self, *,
                         indent: Optional[Union[int, str]] = None,
                         **kwargs: Any) -> str:
        self.generate()
        return self._bom_xml if indent is None else dom_parseString(  # nosec B318
            self._bom_xml).toprettyxml(
            indent=self.__make_indent(indent)
            # do not set `encoding` - this would convert result to binary, not string
        )

    def get_target_namespace(self) -> str:
        return f'http://cyclonedx.org/schema/bom/{self.get_schema_version()}'


class XmlV1Dot0(Xml, SchemaVersion1Dot0):

    def _create_bom_element(self) -> XmlElement:
        return XmlElement('bom', {'xmlns': self.get_target_namespace(), 'version': '1'})


class XmlV1Dot1(Xml, SchemaVersion1Dot1):
    pass


class XmlV1Dot2(Xml, SchemaVersion1Dot2):
    pass


class XmlV1Dot3(Xml, SchemaVersion1Dot3):
    pass


class XmlV1Dot4(Xml, SchemaVersion1Dot4):
    pass


class XmlV1Dot5(Xml, SchemaVersion1Dot5):
    pass


class XmlV1Dot6(Xml, SchemaVersion1Dot6):
    pass


class XmlV1Dot7(Xml, SchemaVersion1Dot7):
    pass


BY_SCHEMA_VERSION: dict[SchemaVersion, type[Xml]] = {
    SchemaVersion.V1_7: XmlV1Dot7,
    SchemaVersion.V1_6: XmlV1Dot6,
    SchemaVersion.V1_5: XmlV1Dot5,
    SchemaVersion.V1_4: XmlV1Dot4,
    SchemaVersion.V1_3: XmlV1Dot3,
    SchemaVersion.V1_2: XmlV1Dot2,
    SchemaVersion.V1_1: XmlV1Dot1,
    SchemaVersion.V1_0: XmlV1Dot0,
}
