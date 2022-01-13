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

import warnings
from typing import List, Optional
from xml.etree import ElementTree

from . import BaseOutput
from .schema import BaseSchemaVersion, SchemaVersion1Dot0, SchemaVersion1Dot1, SchemaVersion1Dot2, SchemaVersion1Dot3, \
    SchemaVersion1Dot4
from ..exception.output import ComponentVersionRequiredException
from ..model import ExternalReference, HashType, OrganizationalEntity, OrganizationalContact, Tool
from ..model.bom import Bom
from ..model.component import Component
from ..model.vulnerability import Vulnerability, VulnerabilityRating, VulnerabilitySource, BomTargetVersionRange


class Xml(BaseOutput, BaseSchemaVersion):
    VULNERABILITY_EXTENSION_NAMESPACE: str = 'http://cyclonedx.org/schema/ext/vulnerability/1.0'
    XML_VERSION_DECLARATION: str = '<?xml version="1.0" encoding="UTF-8"?>'

    def __init__(self, bom: Bom) -> None:
        super().__init__(bom=bom)
        self._root_bom_element: ElementTree.Element = self._create_bom_element()

    def generate(self, force_regeneration: bool = False) -> None:
        if self.generated and force_regeneration:
            self._root_bom_element = self._create_bom_element()
        elif self.generated:
            return

        if self.bom_supports_metadata():
            self._add_metadata_element()

        components_element = ElementTree.SubElement(self._root_bom_element, 'components')

        has_vulnerabilities: bool = False
        for component in self.get_bom().components:
            component_element = self._add_component_element(component=component)
            components_element.append(component_element)
            if self.bom_supports_vulnerabilities_via_extension() and component.has_vulnerabilities():
                # Vulnerabilities are only possible when bom-ref is supported by the main CycloneDX schema version
                vulnerabilities = ElementTree.SubElement(component_element, 'v:vulnerabilities')
                for vulnerability in component.get_vulnerabilities():
                    if component.bom_ref:
                        vulnerabilities.append(
                            self._get_vulnerability_as_xml_element_pre_1_3(bom_ref=component.bom_ref,
                                                                           vulnerability=vulnerability)
                        )
                    else:
                        warnings.warn(
                            f'Unable to include Vulnerability {str(vulnerability)} in generated BOM as the Component'
                            f'it relates to ({str(component)}) but it has no bom-ref.'
                        )
            elif component.has_vulnerabilities():
                has_vulnerabilities = True

        if self.bom_supports_vulnerabilities() and has_vulnerabilities:
            vulnerabilities_element = ElementTree.SubElement(self._root_bom_element, 'vulnerabilities')
            for component in self.get_bom().components:
                for vulnerability in component.get_vulnerabilities():
                    vulnerabilities_element.append(
                        self._get_vulnerability_as_xml_element_post_1_4(vulnerability=vulnerability)
                    )

        self.generated = True

    def output_as_string(self) -> str:
        self.generate()
        return Xml.XML_VERSION_DECLARATION + ElementTree.tostring(self._root_bom_element, 'unicode')

    def get_target_namespace(self) -> str:
        return f'http://cyclonedx.org/schema/bom/{self.get_schema_version()}'

    # Builder Methods
    def _create_bom_element(self) -> ElementTree.Element:
        root_attributes = {
            'xmlns': self.get_target_namespace(),
            'version': '1',
            'serialNumber': self.get_bom().get_urn_uuid()
        }

        if self.bom_supports_vulnerabilities_via_extension() and self.get_bom().has_vulnerabilities():
            root_attributes['xmlns:v'] = Xml.VULNERABILITY_EXTENSION_NAMESPACE
            ElementTree.register_namespace('v', Xml.VULNERABILITY_EXTENSION_NAMESPACE)

        return ElementTree.Element('bom', root_attributes)

    def _add_metadata_element(self) -> None:
        bom_metadata = self.get_bom().metadata
        metadata_e = ElementTree.SubElement(self._root_bom_element, 'metadata')

        ElementTree.SubElement(metadata_e, 'timestamp').text = bom_metadata.timestamp.isoformat()

        if self.bom_metadata_supports_tools() and len(bom_metadata.tools) > 0:
            tools_e = ElementTree.SubElement(metadata_e, 'tools')
            for tool in bom_metadata.tools:
                self._add_tool(parent_element=tools_e, tool=tool)

        if bom_metadata.component:
            metadata_e.append(self._add_component_element(component=bom_metadata.component))

    def _add_component_element(self, component: Component) -> ElementTree.Element:
        element_attributes = {'type': component.type.value}
        if self.component_supports_bom_ref_attribute() and component.bom_ref:
            element_attributes['bom-ref'] = component.bom_ref
        if self.component_supports_mime_type_attribute() and component.mime_type:
            element_attributes['mime-type'] = component.mime_type

        component_element = ElementTree.Element('component', element_attributes)

        if self.component_supports_author() and component.author is not None:
            ElementTree.SubElement(component_element, 'author').text = component.author

        # group
        if component.group:
            ElementTree.SubElement(component_element, 'group').text = component.group

        # name
        ElementTree.SubElement(component_element, 'name').text = component.name

        # version
        if self.component_version_optional():
            if component.version:
                # 1.4 schema version
                ElementTree.SubElement(component_element, 'version').text = component.version
        else:
            if not component.version:
                raise ComponentVersionRequiredException(
                    f'Component "{str(component)}" has no version but the target schema version mandates '
                    f'Components have a version specified'
                )
            ElementTree.SubElement(component_element, 'version').text = component.version

        # hashes
        if component.hashes:
            Xml._add_hashes_to_element(hashes=component.hashes, element=component_element)

        # licenses
        if component.licenses:
            licenses_e = ElementTree.SubElement(component_element, 'licenses')
            for license in component.licenses:
                if license.license:
                    license_e = ElementTree.SubElement(licenses_e, 'license')
                    if license.license.id:
                        ElementTree.SubElement(license_e, 'id').text = license.license.id
                    elif license.license.name:
                        ElementTree.SubElement(license_e, 'name').text = license.license.name
                    if license.license.text:
                        license_text_e_attrs = {}
                        if license.license.text.content_type:
                            license_text_e_attrs['content-type'] = license.license.text.content_type
                        if license.license.text.encoding:
                            license_text_e_attrs['encoding'] = license.license.text.encoding.value
                        ElementTree.SubElement(license_e, 'text',
                                               license_text_e_attrs).text = license.license.text.content

                        ElementTree.SubElement(license_e, 'text').text = license.license.id
                else:
                    ElementTree.SubElement(licenses_e, 'expression').text = license.expression

        # purl
        if component.purl:
            ElementTree.SubElement(component_element, 'purl').text = component.purl.to_string()

        # modified
        if self.bom_requires_modified():
            ElementTree.SubElement(component_element, 'modified').text = 'false'

        # externalReferences
        if self.component_supports_external_references() and len(component.external_references) > 0:
            external_references_e = ElementTree.SubElement(component_element, 'externalReferences')
            for ext_ref in component.external_references:
                external_reference_e = ElementTree.SubElement(
                    external_references_e, 'reference', {'type': ext_ref.get_reference_type().value}
                )
                ElementTree.SubElement(external_reference_e, 'url').text = ext_ref.get_url()

                if ext_ref.get_comment():
                    ElementTree.SubElement(external_reference_e, 'comment').text = ext_ref.get_comment()

                if len(ext_ref.get_hashes()) > 0:
                    Xml._add_hashes_to_element(hashes=ext_ref.get_hashes(), element=external_reference_e)

        # releaseNotes
        if self.component_supports_release_notes() and component.release_notes:
            release_notes_e = ElementTree.SubElement(component_element, 'releaseNotes')
            release_notes = component.release_notes

            ElementTree.SubElement(release_notes_e, 'type').text = release_notes.type
            if release_notes.title:
                ElementTree.SubElement(release_notes_e, 'title').text = release_notes.title
            if release_notes.featured_image:
                ElementTree.SubElement(release_notes_e,
                                       'featuredImage').text = str(release_notes.featured_image)
            if release_notes.social_image:
                ElementTree.SubElement(release_notes_e,
                                       'socialImage').text = str(release_notes.social_image)
            if release_notes.description:
                ElementTree.SubElement(release_notes_e,
                                       'description').text = release_notes.description
            if release_notes.timestamp:
                ElementTree.SubElement(release_notes_e, 'timestamp').text = release_notes.timestamp.isoformat()
            if release_notes.aliases:
                release_notes_aliases_e = ElementTree.SubElement(release_notes_e, 'aliases')
                for alias in release_notes.aliases:
                    ElementTree.SubElement(release_notes_aliases_e, 'alias').text = alias
            if release_notes.tags:
                release_notes_tags_e = ElementTree.SubElement(release_notes_e, 'tags')
                for tag in release_notes.tags:
                    ElementTree.SubElement(release_notes_tags_e, 'tag').text = tag
            if release_notes.resolves:
                release_notes_resolves_e = ElementTree.SubElement(release_notes_e, 'resolves')
                for issue in release_notes.resolves:
                    issue_e = ElementTree.SubElement(
                        release_notes_resolves_e, 'issue', {'type': issue.get_classification().value}
                    )
                    if issue.get_id():
                        ElementTree.SubElement(issue_e, 'id').text = issue.get_id()
                    if issue.get_name():
                        ElementTree.SubElement(issue_e, 'name').text = issue.get_name()
                    if issue.get_description():
                        ElementTree.SubElement(issue_e, 'description').text = issue.get_description()
                    if issue.source:
                        issue_source_e = ElementTree.SubElement(issue_e, 'source')
                        if issue.source.name:
                            ElementTree.SubElement(issue_source_e, 'name').text = issue.source.name
                        if issue.source.url:
                            ElementTree.SubElement(issue_source_e, 'url').text = str(issue.source.url)
                    if issue.get_references():
                        issue_references_e = ElementTree.SubElement(issue_e, 'references')
                        for reference in issue.get_references():
                            ElementTree.SubElement(issue_references_e, 'url').text = str(reference)
            if release_notes.notes:
                release_notes_notes_e = ElementTree.SubElement(release_notes_e, 'notes')
                for note in release_notes.notes:
                    note_e = ElementTree.SubElement(release_notes_notes_e, 'note')
                    if note.locale:
                        ElementTree.SubElement(note_e, 'locale').text = note.locale
                    text_attrs = {}
                    if note.text.content_type:
                        text_attrs['content-type'] = note.text.content_type
                    if note.text.encoding:
                        text_attrs['encoding'] = note.text.encoding.value
                    ElementTree.SubElement(note_e, 'text', text_attrs).text = note.text.content
            if release_notes.properties:
                release_notes_properties_e = ElementTree.SubElement(release_notes_e, 'properties')
                for prop in release_notes.properties:
                    ElementTree.SubElement(
                        release_notes_properties_e, 'property', {'name': prop.get_name()}
                    ).text = prop.get_value()

        return component_element

    def _get_vulnerability_as_xml_element_post_1_4(self, vulnerability: Vulnerability) -> ElementTree.Element:
        vulnerability_element = ElementTree.Element(
            'vulnerability',
            {'bom-ref': vulnerability.bom_ref} if vulnerability.bom_ref else {}
        )

        # id
        if vulnerability.id:
            ElementTree.SubElement(vulnerability_element, 'id').text = vulnerability.id

        # source
        Xml._add_vulnerability_source(parent_element=vulnerability_element, source=vulnerability.source)

        # references
        if vulnerability.references:
            v_references_element = ElementTree.SubElement(vulnerability_element, 'references')
            for reference in vulnerability.references:
                v_reference_element = ElementTree.SubElement(v_references_element, 'reference')
                if reference.id:
                    ElementTree.SubElement(v_reference_element, 'id').text = reference.id
                Xml._add_vulnerability_source(parent_element=v_reference_element, source=reference.source)

        # ratings
        if vulnerability.ratings:
            v_ratings_element = ElementTree.SubElement(vulnerability_element, 'ratings')
            for rating in vulnerability.ratings:
                v_rating_element = ElementTree.SubElement(v_ratings_element, 'rating')
                Xml._add_vulnerability_source(parent_element=v_rating_element, source=rating.source)
                if rating.score:
                    ElementTree.SubElement(v_rating_element, 'score').text = f'{rating.score:.1f}'
                if rating.severity:
                    ElementTree.SubElement(v_rating_element, 'severity').text = rating.severity.value
                if rating.method:
                    ElementTree.SubElement(v_rating_element, 'method').text = rating.method.value
                if rating.vector:
                    ElementTree.SubElement(v_rating_element, 'vector').text = rating.vector
                if rating.justification:
                    ElementTree.SubElement(v_rating_element, 'justification').text = rating.justification

        # cwes
        if vulnerability.cwes:
            v_cwes_element = ElementTree.SubElement(vulnerability_element, 'cwes')
            for cwe in vulnerability.cwes:
                ElementTree.SubElement(v_cwes_element, 'cwe').text = str(cwe)

        # description
        if vulnerability.description:
            ElementTree.SubElement(vulnerability_element, 'description').text = vulnerability.description

        # detail
        if vulnerability.detail:
            ElementTree.SubElement(vulnerability_element, 'detail').text = vulnerability.detail

        # recommendation
        if vulnerability.recommendation:
            ElementTree.SubElement(vulnerability_element, 'recommendation').text = vulnerability.recommendation

        # advisories
        if vulnerability.advisories:
            v_advisories_element = ElementTree.SubElement(vulnerability_element, 'advisories')
            for advisory in vulnerability.advisories:
                v_advisory_element = ElementTree.SubElement(v_advisories_element, 'advisory')
                if advisory.title:
                    ElementTree.SubElement(v_advisory_element, 'title').text = advisory.title
                ElementTree.SubElement(v_advisory_element, 'url').text = str(advisory.url)

        # created
        if vulnerability.created:
            ElementTree.SubElement(vulnerability_element, 'created').text = vulnerability.created.isoformat()

        # published
        if vulnerability.published:
            ElementTree.SubElement(vulnerability_element, 'published').text = vulnerability.published.isoformat()

        # updated
        if vulnerability.updated:
            ElementTree.SubElement(vulnerability_element, 'updated').text = vulnerability.updated.isoformat()

        # credits
        if vulnerability.credits:
            v_credits_element = ElementTree.SubElement(vulnerability_element, 'credits')
            if vulnerability.credits.organizations:
                v_credits_organizations_element = ElementTree.SubElement(v_credits_element, 'organizations')
                for organization in vulnerability.credits.organizations:
                    Xml._add_organizational_entity(
                        parent_element=v_credits_organizations_element, organization=organization,
                        tag_name='organization'
                    )
            if vulnerability.credits.individuals:
                v_credits_individuals_element = ElementTree.SubElement(v_credits_element, 'individuals')
                for individual in vulnerability.credits.individuals:
                    Xml._add_organizational_contact(
                        parent_element=v_credits_individuals_element, contact=individual,
                        tag_name='individual'
                    )

        # tools
        if vulnerability.tools:
            v_tools_element = ElementTree.SubElement(vulnerability_element, 'tools')
            for tool in vulnerability.tools:
                self._add_tool(parent_element=v_tools_element, tool=tool)

        # analysis
        if vulnerability.analysis:
            v_analysis_element = ElementTree.SubElement(vulnerability_element, 'analysis')
            if vulnerability.analysis.state:
                ElementTree.SubElement(v_analysis_element, 'state').text = vulnerability.analysis.state.value
            if vulnerability.analysis.justification:
                ElementTree.SubElement(v_analysis_element,
                                       'justification').text = vulnerability.analysis.justification.value
            if vulnerability.analysis.response:
                v_analysis_responses_element = ElementTree.SubElement(v_analysis_element, 'responses')
                for response in vulnerability.analysis.response:
                    ElementTree.SubElement(v_analysis_responses_element, 'response').text = response.value
            if vulnerability.analysis.detail:
                ElementTree.SubElement(v_analysis_element, 'detail').text = vulnerability.analysis.detail

        # affects
        if vulnerability.affects:
            v_affects_element = ElementTree.SubElement(vulnerability_element, 'affects')
            for target in vulnerability.affects:
                v_target_element = ElementTree.SubElement(v_affects_element, 'target')
                ElementTree.SubElement(v_target_element, 'ref').text = target.ref

                if target.versions:
                    v_target_versions_element = ElementTree.SubElement(v_target_element, 'versions')
                    for version in target.versions:
                        Xml._add_bom_target_version_range(parent_element=v_target_versions_element, version=version)

        return vulnerability_element

    def _get_vulnerability_as_xml_element_pre_1_3(self, bom_ref: str,
                                                  vulnerability: Vulnerability) -> ElementTree.Element:
        vulnerability_element = ElementTree.Element('v:vulnerability', {
            'ref': bom_ref
        })

        # id
        ElementTree.SubElement(vulnerability_element, 'v:id').text = vulnerability.id

        # source
        if vulnerability.source and vulnerability.source.name:
            source_element = ElementTree.SubElement(
                vulnerability_element, 'v:source', attrib={'name': str(vulnerability.source.name)}
            )
            if vulnerability.source.url:
                ElementTree.SubElement(source_element, 'v:url').text = str(vulnerability.source.url)

        # ratings
        if vulnerability.ratings:
            ratings_element = ElementTree.SubElement(vulnerability_element, 'v:ratings')
            rating: VulnerabilityRating
            for rating in vulnerability.ratings:
                rating_element = ElementTree.SubElement(ratings_element, 'v:rating')

                if rating.score:
                    score_element = ElementTree.SubElement(rating_element, 'v:score')
                    ElementTree.SubElement(score_element, 'v:base').text = f'{rating.score:.1f}'

                # rating.severity
                if rating.severity:
                    ElementTree.SubElement(rating_element, 'v:severity').text = str(rating.severity.value).title()

                # rating.severity
                if rating.method:
                    ElementTree.SubElement(rating_element, 'v:method').text = rating.method.get_value_pre_1_4()

                # rating.vector
                if rating.vector:
                    ElementTree.SubElement(rating_element, 'v:vector').text = rating.vector

        # cwes
        if vulnerability.cwes:
            cwes_element = ElementTree.SubElement(vulnerability_element, 'v:cwes')
            for cwe in vulnerability.cwes:
                ElementTree.SubElement(cwes_element, 'v:cwe').text = str(cwe)

        # description
        if vulnerability.description:
            ElementTree.SubElement(vulnerability_element, 'v:description').text = vulnerability.description

        # recommendations
        if vulnerability.recommendation:
            recommendations_element = ElementTree.SubElement(vulnerability_element, 'v:recommendations')
            # for recommendation in vulnerability.get_recommendations():
            ElementTree.SubElement(recommendations_element, 'v:recommendation').text = vulnerability.recommendation

        # advisories
        if vulnerability.advisories:
            advisories_element = ElementTree.SubElement(vulnerability_element, 'v:advisories')
            for advisory in vulnerability.advisories:
                ElementTree.SubElement(advisories_element, 'v:advisory').text = str(advisory.url)

        return vulnerability_element

    @staticmethod
    def _add_external_references_to_element(ext_refs: List[ExternalReference], element: ElementTree.Element) -> None:
        ext_refs_element = ElementTree.SubElement(element, 'externalReferences')
        for external_reference in ext_refs:
            ext_ref_element = ElementTree.SubElement(
                ext_refs_element, 'reference', {'type': external_reference.get_reference_type().value}
            )
            ElementTree.SubElement(ext_ref_element, 'url').text = external_reference.get_url()
            if external_reference.get_comment():
                ElementTree.SubElement(ext_ref_element, 'comment').text = external_reference.get_comment()
            if external_reference.get_hashes():
                Xml._add_hashes_to_element(hashes=external_reference.get_hashes(), element=ext_ref_element)

    @staticmethod
    def _add_hashes_to_element(hashes: List[HashType], element: ElementTree.Element) -> None:
        hashes_e = ElementTree.SubElement(element, 'hashes')
        for h in hashes:
            ElementTree.SubElement(
                hashes_e, 'hash', {'alg': h.get_algorithm().value}
            ).text = h.get_hash_value()

    @staticmethod
    def _add_bom_target_version_range(parent_element: ElementTree.Element, version: BomTargetVersionRange) -> None:
        version_element = ElementTree.SubElement(parent_element, 'version')
        if version.version:
            ElementTree.SubElement(version_element, 'version').text = version.version
        else:
            ElementTree.SubElement(version_element, 'range').text = version.range

        if version.status:
            ElementTree.SubElement(version_element, 'status').text = version.status.value

    def _add_tool(self, parent_element: ElementTree.Element, tool: Tool, tag_name: str = 'tool') -> None:
        tool_element = ElementTree.SubElement(parent_element, tag_name)
        if tool.get_vendor():
            ElementTree.SubElement(tool_element, 'vendor').text = tool.get_vendor()
        if tool.get_name():
            ElementTree.SubElement(tool_element, 'name').text = tool.get_name()
        if tool.get_version():
            ElementTree.SubElement(tool_element, 'version').text = tool.get_version()
        if tool.get_hashes():
            Xml._add_hashes_to_element(hashes=tool.get_hashes(), element=tool_element)
        if self.bom_metadata_supports_tools_external_references() and tool.get_external_references():
            Xml._add_external_references_to_element(
                ext_refs=tool.get_external_references(), element=tool_element
            )

    @staticmethod
    def _add_organizational_contact(parent_element: ElementTree.Element, contact: OrganizationalContact,
                                    tag_name: str) -> None:
        oc_element = ElementTree.SubElement(parent_element, tag_name)
        if contact.name:
            ElementTree.SubElement(oc_element, 'name').text = contact.name
        if contact.email:
            ElementTree.SubElement(oc_element, 'email').text = contact.email
        if contact.phone:
            ElementTree.SubElement(oc_element, 'phone').text = contact.phone

    @staticmethod
    def _add_organizational_entity(parent_element: ElementTree.Element, organization: OrganizationalEntity,
                                   tag_name: str) -> None:
        oe_element = ElementTree.SubElement(parent_element, tag_name)
        if organization.name:
            ElementTree.SubElement(oe_element, 'name').text = organization.name
        if organization.urls:
            for url in organization.urls:
                ElementTree.SubElement(oe_element, 'url').text = str(url)
        if organization.contacts:
            for contact in organization.contacts:
                Xml._add_organizational_contact(parent_element=oe_element, contact=contact, tag_name='contact')

    @staticmethod
    def _add_vulnerability_source(parent_element: ElementTree.Element,
                                  source: Optional[VulnerabilitySource] = None) -> None:
        if source:
            v_source_element = ElementTree.SubElement(parent_element, 'source')
            if source.name:
                ElementTree.SubElement(v_source_element, 'name').text = source.name
            if source.url:
                ElementTree.SubElement(v_source_element, 'url').text = str(source.url)


class XmlV1Dot0(Xml, SchemaVersion1Dot0):

    def _create_bom_element(self) -> ElementTree.Element:
        return ElementTree.Element('bom', {'xmlns': self.get_target_namespace(), 'version': '1'})


class XmlV1Dot1(Xml, SchemaVersion1Dot1):
    pass


class XmlV1Dot2(Xml, SchemaVersion1Dot2):
    pass


class XmlV1Dot3(Xml, SchemaVersion1Dot3):
    pass


class XmlV1Dot4(Xml, SchemaVersion1Dot4):
    pass
