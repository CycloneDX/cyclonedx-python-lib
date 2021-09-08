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

from xml.etree import ElementTree

from . import BaseOutput
from .schema import BaseSchemaVersion, SchemaVersion1Dot0, SchemaVersion1Dot1, SchemaVersion1Dot2, SchemaVersion1Dot3
from ..model.component import Component


class Xml(BaseOutput, BaseSchemaVersion):
    XML_VERSION_DECLARATION: str = '<?xml version="1.0" encoding="UTF-8"?>'

    def get_target_namespace(self) -> str:
        return 'http://cyclonedx.org/schema/bom/{}'.format(self.get_schema_version())

    def output_as_string(self) -> str:
        bom = self._get_bom_root_element()

        if self.bom_supports_metadata():
            bom = self._add_metadata(bom=bom)

        components = ElementTree.SubElement(bom, 'components')
        for component in self.get_bom().get_components():
            components.append(self._get_component_as_xml_element(component=component))

        return Xml.XML_VERSION_DECLARATION + ElementTree.tostring(bom, 'unicode')

    def _component_supports_bom_ref_attribute(self) -> bool:
        return True

    def _get_bom_root_element(self) -> ElementTree.Element:
        return ElementTree.Element('bom', {'xmlns': self.get_target_namespace(), 'version': '1',
                                           'serialNumber': self.get_bom().get_urn_uuid()})

    def _get_component_as_xml_element(self, component: Component) -> ElementTree.Element:
        element_attributes = {'type': component.get_type().value}
        if self.component_supports_bom_ref():
            element_attributes['bom-ref'] = component.get_purl()

        component_element = ElementTree.Element('component', element_attributes)

        if self.component_supports_author() and component.get_author() is not None:
            ElementTree.SubElement(component_element, 'author').text = component.get_author()

        # if publisher and publisher != "UNKNOWN":
        #     ElementTree.SubElement(component, "publisher").text = re.sub(RE_XML_ILLEGAL, "?", publisher)

        # if name and name != "UNKNOWN":
        ElementTree.SubElement(component_element, 'name').text = component.get_name()

        # if version and version != "UNKNOWN":
        ElementTree.SubElement(component_element, 'version').text = component.get_version()

        # if description and description != "UNKNOWN":
        #     ElementTree.SubElement(component, "description").text = re.sub(RE_XML_ILLEGAL, "?", description)
        #
        # if hashes:
        #     hashes_elm = ElementTree.SubElement(component, "hashes")
        #     for h in hashes:
        #         ElementTree.SubElement(hashes_elm, "hash", alg=h.alg).text = h.content
        #
        # if len(licenses):
        #     licenses_elm = ElementTree.SubElement(component, "licenses")
        #     for component_license in licenses:
        #         if component_license.license is not None:
        #             license_elm = ElementTree.SubElement(licenses_elm, "license")
        #             ElementTree.SubElement(license_elm, "name").text = re.sub(RE_XML_ILLEGAL, "?",
        #             component_license.license.name)

        # if purl:
        ElementTree.SubElement(component_element, 'purl').text = component.get_purl()

        # ElementTree.SubElement(component, "modified").text = modified if modified else "false"

        return component_element

    def _add_metadata(self, bom: ElementTree.Element) -> ElementTree.Element:
        metadata_e = ElementTree.SubElement(bom, 'metadata')
        ElementTree.SubElement(metadata_e, 'timestamp').text = self.get_bom().get_metadata().get_timestamp().isoformat()
        return bom


class XmlV1Dot0(Xml, SchemaVersion1Dot0):

    def _get_bom_root_element(self) -> ElementTree.Element:
        return ElementTree.Element('bom', {'xmlns': self.get_target_namespace(), 'version': '1'})


class XmlV1Dot1(Xml, SchemaVersion1Dot1):
    pass


class XmlV1Dot2(Xml, SchemaVersion1Dot2):
    pass


class XmlV1Dot3(Xml, SchemaVersion1Dot3):
    pass
