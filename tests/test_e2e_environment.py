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
import os
from unittest import TestCase
from xml.etree import ElementTree

from cyclonedx.model.bom import Bom
from cyclonedx.output import get_instance, OutputFormat
from cyclonedx.output.json import Json
from cyclonedx.output.xml import Xml
from cyclonedx.parser.environment import EnvironmentParser


class TestE2EEnvironment(TestCase):
    _our_package_version: str

    @classmethod
    def setUpClass(cls) -> None:
        with open(os.path.join(os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../')),
                               'VERSION')) as _our_version:
            cls._our_package_version = _our_version.read()

        _our_version.close()

    def test_json_defaults(self):
        outputter: Json = get_instance(bom=Bom.from_parser(EnvironmentParser()), output_format=OutputFormat.JSON)
        bom_json = json.loads(outputter.output_as_string())
        component_this_library = next(
            (x for x in bom_json['components'] if
             x['purl'] == 'pkg:pypi/cyclonedx-python-lib@{}'.format(TestE2EEnvironment._our_package_version)), None
        )

        self.assertTrue('author' in component_this_library.keys(), 'author is missing from JSON BOM')
        self.assertEqual(component_this_library['author'], 'Sonatype Community')
        self.assertEqual(component_this_library['name'], 'cyclonedx-python-lib')
        self.assertEqual(component_this_library['version'], TestE2EEnvironment._our_package_version)

    def test_xml_defaults(self):
        outputter: Xml = get_instance(bom=Bom.from_parser(EnvironmentParser()))

        # Check we have cyclonedx-python-lib with Author, Name and Version
        bom_xml_e = ElementTree.fromstring(outputter.output_as_string())
        component_this_library = bom_xml_e.find('./{{{}}}components/{{{}}}component[@bom-ref=\'pkg:pypi/{}\']'.format(
            outputter.get_target_namespace(), outputter.get_target_namespace(), 'cyclonedx-python-lib@{}'.format(
                TestE2EEnvironment._our_package_version
            )
        ))

        author = component_this_library.find('./{{{}}}author'.format(outputter.get_target_namespace()))
        self.assertIsNotNone(author, 'No author element but one was expected.')
        self.assertEqual(author.text, 'Sonatype Community')

        name = component_this_library.find('./{{{}}}name'.format(outputter.get_target_namespace()))
        self.assertIsNotNone(name, 'No name element but one was expected.')
        self.assertEqual(name.text, 'cyclonedx-python-lib')

        version = component_this_library.find('./{{{}}}version'.format(outputter.get_target_namespace()))
        self.assertIsNotNone(version, 'No version element but one was expected.')
        self.assertEqual(version.text, TestE2EEnvironment._our_package_version)
