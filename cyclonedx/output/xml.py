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


from typing import Dict, Optional, Type
from xml.etree import ElementTree

from ..exception.output import BomGenerationErrorException
from ..model.bom import Bom
from ..schema import OutputFormat, SchemaVersion
from ..schema.schema import (
    SCHEMA_VERSIONS,
    BaseSchemaVersion,
    SchemaVersion1Dot0,
    SchemaVersion1Dot1,
    SchemaVersion1Dot2,
    SchemaVersion1Dot3,
    SchemaVersion1Dot4,
)
from . import BaseOutput


class Xml(BaseSchemaVersion, BaseOutput):
    XML_VERSION_DECLARATION: str = '<?xml version="1.0" encoding="UTF-8"?>'

    def __init__(self, bom: Bom) -> None:
        super().__init__(bom=bom)
        self._root_bom_element: Optional[ElementTree.Element] = None

    @property
    def schema_version(self) -> SchemaVersion:
        return self.schema_version_enum

    @property
    def output_format(self) -> OutputFormat:
        return OutputFormat.XML

    def generate(self, force_regeneration: bool = False) -> None:
        if force_regeneration or not self.generated:
            _view = SCHEMA_VERSIONS[self.schema_version_enum]
            self.get_bom().validate()
            self._root_bom_element = self.get_bom().as_xml(  # type: ignore
                view_=_view, as_string=False, xmlns=self.get_target_namespace()
            )
            self.generated = True

    def output_as_string(self) -> str:
        self.generate()
        if not self.generated or self._root_bom_element is None:
            raise BomGenerationErrorException('There was no Root XML Element after BOM generation.')
        ElementTree.register_namespace('', self.get_target_namespace())
        return ElementTree.tostring(
            self._root_bom_element, method='xml',
            encoding='unicode', xml_declaration=True,
            # cannot set defaultNS, because the stupid XML serializer forgot to set NS on attributes.
            # therefore, the defaultNS was registered as nsID with empty string. see above.
            # see https://github.com/madpah/serializable/issues/12
            # default_namespace=self.get_target_namespace()
        )

    def get_target_namespace(self) -> str:
        return f'http://cyclonedx.org/schema/bom/{self.get_schema_version()}'


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


BY_SCHEMA_VERSION: Dict[SchemaVersion, Type[Xml]] = {
    SchemaVersion.V1_4: XmlV1Dot4,  # type:ignore[type-abstract]
    SchemaVersion.V1_3: XmlV1Dot3,  # type:ignore[type-abstract]
    SchemaVersion.V1_2: XmlV1Dot2,  # type:ignore[type-abstract]
    SchemaVersion.V1_1: XmlV1Dot1,  # type:ignore[type-abstract]
    SchemaVersion.V1_0: XmlV1Dot0,  # type:ignore[type-abstract]
}
