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

from datetime import datetime, timezone
from itertools import chain, product
from os.path import dirname, join
from typing import Type, Union
from unittest import TestCase
from uuid import UUID

from ddt import ddt, idata, unpack

from cyclonedx.model import AttachedText, Encoding, License, LicenseChoice, XsUri
from cyclonedx.model.bom import Bom, Component
from cyclonedx.output.json import Json, JsonV1Dot2, JsonV1Dot3, JsonV1Dot4
from cyclonedx.output.xml import Xml, XmlV1Dot0, XmlV1Dot1, XmlV1Dot2, XmlV1Dot3, XmlV1Dot4

_bom_multiple_licenses = Bom(serial_number=UUID(hex='92f71d34625a449798913333c56a7af1'))
_bom_multiple_licenses.metadata.timestamp = datetime(2022, 6, 15, 13, 5, 12, 0, timezone.utc)
_bom_multiple_licenses.metadata.tools = []
_bom_multiple_licenses.components.add(Component(
    name='multiple-licenses',
    bom_ref='testing',
    licenses=[
        LicenseChoice(
            license=License(
                id='Apache-2.0',
                text=AttachedText(
                    content='VGVzdCBjb250ZW50IC0gdGhpcyBpcyBub3QgdGhlIEFwYWNoZSAyLjAgbGljZW5zZSE=',
                    encoding=Encoding.BASE_64
                ),
                url=XsUri('https://www.apache.org/licenses/LICENSE-2.0.txt')
            )
        ),
        LicenseChoice(license=License(name='OSI_APACHE'))
    ]))

_bom_expression_preferred = Bom(serial_number=UUID(hex='66f6f3d40d244db3b69cbd547be9b0d3'))
_bom_expression_preferred.metadata.timestamp = datetime(2022, 6, 15, 13, 9, 38, 0, timezone.utc)
_bom_multiple_licenses.metadata.tools = []
_bom_expression_preferred.components.add(Component(
    name='expression-preferred',
    bom_ref='testing',
    licenses=[
        LicenseChoice(
            license=License(
                id='Apache-2.0',
                text=AttachedText(
                    content='VGVzdCBjb250ZW50IC0gdGhpcyBpcyBub3QgdGhlIEFwYWNoZSAyLjAgbGljZW5zZSE=',
                    encoding=Encoding.BASE_64
                ),
                url=XsUri('https://www.apache.org/licenses/LICENSE-2.0.txt')
            )
        ),
        LicenseChoice(expression='(Apache-2.0 OR MIT)'),
        LicenseChoice(license=License(name='OSI_APACHE'))
    ]))


@ddt
class Regression365(TestCase):
    """
    This is a regression test against https://github.com/CycloneDX/cyclonedx-python-lib/issues/365

    license list serialization must be like:
    - if list contains any expressions: serialize the first expression only
    - if list contains no expression: serialize all items
    """

    @idata(chain(
        product(
            [_bom_multiple_licenses, _bom_expression_preferred],
            ['xml'],
            [XmlV1Dot4, XmlV1Dot3, XmlV1Dot2, XmlV1Dot1, XmlV1Dot0]
        ),
        product(
            [_bom_multiple_licenses, _bom_expression_preferred],
            ['json'],
            [JsonV1Dot4, JsonV1Dot3, JsonV1Dot2]
        ),
    ))
    @unpack
    def test_serialize(self, bom: Bom, target: str, schema_type: Union[Type[Json], Type[Xml]]) -> None:
        serializer = schema_type(bom)
        serialized = serializer.output_as_string()

        expected_file = join(
            dirname(__file__),
            f'fixtures/{target}/{serializer.get_schema_version()}/regression365_{bom.components[0].name}.{target}')
        with open(expected_file, 'r') as expected_fh:
            self.assertEqual(expected_fh.read(), serialized)
