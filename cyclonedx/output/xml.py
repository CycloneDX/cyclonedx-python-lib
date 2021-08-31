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
    XML_VERSION_DECLARATION: str = '<?xml version="1.0" encoding="UTF-8"?>\n'

    def output_as_string(self) -> str:
        bom = ElementTree.Element('bom', {'xmlns': self._get_target_namespace(), 'version': self._get_schema_version()})
        components = ElementTree.SubElement(bom, 'components')
        for component in self.get_bom().get_components():
            components.append(Xml._get_component_as_xml_element(component=component))

        return Xml.XML_VERSION_DECLARATION + ElementTree.tostring(bom, 'unicode')

    def output_to_file(self, filename: str):
        pass

    @staticmethod
    def _get_component_as_xml_element(component: Component) -> ElementTree.Element:
        element = ElementTree.Element('component', {'type': component.get_type().value, 'bom-ref': component.get_purl()})

        # if publisher and publisher != "UNKNOWN":
        #     ElementTree.SubElement(component, "publisher").text = re.sub(RE_XML_ILLEGAL, "?", publisher)

        # if name and name != "UNKNOWN":
        ElementTree.SubElement(element, 'name').text = component.get_name()

        # if version and version != "UNKNOWN":
        ElementTree.SubElement(element, 'version').text = component.get_version()

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
        #             ElementTree.SubElement(license_elm, "name").text = re.sub(RE_XML_ILLEGAL, "?", component_license.license.name)

        # if purl:
        ElementTree.SubElement(element, 'purl').text = component.get_purl()

        # ElementTree.SubElement(component, "modified").text = modified if modified else "false"

        return element

    @abstractmethod
    def _get_schema_version(self) -> str:
        pass

    def _get_target_namespace(self) -> str:
        return 'http://cyclonedx.org/schema/bom/{}'.format(self._get_schema_version())


class XmlV1Dot2(Xml):

    def _get_schema_version(self) -> str:
        return '1.2'


class XmlV1Dot3(Xml):

    def _get_schema_version(self) -> str:
        return '1.3'
