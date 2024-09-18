# This file is part of CycloneDX Python Library
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

import sys
from json import loads as json_loads
from typing import TYPE_CHECKING

from defusedxml import ElementTree as SafeElementTree  # type:ignore[import-untyped]

from cyclonedx.exception import MissingOptionalDependencyException
from cyclonedx.model.bom import Bom
from cyclonedx.schema import OutputFormat, SchemaVersion
from cyclonedx.validation import make_schemabased_validator
from cyclonedx.validation.json import JsonStrictValidator

if TYPE_CHECKING:
    from cyclonedx.validation.xml import XmlValidator

# region JSON

json_data = """{
  "$schema": "http://cyclonedx.org/schema/bom-1.6.schema.json",
  "bomFormat": "CycloneDX",
  "specVersion": "1.6",
  "serialNumber": "urn:uuid:88fabcfa-7529-4ba2-8256-29bec0c03900",
  "version": 1,
  "metadata": {
    "timestamp": "2024-02-10T21:38:53.313120+00:00",
    "tools": [
      {
        "vendor": "CycloneDX",
        "name": "cyclonedx-python-lib",
        "version": "6.4.1",
        "externalReferences": [
          {
            "type": "build-system",
            "url": "https://github.com/CycloneDX/cyclonedx-python-lib/actions"
          },
          {
            "type": "distribution",
            "url": "https://pypi.org/project/cyclonedx-python-lib/"
          },
          {
            "type": "documentation",
            "url": "https://cyclonedx-python-library.readthedocs.io/"
          },
          {
            "type": "issue-tracker",
            "url": "https://github.com/CycloneDX/cyclonedx-python-lib/issues"
          },
          {
            "type": "license",
            "url": "https://github.com/CycloneDX/cyclonedx-python-lib/blob/main/LICENSE"
          },
          {
            "type": "release-notes",
            "url": "https://github.com/CycloneDX/cyclonedx-python-lib/blob/main/CHANGELOG.md"
          },
          {
            "type": "vcs",
            "url": "https://github.com/CycloneDX/cyclonedx-python-lib"
          },
          {
            "type": "website",
            "url": "https://github.com/CycloneDX/cyclonedx-python-lib/#readme"
          }
        ]
      }
    ],
    "component": {
      "bom-ref": "myApp",
      "name": "myApp",
      "type": "application",
      "licenses": [
        {
          "license": {
            "id": "MIT"
          }
        }
      ]
    }
  },
  "components": [
    {
      "bom-ref": "myComponent@1.33.7-beta.1",
      "type": "library",
      "group": "acme",
      "name": "some-component",
      "version": "1.33.7-beta.1",
      "purl": "pkg:generic/acme/some-component@1.33.7-beta.1",
      "licenses": [
        {
          "license": {
            "name": "(c) 2021 Acme inc."
          }
        }
      ],
      "supplier": {
        "name": "Acme Inc",
        "url": [
          "https://www.acme.org"
        ]
      }
    },
    {
      "bom-ref": "some-lib",
      "type": "library",
      "name": "some-library",
      "licenses": [
        {
          "expression": "GPL-3.0-only WITH Classpath-exception-2.0"
        }
      ]
    }
  ],
  "dependencies": [
    {
      "ref": "some-lib"
    },
    {
      "dependsOn": [
        "myComponent@1.33.7-beta.1"
      ],
      "ref": "myApp"
    },
    {
      "dependsOn": [
        "some-lib"
      ],
      "ref": "myComponent@1.33.7-beta.1"
    }
  ]
}"""
my_json_validator = JsonStrictValidator(SchemaVersion.V1_6)
try:
    validation_errors = my_json_validator.validate_str(json_data)
    if validation_errors:
        print('JSON invalid', 'ValidationError:', repr(validation_errors), sep='\n', file=sys.stderr)
        sys.exit(2)
    print('JSON valid')
except MissingOptionalDependencyException as error:
    print('JSON-validation was skipped due to', error)
