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


from itertools import product
from typing import Tuple
from unittest import TestCase
from unittest.mock import Mock

from ddt import data, ddt, named_data, unpack

from cyclonedx.model.bom import Bom
from cyclonedx.model.bom_ref import BomRef
from cyclonedx.output import BomRefDiscriminator, make_outputter
from cyclonedx.schema import OutputFormat, SchemaVersion


@ddt
class TestTestGetInstance(TestCase):

    @named_data(*([f'{x[0].name} {x[1].name}', *x] for x in product(OutputFormat, SchemaVersion)))
    @unpack
    def test_as_expected(self, of: OutputFormat, sv: SchemaVersion) -> None:
        bom = Mock(spec=Bom)
        outputter = make_outputter(bom, of, sv)
        self.assertIs(outputter.get_bom(), bom)
        self.assertIs(outputter.output_format, of)
        self.assertIs(outputter.schema_version, sv)

    @data(
        *((of, 'foo', (ValueError, f"Unknown {of.name}/schema_version: 'foo'")) for of in OutputFormat),
        *(('foo', sv, (ValueError, "Unexpected output_format: 'foo'")) for sv in SchemaVersion),
    )
    @unpack
    def test_fails_on_wrong_args(self, of: OutputFormat, sv: SchemaVersion, raises_regex: Tuple) -> None:
        bom = Mock(spec=Bom)
        with self.assertRaisesRegex(*raises_regex):
            make_outputter(bom, of, sv)


class TestBomRefDiscriminator(TestCase):

    def test_discriminate_and_reset_with(self) -> None:
        bomref1 = BomRef('djdlkfjdslkf')
        bomref2 = BomRef('djdlkfjdslkf')
        self.assertEqual(bomref1.value, bomref2.value, 'blank')
        discr = BomRefDiscriminator([bomref1, bomref2])
        self.assertEqual(bomref1.value, bomref2.value, 'init')
        discr.discriminate()
        self.assertNotEqual(bomref1.value, bomref2.value, 'should be discriminated')
        discr.reset()
        self.assertEqual('djdlkfjdslkf', bomref1.value)
        self.assertEqual('djdlkfjdslkf', bomref2.value)

    def test_discriminate_and_reset_manually(self) -> None:
        bomref1 = BomRef('djdlkfjdslkf')
        bomref2 = BomRef('djdlkfjdslkf')
        self.assertEqual(bomref1.value, bomref2.value, 'blank')
        discr = BomRefDiscriminator([bomref1, bomref2])
        self.assertEqual(bomref1.value, bomref2.value, 'init')
        with discr:
            self.assertNotEqual(bomref1.value, bomref2.value, 'should be discriminated')
        discr.reset()
        self.assertEqual('djdlkfjdslkf', bomref1.value)
        self.assertEqual('djdlkfjdslkf', bomref2.value)
