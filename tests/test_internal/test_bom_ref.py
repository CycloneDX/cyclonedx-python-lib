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

from unittest import TestCase

from cyclonedx._internal.bom_ref import bom_ref_from_str
from cyclonedx.model.bom_ref import BomRef


class TestInternalBomRefFromStr(TestCase):

    def test_bomref_io(self) -> None:
        i = BomRef()
        o = bom_ref_from_str(i)
        self.assertIs(i, o)

    def test_none_optional_is_none(self) -> None:
        o = bom_ref_from_str(None, optional=True)
        self.assertIsNone(o)

    def test_none_mandatory_is_something(self) -> None:
        o = bom_ref_from_str(None, optional=False)
        self.assertIsInstance(o, BomRef)
        self.assertIsNone(o.value)

    def test_nothing_optional_is_none(self) -> None:
        o = bom_ref_from_str('', optional=True)
        self.assertIsNone(o)

    def test_nothing_mandatory_is_something(self) -> None:
        o = bom_ref_from_str('', optional=False)
        self.assertIsInstance(o, BomRef)
        self.assertIsNone(o.value)

    def test_something_optional(self) -> None:
        o = bom_ref_from_str('foobar', optional=True)
        self.assertIsInstance(o, BomRef)
        self.assertEqual('foobar', o.value)

    def test_something_mandatory(self) -> None:
        o = bom_ref_from_str('foobar', optional=False)
        self.assertIsInstance(o, BomRef)
        self.assertEqual('foobar', o.value)
