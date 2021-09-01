from abc import abstractmethod
from xml.etree import ElementTree

from . import BaseOutput
from ..model.cyclonedx import Component


def _xml_pretty_print(elem: ElementTree.Element, level: int = 0) -> ElementTree.Element:
    """
    Helper method lifed from cyclonedx-python original project for formatting
    XML without using any XML-libraries.

    NOTE: This method is recursive.

    :param elem:
    :param level:
    :return:
    """
    i = "\n" + level * "    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            _xml_pretty_print(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
    return elem


class Xml(BaseOutput):
    XML_VERSION_DECLARATION: str = '<?xml version="1.0" encoding="UTF-8"?>'

    def get_target_namespace(self) -> str:
        return 'http://cyclonedx.org/schema/bom/{}'.format(self._get_schema_version())

    def output_as_string(self) -> str:
        bom = self._get_bom_root_element()

        if self._bom_supports_metadata():
            bom = self._add_metadata(bom=bom)

        components = ElementTree.SubElement(bom, 'components')
        for component in self.get_bom().get_components():
            components.append(self._get_component_as_xml_element(component=component))

        return Xml.XML_VERSION_DECLARATION + ElementTree.tostring(bom, 'unicode')

    def output_to_file(self, filename: str):
        pass

    def _get_bom_root_element(self) -> ElementTree.Element:
        return ElementTree.Element('bom', {'xmlns': self.get_target_namespace(), 'version': '1',
                                           'serialNumber': self.get_bom().get_urn_uuid()})

    def _get_component_as_xml_element(self, component: Component) -> ElementTree.Element:
        element_attributes = {'type': component.get_type().value}
        if self._component_supports_bom_ref_attribute():
            element_attributes['bom-ref'] = component.get_purl()

        component_element = ElementTree.Element('component', element_attributes)

        if self._component_supports_author() and component.get_author() is not None:
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

    def _bom_supports_metadata(self) -> bool:
        return True

    def _component_supports_author(self) -> bool:
        return True

    def _component_supports_bom_ref_attribute(self) -> bool:
        return True

    @abstractmethod
    def _get_schema_version(self) -> str:
        pass


class XmlV1Dot0(Xml):

    def _get_bom_root_element(self) -> ElementTree.Element:
        return ElementTree.Element('bom', {'xmlns': self.get_target_namespace(), 'version': '1'})

    def _get_schema_version(self) -> str:
        return '1.0'

    def _bom_supports_metadata(self) -> bool:
        return False

    def _component_supports_bom_ref_attribute(self) -> bool:
        return False

    def _component_supports_author(self) -> bool:
        return False


class XmlV1Dot1(Xml):

    def _get_schema_version(self) -> str:
        return '1.1'

    def _bom_supports_metadata(self) -> bool:
        return False

    def _component_supports_author(self) -> bool:
        return False


class XmlV1Dot2(Xml):

    def _get_schema_version(self) -> str:
        return '1.2'


class XmlV1Dot3(Xml):

    def _get_schema_version(self) -> str:
        return '1.3'
