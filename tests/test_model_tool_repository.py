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

from cyclonedx.model.component import Component
from cyclonedx.model.service import Service
from cyclonedx.model.tool import Tool, ToolRepository


class TestModelToolRepository(TestCase):

    def test_init(self) -> ToolRepository:
        c = Component(name='test-component')
        s = Service(name='test-service')
        t = Tool(name='test-tool')
        tr = ToolRepository(
            components=(c,),
            services=(s,),
            tools=(t,)
        )
        self.assertIs(c, tuple(tr.components)[0])
        self.assertIs(s, tuple(tr.services)[0])
        self.assertIs(t, tuple(tr.tools)[0])
        return tr

    def test_filled(self) -> None:
        tr = self.test_init()
        self.assertEqual(3, len(tr))
        self.assertTrue(tr)

    def test_empty(self) -> None:
        tr = ToolRepository()
        self.assertEqual(0, len(tr))
        self.assertFalse(tr)

    def test_unequal_different_type(self) -> None:
        tr = ToolRepository()
        self.assertFalse(tr == 'other')

    def test_equal_self(self) -> None:
        tr = ToolRepository()
        tr.tools.add(Tool(name='my-tool'))
        self.assertTrue(tr == tr)

    def test_unequal(self) -> None:
        tr1 = ToolRepository()
        tr1.components.add(Component(name='my-component'))
        tr1.services.add(Service(name='my-service'))
        tr1.tools.add(Tool(name='my-tool'))
        tr2 = ToolRepository()
        self.assertFalse(tr1 == tr2)

    def test_equal(self) -> None:
        c = Component(name='my-component')
        s = Service(name='my-service')
        t = Tool(name='my-tool')
        tr1 = ToolRepository()
        tr1.components.add(c)
        tr1.services.add(s)
        tr1.tools.add(t)
        tr2 = ToolRepository()
        tr2.components.add(c)
        tr2.services.add(s)
        tr2.tools.add(t)
        self.assertTrue(tr1 == tr2)
