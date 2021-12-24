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

from typing import cast, List
from urllib.parse import ParseResult
from xml.etree import ElementTree

from . import BaseOutput
from .schema import BaseSchemaVersion, SchemaVersion1Dot0, SchemaVersion1Dot1, SchemaVersion1Dot2, SchemaVersion1Dot3, \
    SchemaVersion1Dot4
from ..exception.output import ComponentVersionRequiredException
from ..model import ExternalReference, HashType
from ..model.component import Component
from ..model.vulnerability import Vulnerability, VulnerabilityRating, VulnerabilitySeverity, VulnerabilityScoreSource


class Xml(BaseOutput, BaseSchemaVersion):
    XML_VERSION_DECLARATION: str = '<?xml version="1.0" encoding="UTF-8"?>'

    def get_target_namespace(self) -> str:
        return 'http://cyclonedx.org/schema/bom/{}'.format(self.get_schema_version())

    @staticmethod
    def get_vulnerabilities_namespace() -> str:
        return 'http://cyclonedx.org/schema/ext/vulnerability/1.0'

    def output_as_string(self) -> str:
        bom = self._get_bom_root_element()

        if self.bom_supports_metadata():
            bom = self._add_metadata(bom=bom)

        if self.get_bom().has_vulnerabilities():
            ElementTree.register_namespace('v', Xml.get_vulnerabilities_namespace())

        components = ElementTree.SubElement(bom, 'components')

        for component in self.get_bom().get_components():
            component_element = self._get_component_as_xml_element(component=component)
            components.append(component_element)
            if component.has_vulnerabilities() and self.component_supports_bom_ref():
                # Vulnerabilities are only possible when bom-ref is supported by the main CycloneDX schema version
                vulnerabilities = ElementTree.SubElement(component_element, 'v:vulnerabilities')
                for vulnerability in component.get_vulnerabilities():
                    vulnerabilities.append(self._get_vulnerability_as_xml_element(bom_ref=component.get_purl(),
                                                                                  vulnerability=vulnerability))

        return Xml.XML_VERSION_DECLARATION + ElementTree.tostring(bom, 'unicode')

    def _component_supports_bom_ref_attribute(self) -> bool:
        return True

    def _get_bom_root_element(self) -> ElementTree.Element:
        root_attributes = {
            'xmlns': self.get_target_namespace(),
            'version': '1',
            'serialNumber': self.get_bom().get_urn_uuid()
        }

        if self.get_bom().has_vulnerabilities():
            root_attributes['xmlns:v'] = Xml.get_vulnerabilities_namespace()

        return ElementTree.Element('bom', root_attributes)

    def _get_component_as_xml_element(self, component: Component) -> ElementTree.Element:
        element_attributes = {'type': component.get_type().value}
        if self.component_supports_bom_ref():
            element_attributes['bom-ref'] = component.get_purl()

        component_element = ElementTree.Element('component', element_attributes)

        if self.component_supports_author() and component.get_author() is not None:
            ElementTree.SubElement(component_element, 'author').text = component.get_author()

        # group
        if component.get_namespace():
            ElementTree.SubElement(component_element, 'group').text = component.get_namespace()

        # name
        ElementTree.SubElement(component_element, 'name').text = component.get_name()

        # version
        if self.component_version_optional():
            if component.get_version():
                # 1.4 schema version
                ElementTree.SubElement(component_element, 'version').text = component.get_version()
        else:
            if not component.get_version():
                raise ComponentVersionRequiredException(
                    f'Component "{component.get_purl()}" has no version but the target schema version mandates '
                    f'Components have a version specified'
                )
            ElementTree.SubElement(component_element, 'version').text = component.get_version()

        # hashes
        if len(component.get_hashes()) > 0:
            Xml._add_hashes_to_element(hashes=component.get_hashes(), element=component_element)

        # licenses
        if component.get_license():
            licenses_e = ElementTree.SubElement(component_element, 'licenses')
            license_e = ElementTree.SubElement(licenses_e, 'license')
            ElementTree.SubElement(license_e, 'name').text = component.get_license()

        # purl
        ElementTree.SubElement(component_element, 'purl').text = component.get_purl()

        # modified
        if self.bom_requires_modified():
            ElementTree.SubElement(component_element, 'modified').text = 'false'

        # externalReferences
        if self.component_supports_external_references() and len(component.get_external_references()) > 0:
            external_references_e = ElementTree.SubElement(component_element, 'externalReferences')
            for ext_ref in component.get_external_references():
                external_reference_e = ElementTree.SubElement(
                    external_references_e, 'reference', {'type': ext_ref.get_reference_type().value}
                )
                ElementTree.SubElement(external_reference_e, 'url').text = ext_ref.get_url()

                if ext_ref.get_comment():
                    ElementTree.SubElement(external_reference_e, 'comment').text = ext_ref.get_comment()

                if len(ext_ref.get_hashes()) > 0:
                    Xml._add_hashes_to_element(hashes=ext_ref.get_hashes(), element=external_reference_e)

        # releaseNotes
        if self.component_supports_release_notes() and component.get_release_notes():
            release_notes_e = ElementTree.SubElement(component_element, 'releaseNotes')
            ElementTree.SubElement(release_notes_e, 'type').text = component.get_release_notes().get_type()
            if component.get_release_notes().get_title():
                ElementTree.SubElement(release_notes_e, 'title').text = component.get_release_notes().get_title()
            if component.get_release_notes().get_featured_image():
                ElementTree.SubElement(release_notes_e,
                                       'featuredImage').text = str(component.get_release_notes().get_featured_image())
            if component.get_release_notes().get_social_image():
                ElementTree.SubElement(release_notes_e,
                                       'socialImage').text = str(component.get_release_notes().get_social_image())
            if component.get_release_notes().get_description():
                ElementTree.SubElement(release_notes_e,
                                       'description').text = component.get_release_notes().get_description()
            if component.get_release_notes().get_timestamp():
                ElementTree.SubElement(release_notes_e,
                                       'timestamp').text = component.get_release_notes().get_timestamp().isoformat()
            if component.get_release_notes().get_aliases():
                release_notes_aliases_e = ElementTree.SubElement(release_notes_e, 'aliases')
                for alias in component.get_release_notes().get_aliases():
                    ElementTree.SubElement(release_notes_aliases_e, 'alias').text = alias
            if component.get_release_notes().get_tags():
                release_notes_tags_e = ElementTree.SubElement(release_notes_e, 'tags')
                for tag in component.get_release_notes().get_tags():
                    ElementTree.SubElement(release_notes_tags_e, 'tag').text = tag
            if component.get_release_notes().get_resolves():
                release_notes_resolves_e = ElementTree.SubElement(release_notes_e, 'resolves')
                for issue in component.get_release_notes().get_resolves():
                    issue_e = ElementTree.SubElement(
                        release_notes_resolves_e, 'issue', {'type': issue.get_classification().value}
                    )
                    if issue.get_id():
                        ElementTree.SubElement(issue_e, 'id').text = issue.get_id()
                    if issue.get_name():
                        ElementTree.SubElement(issue_e, 'name').text = issue.get_name()
                    if issue.get_description():
                        ElementTree.SubElement(issue_e, 'description').text = issue.get_description()
                    if issue.get_source_name() or issue.get_source_url():
                        issue_source_e = ElementTree.SubElement(issue_e, 'source')
                        if issue.get_source_name():
                            ElementTree.SubElement(issue_source_e, 'name').text = issue.get_source_name()
                        if issue.get_source_url():
                            ElementTree.SubElement(issue_source_e, 'url').text = str(issue.get_source_url())
                    if issue.get_references():
                        issue_references_e = ElementTree.SubElement(issue_e, 'references')
                        for reference in issue.get_references():
                            ElementTree.SubElement(issue_references_e, 'url').text = str(reference)
            if component.get_release_notes().get_notes():
                release_notes_notes_e = ElementTree.SubElement(release_notes_e, 'notes')
                for note in component.get_release_notes().get_notes():
                    note_e = ElementTree.SubElement(release_notes_notes_e, 'note')
                    if note.get_locale():
                        ElementTree.SubElement(note_e, 'locale').text = note.get_locale()
                    text_attrs = {}
                    if note.get_content_type():
                        text_attrs['content-type'] = note.get_content_type()
                    if note.get_content_encoding():
                        text_attrs['encoding'] = note.get_content_encoding().value
                    ElementTree.SubElement(note_e, 'text', text_attrs).text = note.get_text()
            if component.get_release_notes().get_properties():
                release_notes_properties_e = ElementTree.SubElement(release_notes_e, 'properties')
                for prop in component.get_release_notes().get_properties().get_properties():
                    ElementTree.SubElement(
                        release_notes_properties_e, 'property', {'name': prop.get_name()}
                    ).text = prop.get_value()

        return component_element

    @staticmethod
    def _get_vulnerability_as_xml_element(bom_ref: str, vulnerability: Vulnerability) -> ElementTree.Element:
        vulnerability_element = ElementTree.Element('v:vulnerability', {
            'ref': bom_ref
        })

        # id
        ElementTree.SubElement(vulnerability_element, 'v:id').text = vulnerability.get_id()

        # source
        if vulnerability.get_source_name():
            source_element = ElementTree.SubElement(
                vulnerability_element, 'v:source', attrib={'name': str(vulnerability.get_source_name())}
            )
            if vulnerability.get_source_url():
                ElementTree.SubElement(source_element, 'v:url').text = str(
                    cast(ParseResult, vulnerability.get_source_url()).geturl()
                )

        # ratings
        if vulnerability.has_ratings():
            ratings_element = ElementTree.SubElement(vulnerability_element, 'v:ratings')
            rating: VulnerabilityRating
            for rating in vulnerability.get_ratings():
                rating_element = ElementTree.SubElement(ratings_element, 'v:rating')

                # rating.score
                if rating.has_score():
                    score_element = ElementTree.SubElement(rating_element, 'v:score')
                    if rating.get_base_score():
                        ElementTree.SubElement(score_element, 'v:base').text = str(rating.get_base_score())
                    if rating.get_impact_score():
                        ElementTree.SubElement(score_element, 'v:impact').text = str(rating.get_impact_score())
                    if rating.get_exploitability_score():
                        ElementTree.SubElement(score_element,
                                               'v:exploitability').text = str(rating.get_exploitability_score())

                # rating.severity
                if rating.get_severity():
                    ElementTree.SubElement(rating_element, 'v:severity').text = cast(
                        VulnerabilitySeverity, rating.get_severity()
                    ).value

                # rating.severity
                if rating.get_method():
                    ElementTree.SubElement(rating_element, 'v:method').text = cast(
                        VulnerabilityScoreSource, rating.get_method()
                    ).value

                # rating.vector
                if rating.get_vector():
                    ElementTree.SubElement(rating_element, 'v:vector').text = rating.get_vector()

        # cwes
        if vulnerability.has_cwes():
            cwes_element = ElementTree.SubElement(vulnerability_element, 'v:cwes')
            for cwe in vulnerability.get_cwes():
                ElementTree.SubElement(cwes_element, 'v:cwe').text = str(cwe)

        # description
        if vulnerability.get_description():
            ElementTree.SubElement(vulnerability_element, 'v:description').text = vulnerability.get_description()

        # recommendations
        if vulnerability.has_recommendations():
            recommendations_element = ElementTree.SubElement(vulnerability_element, 'v:recommendations')
            for recommendation in vulnerability.get_recommendations():
                ElementTree.SubElement(recommendations_element, 'v:recommendation').text = recommendation

        # advisories
        if vulnerability.has_advisories():
            advisories_element = ElementTree.SubElement(vulnerability_element, 'v:advisories')
            for advisory in vulnerability.get_advisories():
                ElementTree.SubElement(advisories_element, 'v:advisory').text = advisory

        return vulnerability_element

    def _add_metadata(self, bom: ElementTree.Element) -> ElementTree.Element:
        bom_metadata = self.get_bom().get_metadata()

        metadata_e = ElementTree.SubElement(bom, 'metadata')
        ElementTree.SubElement(metadata_e, 'timestamp').text = bom_metadata.get_timestamp().isoformat()

        if self.bom_metadata_supports_tools() and len(bom_metadata.get_tools()) > 0:
            tools_e = ElementTree.SubElement(metadata_e, 'tools')
            for tool in bom_metadata.get_tools():
                tool_e = ElementTree.SubElement(tools_e, 'tool')
                ElementTree.SubElement(tool_e, 'vendor').text = tool.get_vendor()
                ElementTree.SubElement(tool_e, 'name').text = tool.get_name()
                ElementTree.SubElement(tool_e, 'version').text = tool.get_version()
                if tool.get_hashes():
                    Xml._add_hashes_to_element(hashes=tool.get_hashes(), element=tool_e)
                if self.bom_metadata_supports_tools_external_references() and tool.get_external_references():
                    Xml._add_external_references_to_element(
                        ext_refs=tool.get_external_references(), element=tool_e
                    )

        return bom

    @staticmethod
    def _add_external_references_to_element(ext_refs: List[ExternalReference], element: ElementTree.Element) -> None:
        tool_ext_refs = ElementTree.SubElement(element, 'externalReferences')
        for ext_ref in ext_refs:
            tool_ext_ref = ElementTree.SubElement(
                tool_ext_refs, 'reference', {'type': ext_ref.get_reference_type().value}
            )
            ElementTree.SubElement(tool_ext_ref, 'url').text = ext_ref.get_url()
            if ext_ref.get_comment():
                ElementTree.SubElement(tool_ext_ref, 'comment').text = ext_ref.get_comment()
            if ext_ref.get_hashes():
                Xml._add_hashes_to_element(hashes=ext_ref.get_hashes(), element=tool_ext_ref)

    @staticmethod
    def _add_hashes_to_element(hashes: List[HashType], element: ElementTree.Element) -> None:
        hashes_e = ElementTree.SubElement(element, 'hashes')
        for h in hashes:
            ElementTree.SubElement(
                hashes_e, 'hash', {'alg': h.get_algorithm().value}
            ).text = h.get_hash_value()


class XmlV1Dot0(Xml, SchemaVersion1Dot0):

    def _get_bom_root_element(self) -> ElementTree.Element:
        return ElementTree.Element('bom', {'xmlns': self.get_target_namespace(), 'version': '1'})


class XmlV1Dot1(Xml, SchemaVersion1Dot1):
    pass


class XmlV1Dot2(Xml, SchemaVersion1Dot2):
    pass


class XmlV1Dot3(Xml, SchemaVersion1Dot3):
    pass


class XmlV1Dot4(Xml, SchemaVersion1Dot4):
    pass
