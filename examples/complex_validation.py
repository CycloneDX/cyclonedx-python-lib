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

import json
import sys
from typing import TYPE_CHECKING, Optional

from cyclonedx.exception import MissingOptionalDependencyException
from cyclonedx.schema import OutputFormat, SchemaVersion
from cyclonedx.validation import make_schemabased_validator

if TYPE_CHECKING:
    from cyclonedx.validation.json import JsonValidator
    from cyclonedx.validation.xml import XmlValidator

"""
This example demonstrates how to validate CycloneDX documents (both JSON and XML).
Make sure to have the needed dependencies installed - install the library's extra 'validation' for that.
"""

# region Sample SBOMs

JSON_SBOM = """
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.5",
  "version": 1,
  "metadata": {
    "component": {
      "type": "application",
      "name": "my-app",
      "version": "1.0.0"
    }
  },
  "components": []
}
"""

XML_SBOM = """<?xml version="1.0" encoding="UTF-8"?>
<bom xmlns="http://cyclonedx.org/schema/bom/1.5" version="1">
  <metadata>
    <component type="application">
      <name>my-app</name>
      <version>1.0.0</version>
    </component>
  </metadata>
</bom>
"""

INVALID_JSON_SBOM = """
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.5",
  "metadata": {
    "component": {
      "type": "invalid-type",
      "name": "my-app"
    }
  }
}
"""
# endregion Sample SBOMs


# region JSON Validation

print('--- JSON Validation ---')

# Create a JSON validator for a specific schema version
json_validator: 'JsonValidator' = make_schemabased_validator(OutputFormat.JSON, SchemaVersion.V1_5)

# 1. Validate valid SBOM
try:
    validation_errors = json_validator.validate_str(JSON_SBOM)
except MissingOptionalDependencyException as error:
    print('JSON validation was skipped:', error)
else:
    if validation_errors:
        print('JSON SBOM is unexpectedly invalid!', file=sys.stderr)
    else:
        print('JSON SBOM is valid')

    # 2. Validate invalid SBOM and inspect details
    print('\nChecking invalid JSON SBOM...')
    try:
        validation_errors = json_validator.validate_str(INVALID_JSON_SBOM)
    except MissingOptionalDependencyException as error:
        print('JSON validation was skipped:', error)
    else:
        if validation_errors:
            print('Validation failed as expected.')
            print(f'Error Message: {validation_errors.data.message}')
            print(f'JSON Path:     {validation_errors.data.json_path}')
            print(f'Invalid Data:  {validation_errors.data.instance}')

# endregion JSON Validation


print('\n' + '=' * 30 + '\n')


# region XML Validation

print('--- XML Validation ---')

xml_validator: 'XmlValidator' = make_schemabased_validator(OutputFormat.XML, SchemaVersion.V1_5)

try:
    xml_validation_errors = xml_validator.validate_str(XML_SBOM)
    if xml_validation_errors:
        print('XML SBOM is invalid!', file=sys.stderr)
    else:
        print('XML SBOM is valid')
except MissingOptionalDependencyException as error:
    print('XML validation was skipped:', error)

# endregion XML Validation


print('\n' + '=' * 30 + '\n')


# region Dynamic version detection

print('--- Dynamic Validation ---')


def _detect_json_format(raw_data: str) -> Optional[tuple[OutputFormat, SchemaVersion]]:
    """Detect JSON format and extract schema version."""
    try:
        data = json.loads(raw_data)
    except json.JSONDecodeError:
        return None

    spec_version_str = data.get('specVersion')
    try:
        schema_version = SchemaVersion.from_version(spec_version_str)
    except Exception:
        print('failed to detect schema_version from', repr(spec_version_str), file=sys.stderr)
        return None
    return (OutputFormat.JSON, schema_version)


def _detect_xml_format(raw_data: str) -> Optional[tuple[OutputFormat, SchemaVersion]]:
    try:
        from lxml import etree  # type: ignore[import-untyped]
    except ImportError:
        return None

    try:
        xml_tree = etree.fromstring(raw_data.encode('utf-8'))
    except etree.XMLSyntaxError:
        return None

    for ns in xml_tree.nsmap.values():
        if ns and ns.startswith('http://cyclonedx.org/schema/bom/'):
            version_str = ns.split('/')[-1]
            try:
                return (OutputFormat.XML, SchemaVersion.from_version(version_str))
            except Exception:
                print('failed to detect schema_version from namespace', repr(ns), file=sys.stderr)
                return None

    print('failed to detect CycloneDX namespace in XML document', file=sys.stderr)
    return None


def validate_sbom(raw_data: str) -> bool:
    """Validate an SBOM by detecting its format and version."""
    # Detect format and version
    format_info = _detect_json_format(raw_data) or _detect_xml_format(raw_data)
    if not format_info:
        return False

    input_format, schema_version = format_info
    try:
        validator = make_schemabased_validator(input_format, schema_version)
        errors = validator.validate_str(raw_data)
        if errors:
            print(f'Validation failed ({input_format.name} {schema_version.to_version()}): {errors}',
                  file=sys.stderr)
            return False
        print(f'Valid {input_format.name} SBOM (schema {schema_version.to_version()})')
        return True
    except MissingOptionalDependencyException as e:
        print(f'Validation skipped (missing dependencies): {e}')
        return False


# Execute dynamic validation
validate_sbom(JSON_SBOM)
validate_sbom(XML_SBOM)

# endregion Dynamic version detection
