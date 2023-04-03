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
from typing import cast, Dict, Any, Optional
from unittest import TestCase

from lxml import etree  # type: ignore
from packageurl import PackageURL

from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component
from cyclonedx.output import get_instance
from cyclonedx.output.json import Json
from cyclonedx.output.xml import Xml
from cyclonedx.schema import OutputFormat

from .base import cyclonedx_lib_name, cyclonedx_lib_version

OUR_PACKAGE_NAME: str = cyclonedx_lib_name
OUR_PACKAGE_VERSION: str = cyclonedx_lib_version
OUR_PACKAGE_AUTHOR: str = 'Paul Horton'

TEST_BOM: Bom = Bom()
TEST_BOM.components.add(
    Component(
        name=OUR_PACKAGE_NAME, author=OUR_PACKAGE_AUTHOR, version=OUR_PACKAGE_VERSION,
        purl=PackageURL(type='pypi', name=OUR_PACKAGE_NAME, version=OUR_PACKAGE_VERSION)
    )
)


class TestE2EEnvironment(TestCase):

    def test_json_defaults(self) -> None:
        outputter: Json = cast(Json, get_instance(bom=TEST_BOM, output_format=OutputFormat.JSON))
        bom_json = json.loads(outputter.output_as_string())
        self.assertTrue('metadata' in bom_json)
        self.assertFalse('component' in bom_json['metadata'])
        component_this_library: Optional[Dict[str, Any]] = next(
            (x for x in bom_json['components'] if
             x['purl'] == 'pkg:pypi/{}@{}'.format(OUR_PACKAGE_NAME, OUR_PACKAGE_VERSION)), None
        )

        self.assertIsNotNone(component_this_library)
        if component_this_library:
            self.assertTrue('author' in component_this_library.keys(), 'author is missing from JSON BOM')
            self.assertEqual(component_this_library['author'], OUR_PACKAGE_AUTHOR)
            self.assertEqual(component_this_library['name'], OUR_PACKAGE_NAME)
            self.assertEqual(component_this_library['version'], OUR_PACKAGE_VERSION)

    def test_xml_defaults(self) -> None:
        outputter: Xml = cast(Xml, get_instance(bom=TEST_BOM))

        # Check we have cyclonedx-python-lib with Author, Name and Version
        bom_xml_e: etree.ElementTree = etree.fromstring(bytes(outputter.output_as_string(), encoding='utf-8'))
        component_this_library: etree.Element = bom_xml_e.xpath(
            '/cdx:bom/cdx:components/cdx:component',
            namespaces={
                'cdx': outputter.get_target_namespace()
            }
        )[0]
        for a in component_this_library:
            if a.tag == 'author':
                self.assertEqual(a.text, OUR_PACKAGE_AUTHOR)
            if a.tag == 'name':
                self.assertEqual(a.text, OUR_PACKAGE_NAME)
            if a.tag == 'version':
                self.assertEqual(a.text, OUR_PACKAGE_VERSION)
