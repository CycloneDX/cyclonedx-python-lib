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
import xml.etree.ElementTree
from datetime import datetime, timezone
from typing import Any
from unittest import TestCase
from uuid import uuid4

from lxml import etree
from xmldiff import main
from xmldiff.actions import MoveNode

from cyclonedx.exception import MissingOptionalDependencyException
from cyclonedx.output import SchemaVersion
from cyclonedx.validation.json import JsonValidator
from cyclonedx.validation.xml import XmlValidator

single_uuid: str = 'urn:uuid:{}'.format(uuid4())

from . import SNAPSHOTS_DIRECTORY, RECREATE_SNAPSHOTS
from os.path import join


class SnapshotCompareMixin(object):
    def __getSnapshotFile(self, snapshot_name: str) -> str:
        return join(SNAPSHOTS_DIRECTORY, f'{snapshot_name}.bin')

    def writeSnapshot(self, snapshot_name: str, data: str):
        with open(self.__getSnapshotFile(snapshot_name), 'w') as s:
            s.write(data)

    def readSnapshot(self, snapshot_name: str) -> str:
        with open(self.__getSnapshotFile(snapshot_name), 'r') as s:
            return s.read()

    def assertEqualSnapshot(self, actual: str, snapshot_name: str) -> None:
        if RECREATE_SNAPSHOTS:
            self.writeSnapshot(snapshot_name, actual)
        self.assertEqual(actual, self.readSnapshot(snapshot_name))


class BaseJsonTestCase(TestCase):

    def assertValidAgainstSchema(self, bom_json: str, schema_version: SchemaVersion) -> None:
        try:
            validation_error = JsonValidator(schema_version).validate_str(bom_json)
        except MissingOptionalDependencyException:
            return  # some deps are missing - skip the validation
        self.assertIsNone(validation_error,
                          f'Failed to validate SBOM against JSON schema: {str(validation_error)}')

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
        try:
            validation_error = XmlValidator(schema_version).validate_str(bom_xml)
        except MissingOptionalDependencyException:
            return  # some deps are missing - skip the validation
        self.assertIsNone(validation_error,
                          f'Failed to validate Generated SBOM against XSD Schema: {str(validation_error)}')

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
