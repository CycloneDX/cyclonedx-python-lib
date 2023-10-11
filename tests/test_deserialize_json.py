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


from json import loads as json_loads
from os.path import join
from typing import Any, Callable
from unittest import TestCase
from unittest.mock import patch

from ddt import data, ddt, named_data

from cyclonedx.model.bom import Bom
from cyclonedx.model.license import DisjunctiveLicense, LicenseExpression, LicenseRepository
from cyclonedx.schema import OutputFormat, SchemaVersion
from tests import OWN_DATA_DIRECTORY, DeepCompareMixin, SnapshotMixin, mksname, uuid_generator
from tests._data.models import all_get_bom_funct_valid, all_get_bom_funct_with_incomplete_deps


@ddt
class TestDeserializeJson(TestCase, SnapshotMixin, DeepCompareMixin):

    @named_data(*all_get_bom_funct_valid)
    @patch('cyclonedx.model.ThisTool._version', 'TESTING')
    @patch('cyclonedx.model.bom_ref.uuid4', side_effect=uuid_generator(0, version=4))
    def test_prepared(self, get_bom: Callable[[], Bom], *_: Any, **__: Any) -> None:
        # only latest schema will have all data populated in serialized form
        snapshot_name = mksname(get_bom, SchemaVersion.V1_4, OutputFormat.JSON)
        expected = get_bom()
        json = json_loads(self.readSnapshot(snapshot_name))
        bom = Bom.from_json(json)
        self.assertBomDeepEqual(expected, bom,
                                fuzzy_deps=get_bom in all_get_bom_funct_with_incomplete_deps)

    @data(SchemaVersion.V1_4, SchemaVersion.V1_3, SchemaVersion.V1_2)
    def test_mixed_licenses_before15(self, sv: SchemaVersion) -> None:
        # before CDX 1.5 it was allowed to mix `expression` and `license`
        def test(ls: LicenseRepository) -> None:
            self.assertEqual(3, len(ls))
            expression: LicenseExpression = next((
                li for li in ls if isinstance(li, LicenseExpression)
            ), None)
            with_id: DisjunctiveLicense = next((
                li for li in ls if isinstance(li, DisjunctiveLicense) and li.id is not None
            ), None)
            with_name: DisjunctiveLicense = next((
                li for li in ls if isinstance(li, DisjunctiveLicense) and li.name is not None
            ), None)
            self.assertEqual('MIT OR Apache-2.0', expression.value)
            self.assertEqual('MIT', with_id.id)
            self.assertEqual('foo license', with_name.name)

        json_file = join(OWN_DATA_DIRECTORY, 'json', sv.to_version(), 'bom_with_mixed_licenses.json')
        with open(json_file) as f:
            json = json_loads(f.read())
        bom: Bom = Bom.from_json(json)
        test(bom.metadata.licenses)
        test(bom.metadata.component.licenses)
        test(list(bom.components)[0].licenses)
        test(list(bom.services)[0].licenses)
