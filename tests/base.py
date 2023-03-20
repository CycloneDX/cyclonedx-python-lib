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

import io
import json
import os
import sys
import xml.etree.ElementTree
from datetime import datetime, timezone
from typing import Any
from unittest import TestCase
from uuid import uuid4

from lxml import etree
from lxml.etree import DocumentInvalid
from xmldiff import main
from xmldiff.actions import MoveNode

from cyclonedx.output import SchemaVersion

if sys.version_info >= (3, 7):
    from jsonschema import ValidationError, validate as json_validate

if sys.version_info >= (3, 8):
    from importlib.metadata import PackageNotFoundError, version
else:
    from importlib_metadata import PackageNotFoundError, version

from . import CDX_SCHEMA_DIRECTORY

cyclonedx_lib_name: str = 'cyclonedx-python-lib'
cyclonedx_lib_version: str = 'DEV'
try:
    cyclonedx_lib_version: str = version(cyclonedx_lib_name)
except PackageNotFoundError:
    pass
single_uuid: str = 'urn:uuid:{}'.format(uuid4())


class BaseJsonTestCase(TestCase):

    def assertValidAgainstSchema(self, bom_json: str, schema_version: SchemaVersion) -> None:
        if sys.version_info >= (3, 7):
            schema_fn = os.path.join(
                CDX_SCHEMA_DIRECTORY,
                f'bom-{schema_version.name.replace("_", ".").replace("V", "")}.schema.json'
            )
            with open(schema_fn) as schema_fd:
                schema_doc = json.load(schema_fd)

            try:
                json_validate(instance=json.loads(bom_json), schema=schema_doc)
            except ValidationError as e:
                self.assertTrue(False, f'Failed to validate SBOM against JSON schema: {str(e)}')

            self.assertTrue(True)
        else:
            self.assertTrue(True, 'JSON Schema Validation is not possible in Python < 3.7')

    @staticmethod
    def _sort_json_dict(item: object) -> Any:
        if isinstance(item, dict):
            return sorted((key, BaseJsonTestCase._sort_json_dict(values)) for key, values in item.items())
        if isinstance(item, list):
            return sorted(BaseJsonTestCase._sort_json_dict(x) for x in item)
        else:
            return item

    def assertEqualJson(self, a: str, b: str) -> None:
        self.assertEqual(
            BaseJsonTestCase._sort_json_dict(json.loads(a)),
            BaseJsonTestCase._sort_json_dict(json.loads(b))
        )

    def assertEqualJsonBom(self, a: str, b: str) -> None:
        """
        Remove UUID before comparison as this will be unique to each generation
        """
        ab = json.loads(a)
        bb = json.loads(b)

        # Null serialNumbers
        ab['serialNumber'] = single_uuid
        bb['serialNumber'] = single_uuid

        # Unify timestamps to ensure they will compare
        now = datetime.now(tz=timezone.utc)
        if 'metadata' in ab.keys():
            ab['metadata']['timestamp'] = now.isoformat()
        if 'metadata' in bb.keys():
            bb['metadata']['timestamp'] = now.isoformat()

        self.assertEqualJson(json.dumps(ab), json.dumps(bb))


class BaseXmlTestCase(TestCase):

    def assertValidAgainstSchema(self, bom_xml: str, schema_version: SchemaVersion) -> None:
        xsd_fn = os.path.join(CDX_SCHEMA_DIRECTORY, f'bom-{schema_version.name.replace("_", ".").replace("V", "")}.xsd')
        with open(xsd_fn) as xsd_fd:
            xsd_doc = etree.parse(xsd_fd)

        xml_schema = etree.XMLSchema(xsd_doc)
        schema_validates = False
        try:
            schema_validates = xml_schema.validate(etree.parse(io.BytesIO(bytes(bom_xml, 'ascii'))))
        except DocumentInvalid as e:
            print(f'Failed to validate SBOM against schema: {str(e)}')

        if not schema_validates:
            print(xml_schema.error_log.last_error)
        self.assertTrue(schema_validates, f'Failed to validate Generated SBOM against XSD Schema:'
                                          f'{bom_xml}')

    def assertEqualXml(self, a: str, b: str) -> None:
        diff_results = main.diff_texts(a, b, diff_options={'F': 0.5})
        diff_results = list(filter(lambda o: not isinstance(o, MoveNode), diff_results))
        self.assertEqual(len(diff_results), 0, f'There are XML differences: {diff_results}\n- {a}\n+ {b}')

    def assertEqualXmlBom(self, a: str, b: str, namespace: str) -> None:
        """
        Sanitise some fields such as timestamps which cannot have their values directly compared for equality.
        """
        ba = xml.etree.ElementTree.fromstring(a, etree.XMLParser(remove_blank_text=True, remove_comments=True))
        bb = xml.etree.ElementTree.fromstring(b, etree.XMLParser(remove_blank_text=True, remove_comments=True))

        # Align serialNumbers
        ba.set('serialNumber', single_uuid)
        bb.set('serialNumber', single_uuid)

        # Align timestamps in metadata
        now = datetime.now(tz=timezone.utc)
        metadata_ts_a = ba.find('./{{{}}}metadata/{{{}}}timestamp'.format(namespace, namespace))
        if metadata_ts_a is not None:
            metadata_ts_a.text = now.isoformat()
        metadata_ts_b = bb.find('./{{{}}}metadata/{{{}}}timestamp'.format(namespace, namespace))
        if metadata_ts_b is not None:
            metadata_ts_b.text = now.isoformat()

        self.assertEqualXml(
            xml.etree.ElementTree.tostring(ba, 'unicode'),
            xml.etree.ElementTree.tostring(bb, 'unicode')
        )
