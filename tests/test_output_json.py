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


import re
from typing import Any, Callable
from unittest import TestCase
from unittest.mock import Mock, patch

from ddt import data, ddt, idata, named_data, unpack

from cyclonedx.exception import CycloneDxException, MissingOptionalDependencyException
from cyclonedx.exception.model import LicenseExpressionAlongWithOthersException, UnknownComponentDependencyException
from cyclonedx.exception.output import FormatNotSupportedException
from cyclonedx.model.bom import Bom
from cyclonedx.output.json import BY_SCHEMA_VERSION, Json
from cyclonedx.schema import OutputFormat, SchemaVersion
from cyclonedx.validation.json import JsonStrictValidator
from tests import SnapshotMixin, mksname, uuid_generator
from tests._data.models import all_get_bom_funct_invalid, all_get_bom_funct_valid, bom_all_same_bomref

UNSUPPORTED_SV = frozenset((SchemaVersion.V1_1, SchemaVersion.V1_0,))


@ddt
class TestOutputJson(TestCase, SnapshotMixin):

    @data(*UNSUPPORTED_SV)
    def test_unsupported_schema_raises(self, sv: SchemaVersion) -> None:
        outputter_class = BY_SCHEMA_VERSION[sv]
        self.assertTrue(issubclass(outputter_class, Json))
        outputter = outputter_class(Mock(spec=Bom))
        with self.assertRaises(FormatNotSupportedException):
            outputter.output_as_string()

    @named_data(*((f'{n}-{sv.to_version()}', gb, sv)
                  for n, gb in all_get_bom_funct_valid
                  for sv in SchemaVersion
                  if sv not in UNSUPPORTED_SV))
    @unpack
    @patch('cyclonedx.model.ThisTool._version', 'TESTING')
    @patch('cyclonedx.model.bom_ref.uuid4', side_effect=uuid_generator(0, version=4))
    def test_valid(self, get_bom: Callable[[], Bom], sv: SchemaVersion, *_: Any, **__: Any) -> None:
        snapshot_name = mksname(get_bom, sv, OutputFormat.JSON)
        bom = get_bom()
        json = BY_SCHEMA_VERSION[sv](bom).output_as_string(indent=2)
        try:
            errors = JsonStrictValidator(sv).validate_str(json)
        except MissingOptionalDependencyException:
            errors = None  # skipped validation
        self.assertIsNone(errors)
        self.assertEqualSnapshot(json, snapshot_name)

    @named_data(*((f'{n}-{sv.to_version()}', gb, sv)
                  for n, gb in all_get_bom_funct_invalid
                  for sv in SchemaVersion
                  if sv not in UNSUPPORTED_SV))
    @unpack
    def test_invalid(self, get_bom: Callable[[], Bom], sv: SchemaVersion) -> None:
        bom = get_bom()
        outputter = BY_SCHEMA_VERSION[sv](bom)
        with self.assertRaises(CycloneDxException) as error:
            outputter.output_as_string()
        if isinstance(error.exception, (
            LicenseExpressionAlongWithOthersException,
            UnknownComponentDependencyException,
        )):
            return None  # expected
        raise error.exception

    def test_bomref_not_duplicate(self) -> None:
        bom, nr_bomrefs = bom_all_same_bomref()
        output = BY_SCHEMA_VERSION[SchemaVersion.V1_4](bom).output_as_string()
        found = re.findall(r'"bom-ref":\s*"(.*?)"', output)
        self.assertEqual(nr_bomrefs, len(found))
        self.assertCountEqual(set(found), found, 'expected unique items')


@ddt
class TestFunctionalBySchemaVersion(TestCase):

    @idata(SchemaVersion)
    def test_get_outputter_expected(self, sv: SchemaVersion) -> None:
        outputter_class = BY_SCHEMA_VERSION[sv]
        self.assertTrue(issubclass(outputter_class, Json))
        outputter = outputter_class(Mock(spec=Bom))
        self.assertIs(outputter.schema_version, sv)
        self.assertIs(outputter.output_format, OutputFormat.JSON)
