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
from typing import TYPE_CHECKING

from packageurl import PackageURL

from cyclonedx.builder.this import this_component as cdx_lib_component
from cyclonedx.exception import MissingOptionalDependencyException
from cyclonedx.factory.license import LicenseFactory
from cyclonedx.model import XsUri
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component, ComponentType
from cyclonedx.model.contact import OrganizationalEntity
from cyclonedx.output import make_outputter
from cyclonedx.output.json import JsonV1Dot5
from cyclonedx.schema import OutputFormat, SchemaVersion
from cyclonedx.validation import make_schemabased_validator
from cyclonedx.validation.json import JsonStrictValidator

if TYPE_CHECKING:
    from cyclonedx.output.json import Json as JsonOutputter
    from cyclonedx.output.xml import Xml as XmlOutputter
    from cyclonedx.validation.xml import XmlValidator


lc_factory = LicenseFactory()

# region build the BOM

bom = Bom()
bom.metadata.tools.components.add(cdx_lib_component())
bom.metadata.tools.components.add(Component(
    name='my-own-SBOM-generator',
    type=ComponentType.APPLICATION,
))

bom.metadata.component = root_component = Component(
    name='myApp',
    type=ComponentType.APPLICATION,
    licenses=[lc_factory.make_from_string('MIT')],
    bom_ref='myApp',
)

component1 = Component(
    type=ComponentType.LIBRARY,
    name='some-component',
    group='acme',
    version='1.33.7-beta.1',
    licenses=[lc_factory.make_from_string('(c) 2021 Acme inc.')],
    supplier=OrganizationalEntity(
        name='Acme Inc',
        urls=[XsUri('https://www.acme.org')]
    ),
    bom_ref='myComponent@1.33.7-beta.1',
    purl=PackageURL('generic', 'acme', 'some-component', '1.33.7-beta.1')
)
bom.components.add(component1)
bom.register_dependency(root_component, [component1])

component2 = Component(
    type=ComponentType.LIBRARY,
    name='some-library',
    licenses=[lc_factory.make_from_string('GPL-3.0-only WITH Classpath-exception-2.0')]
)
bom.components.add(component2)
bom.register_dependency(component1, [component2])

# endregion build the BOM

# region JSON
"""demo with explicit instructions for SchemaVersion, outputter and validator"""

my_json_outputter: 'JsonOutputter' = JsonV1Dot5(bom)
serialized_json = my_json_outputter.output_as_string(indent=2)
print(serialized_json)
my_json_validator = JsonStrictValidator(SchemaVersion.V1_6)
try:
    validation_errors = my_json_validator.validate_str(serialized_json)
    if validation_errors:
        print('JSON invalid', 'ValidationError:', repr(validation_errors), sep='\n', file=sys.stderr)
        sys.exit(2)
    print('JSON valid')
except MissingOptionalDependencyException as error:
    print('JSON-validation was skipped due to', error)

# endregion JSON

print('', '=' * 30, '', sep='\n')

# region XML
"""demo with implicit instructions for SchemaVersion, outputter and validator. TypeCheckers will catch errors."""

my_xml_outputter: 'XmlOutputter' = make_outputter(bom, OutputFormat.XML, SchemaVersion.V1_6)
serialized_xml = my_xml_outputter.output_as_string(indent=2)
print(serialized_xml)
my_xml_validator: 'XmlValidator' = make_schemabased_validator(
    my_xml_outputter.output_format, my_xml_outputter.schema_version)
try:
    validation_errors = my_xml_validator.validate_str(serialized_xml)
    if validation_errors:
        print('XML invalid', 'ValidationError:', repr(validation_errors), sep='\n', file=sys.stderr)
        sys.exit(2)
    print('XML valid')
except MissingOptionalDependencyException as error:
    print('XML-validation was skipped due to', error)

# endregion XML
