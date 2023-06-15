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

from itertools import chain, product
from os.path import dirname, join
from typing import Callable, Type, Union
from unittest import TestCase

from ddt import ddt, idata, unpack

from cyclonedx.model.bom import Bom
from cyclonedx.output.json import Json, JsonV1Dot2, JsonV1Dot3, JsonV1Dot4
from cyclonedx.output.xml import Xml, XmlV1Dot0, XmlV1Dot1, XmlV1Dot2, XmlV1Dot3, XmlV1Dot4
from tests.data import (
    get_bom_for_issue_365_expression,
    get_bom_for_issue_365_expression_preferred,
    get_bom_for_issue_365_multiple_licenses,
)

_bom_getters = [
    get_bom_for_issue_365_multiple_licenses,
    get_bom_for_issue_365_expression,
    get_bom_for_issue_365_expression_preferred
]


@ddt
class Regression365(TestCase):
    """
    This is a regression test against https://github.com/CycloneDX/cyclonedx-python-lib/issues/365

    license list serialization must be like:
    - if list contains any expressions: serialize the first expression only
    - if list contains no expression: serialize all items
    """

    @idata(chain(
        product(_bom_getters, ['xml'], [XmlV1Dot4, XmlV1Dot3, XmlV1Dot2, XmlV1Dot1, XmlV1Dot0]),
        product(_bom_getters, ['json'], [JsonV1Dot4, JsonV1Dot3, JsonV1Dot2]),
    ))
    @unpack
    def test_serialize(self, bom_getter: Callable[[], Bom], target: str, schema_type: Union[Type[Json], Type[Xml]]) -> None:
        bom = bom_getter()
        serializer = schema_type(bom)
        serialized = serializer.output_as_string()

        expected_file = join(
            dirname(__file__),
            f'fixtures/{target}/{serializer.get_schema_version()}/regression365_{bom.components[0].name}.{target}')
        with open(expected_file, 'w') as expected_fh:
            expected_fh.write(serialized)
            self.assertEqual(expected_fh.read(), serialized)