bom_from_json = Bom.from_json(  # type: ignore[attr-defined]
    json_loads(json_data))
print('bom_from_json', repr(bom_from_json))

# endregion JSON

print('', '=' * 30, '', sep='\n')

# endregion XML

xml_data = """<?xml version="1.0" ?>
<bom xmlns="http://cyclonedx.org/schema/bom/1.6"
  serialNumber="urn:uuid:88fabcfa-7529-4ba2-8256-29bec0c03900"
  version="1"
>
  <metadata>
    <timestamp>2024-02-10T21:38:53.313120+00:00</timestamp>
    <tools>
      <tool>
        <vendor>CycloneDX</vendor>
        <name>cyclonedx-python-lib</name>
        <version>6.4.1</version>
        <externalReferences>
          <reference type="build-system">
            <url>https://github.com/CycloneDX/cyclonedx-python-lib/actions</url>
          </reference>
          <reference type="distribution">
            <url>https://pypi.org/project/cyclonedx-python-lib/</url>
          </reference>
          <reference type="documentation">
            <url>https://cyclonedx-python-library.readthedocs.io/</url>
          </reference>
          <reference type="issue-tracker">
            <url>https://github.com/CycloneDX/cyclonedx-python-lib/issues</url>
          </reference>
          <reference type="license">
            <url>https://github.com/CycloneDX/cyclonedx-python-lib/blob/main/LICENSE</url>
          </reference>
          <reference type="release-notes">
            <url>https://github.com/CycloneDX/cyclonedx-python-lib/blob/main/CHANGELOG.md</url>
          </reference>
          <reference type="vcs">
            <url>https://github.com/CycloneDX/cyclonedx-python-lib</url>
          </reference>
          <reference type="website">
            <url>https://github.com/CycloneDX/cyclonedx-python-lib/#readme</url>
          </reference>
        </externalReferences>
      </tool>
    </tools>
    <component type="application" bom-ref="myApp">
      <name>myApp</name>
      <licenses>
        <license>
          <id>MIT</id>
        </license>
      </licenses>
    </component>
  </metadata>
  <components>
    <component type="library" bom-ref="myComponent@1.33.7-beta.1">
      <supplier>
        <name>Acme Inc</name>
        <url>https://www.acme.org</url>
      </supplier>
      <group>acme</group>
      <name>some-component</name>
      <version>1.33.7-beta.1</version>
      <licenses>
        <license>
          <name>(c) 2021 Acme inc.</name>
        </license>
      </licenses>
      <purl>pkg:generic/acme/some-component@1.33.7-beta.1</purl>
    </component>
    <component type="library" bom-ref="some-lib">
      <name>some-library</name>
      <licenses>
        <expression>GPL-3.0-only WITH Classpath-exception-2.0</expression>
      </licenses>
    </component>
  </components>
  <dependencies>
    <dependency ref="some-lib"/>
    <dependency ref="myApp">
      <dependency ref="myComponent@1.33.7-beta.1"/>
    </dependency>
    <dependency ref="myComponent@1.33.7-beta.1">
      <dependency ref="some-lib"/>
    </dependency>
  </dependencies>
</bom>"""
my_xml_validator: 'XmlValidator' = make_schemabased_validator(OutputFormat.XML, SchemaVersion.V1_6)
try:
    validation_errors = my_xml_validator.validate_str(xml_data)
    if validation_errors:
        print('XML invalid', 'ValidationError:', repr(validation_errors), sep='\n', file=sys.stderr)
        sys.exit(2)
    print('XML valid')
except MissingOptionalDependencyException as error:
    print('XML-validation was skipped due to', error)
bom_from_xml = Bom.from_xml(  # type: ignore[attr-defined]
    SafeElementTree.fromstring(xml_data))
print('bom_from_xml', repr(bom_from_xml))

# endregion XML

print('', '=' * 30, '', sep='\n')

print('assert bom_from_json equals bom_from_xml')
assert bom_from_json == bom_from_xml, 'expected to have equal BOMs from JSON and XML'
