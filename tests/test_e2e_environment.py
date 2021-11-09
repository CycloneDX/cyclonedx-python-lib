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
from unittest import TestCase
from xml.etree import ElementTree

import pkg_resources

from cyclonedx.model.bom import Bom
from cyclonedx.output import get_instance, OutputFormat
from cyclonedx.output.json import Json
from cyclonedx.output.xml import Xml
from cyclonedx.parser.environment import EnvironmentParser

OUR_PACKAGE_NAME: str = 'cyclonedx-python-lib'
OUR_PACKAGE_VERSION: str = pkg_resources.get_distribution(OUR_PACKAGE_NAME).version
OUR_PACKAGE_AUTHOR: str = 'Paul Horton'


class TestE2EEnvironment(TestCase):

    def test_json_defaults(self) -> None:
        outputter: Json = get_instance(bom=Bom.from_parser(EnvironmentParser()), output_format=OutputFormat.JSON)
        bom_json = json.loads(outputter.output_as_string())
        component_this_library = next(
            (x for x in bom_json['components'] if
             x['purl'] == 'pkg:pypi/{}@{}'.format(OUR_PACKAGE_NAME, OUR_PACKAGE_VERSION)), None
        )

        self.assertTrue('author' in component_this_library.keys(), 'author is missing from JSON BOM')
        self.assertEqual(component_this_library['author'], OUR_PACKAGE_AUTHOR)
        self.assertEqual(component_this_library['name'], OUR_PACKAGE_NAME)
        self.assertEqual(component_this_library['version'], OUR_PACKAGE_VERSION)

    def test_xml_defaults(self) -> None:
        outputter: Xml = get_instance(bom=Bom.from_parser(EnvironmentParser()))

        # Check we have cyclonedx-python-lib with Author, Name and Version
        bom_xml_e = ElementTree.fromstring(outputter.output_as_string())
        component_this_library = bom_xml_e.find('./{{{}}}components/{{{}}}component[@bom-ref=\'pkg:pypi/{}\']'.format(
            outputter.get_target_namespace(), outputter.get_target_namespace(), '{}@{}'.format(
                OUR_PACKAGE_NAME, OUR_PACKAGE_VERSION
            )
        ))

        author = component_this_library.find('./{{{}}}author'.format(outputter.get_target_namespace()))
        self.assertIsNotNone(author, 'No author element but one was expected.')
        self.assertEqual(author.text, OUR_PACKAGE_AUTHOR)

        name = component_this_library.find('./{{{}}}name'.format(outputter.get_target_namespace()))
        self.assertIsNotNone(name, 'No name element but one was expected.')
        self.assertEqual(name.text, OUR_PACKAGE_NAME)

        version = component_this_library.find('./{{{}}}version'.format(outputter.get_target_namespace()))
        self.assertIsNotNone(version, 'No version element but one was expected.')
        self.assertEqual(version.text, OUR_PACKAGE_VERSION)
