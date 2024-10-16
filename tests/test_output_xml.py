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

import re
from typing import Any, Callable
from unittest import TestCase
from unittest.mock import Mock, patch
from warnings import warn

from ddt import ddt, idata, named_data, unpack

from cyclonedx.exception import CycloneDxException, MissingOptionalDependencyException
from cyclonedx.exception.model import (
    InvalidOmniBorIdException,
    InvalidSwhidException,
    LicenseExpressionAlongWithOthersException,
    UnknownComponentDependencyException,
)
from cyclonedx.model.bom import Bom
from cyclonedx.output.xml import BY_SCHEMA_VERSION, Xml
from cyclonedx.schema import OutputFormat, SchemaVersion
from cyclonedx.validation.xml import XmlValidator
from tests import SnapshotMixin, is_valid_for_schema_version, mksname
from tests._data.models import all_get_bom_funct_invalid, all_get_bom_funct_valid, bom_all_same_bomref


@ddt
class TestOutputXml(TestCase, SnapshotMixin):

    @named_data(*(
        (f'{n}-{sv.to_version()}', gb, sv)
        for n, gb in all_get_bom_funct_valid
        for sv in SchemaVersion
        if is_valid_for_schema_version(gb, sv)
    ))
    @unpack
    @patch('cyclonedx.builder.this.__ThisVersion', 'TESTING')
    def test_valid(self, get_bom: Callable[[], Bom], sv: SchemaVersion, *_: Any, **__: Any) -> None:
        snapshot_name = mksname(get_bom, sv, OutputFormat.XML)
        if snapshot_name is None:
            return
        bom = get_bom()
        xml = BY_SCHEMA_VERSION[sv](bom).output_as_string(indent=2)
        try:
            errors = XmlValidator(sv).validate_str(xml)
        except MissingOptionalDependencyException:
            warn('!!! skipped schema validation',
                 category=UserWarning, stacklevel=0)
        else:
            self.assertIsNone(errors, xml)
        self.assertEqualSnapshot(xml, snapshot_name)

    @named_data(*(
        (f'{n}-{sv.to_version()}', gb, sv)
        for n, gb in all_get_bom_funct_invalid
        for sv in SchemaVersion
        if is_valid_for_schema_version(gb, sv)
    ))
    @unpack
    def test_invalid(self, get_bom: Callable[[], Bom], sv: SchemaVersion) -> None:
        with self.assertRaises(CycloneDxException) as error:
            bom = get_bom()
            outputter = BY_SCHEMA_VERSION[sv](bom)
            outputter.output_as_string()
        if isinstance(error.exception, (
            LicenseExpressionAlongWithOthersException,
            InvalidOmniBorIdException,
            InvalidSwhidException,
            UnknownComponentDependencyException,
        )):
            return None  # expected
        raise error.exception

    def test_bomref_not_duplicate(self) -> None:
        bom, nr_bomrefs = bom_all_same_bomref()
        output = BY_SCHEMA_VERSION[SchemaVersion.V1_4](bom).output_as_string()
        found = re.findall(r'bom-ref="(.*?)"', output)
        self.assertEqual(nr_bomrefs, len(found))
        self.assertCountEqual(set(found), found, 'expected unique items')


@ddt
class TestFunctionalBySchemaVersion(TestCase):

    @idata(SchemaVersion)
    def test_get_outputter_expected(self, sv: SchemaVersion) -> None:
        outputter_class = BY_SCHEMA_VERSION[sv]
        self.assertTrue(issubclass(outputter_class, Xml))
        outputter = outputter_class(Mock(spec=Bom))
        self.assertIs(outputter.schema_version, sv)
        self.assertIs(outputter.output_format, OutputFormat.XML)
