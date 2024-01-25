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


from glob import iglob
from os.path import basename, join
from typing import Any, Callable
from unittest import TestCase
from unittest.mock import patch

from ddt import ddt, named_data

from cyclonedx.model.bom import Bom
from cyclonedx.schema import OutputFormat, SchemaVersion
from tests import (
    LATEST_SUPPORTED_SCHEMA,
    SCHEMA_TESTDATA_DIRECTORY,
    UNDEFINED_SCHEMA_VERSIONS,
    DeepCompareMixin,
    SnapshotMixin,
    mksname,
)
from tests._data.models import all_get_bom_funct_valid_immut, all_get_bom_funct_with_incomplete_deps

# only latest schema will have all data populated in serialized form

_UNDEFINED_SCHEMA_VERSIONS = UNDEFINED_SCHEMA_VERSIONS[OutputFormat.XML]


@ddt
class TestDeserializeXml(TestCase, SnapshotMixin, DeepCompareMixin):

    @named_data(*all_get_bom_funct_valid_immut)
    @patch('cyclonedx.model.ThisTool._version', 'TESTING')
    def test_prepared(self, get_bom: Callable[[], Bom], *_: Any, **__: Any) -> None:
        # only latest schema will have all data populated in serialized form
        snapshot_name = mksname(get_bom, LATEST_SUPPORTED_SCHEMA, OutputFormat.XML)
        expected = get_bom()
        with open(self.getSnapshotFile(snapshot_name), 'r') as s:
            bom = Bom.from_xml(s)
        self.assertBomDeepEqual(expected, bom,
                                fuzzy_deps=get_bom in all_get_bom_funct_with_incomplete_deps)

    @named_data(*(
        (f'{sv.name}/{basename(tf)}', tf)
        for sv in SchemaVersion if sv not in _UNDEFINED_SCHEMA_VERSIONS
        for tf in iglob(join(SCHEMA_TESTDATA_DIRECTORY, sv.to_version(), f'valid-*.xml'))
    ))
    def test_schemaTestData(self, tf: str) -> None:
        with open(tf, 'r') as s:
            Bom.from_xml(s)
