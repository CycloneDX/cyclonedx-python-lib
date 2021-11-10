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
from .schema import BaseSchemaVersion, SchemaVersion1Dot0, SchemaVersion1Dot1, SchemaVersion1Dot2, SchemaVersion1Dot3
from ..model import HashType
from ..model.component import Component
from ..model.vulnerability import Vulnerability, VulnerabilityRating, VulnerabilitySeverity, VulnerabilitySourceType


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
        ElementTree.SubElement(component_element, 'version').text = component.get_version()

        # hashes
        if len(component.get_hashes()) > 0:
            Xml._add_hashes_to_element(hashes=component.get_hashes(), element=component_element)

        # purl
        ElementTree.SubElement(component_element, 'purl').text = component.get_purl()

        # licenses
        if component.get_license():
            licenses_e = ElementTree.SubElement(component_element, 'licenses')
            license_e = ElementTree.SubElement(licenses_e, 'license')
            ElementTree.SubElement(license_e, 'name').text = component.get_license()

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
                        VulnerabilitySourceType, rating.get_method()
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
                if len(tool.get_hashes()) > 0:
                    hashes_e = ElementTree.SubElement(tool_e, 'hashes')
                    for hash_ in tool.get_hashes():
                        ElementTree.SubElement(hashes_e, 'hash',
                                               {'alg': hash_.get_algorithm().value}).text = hash_.get_hash_value()

        return bom

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
