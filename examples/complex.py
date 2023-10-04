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

import sys

from packageurl import PackageURL

from cyclonedx.exception import MissingOptionalDependencyException
from cyclonedx.factory.license import LicenseChoiceFactory, LicenseFactory
from cyclonedx.model import OrganizationalEntity, XsUri
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component, ComponentType
from cyclonedx.output import get_instance as get_outputter
from cyclonedx.output.json import JsonV1Dot4
from cyclonedx.schema import SchemaVersion, OutputFormat
from cyclonedx.validation.json import JsonStrictValidator
from cyclonedx.validation import get_instance as get_validator

lc_factory = LicenseChoiceFactory(license_factory=LicenseFactory())

# region build the BOM

bom = Bom()
bom.metadata.component = rootComponent = Component(
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
bom.register_dependency(rootComponent, [component1])

component2 = Component(
    type=ComponentType.LIBRARY,
    name='some-library',
    licenses=[lc_factory.make_from_string('GPL-3.0-only WITH Classpath-exception-2.0')]
)
bom.components.add(component2)
bom.register_dependency(component1, [component2])

# endregion build the BOM


serialized_json = JsonV1Dot4(bom).output_as_string(indent=2)
print(serialized_json)
try:
    validation_errors = JsonStrictValidator(SchemaVersion.V1_4).validate_str(serialized_json)
    if validation_errors:
        print('JSON invalid', 'ValidationError:', repr(validation_errors), sep='\n', file=sys.stderr)
        sys.exit(2)
    print('JSON valid')
except MissingOptionalDependencyException as error:
    print('JSON-validation was skipped due to', error)

print('', '=' * 30, '', sep='\n')

my_outputter = get_outputter(bom, OutputFormat.XML, SchemaVersion.V1_4)
serialized_xml = my_outputter.output_as_string(indent=2)
print(serialized_xml)
try:
    validation_errors = get_validator(my_outputter.output_format,
                                      my_outputter.schema_version
                                      ).validate_str(serialized_xml)
    if validation_errors:
        print('XML invalid', 'ValidationError:', repr(validation_errors), sep='\n', file=sys.stderr)
        sys.exit(2)
    print('XML valid')
except MissingOptionalDependencyException as error:
    print('XML-validation was skipped due to', error)
