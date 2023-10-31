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


from unittest import TestCase

from cyclonedx.model.bom_ref import BomRef
from cyclonedx.output import BomRefDiscriminator


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
