# encoding: utf-8

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

import os
from unittest import TestCase

from cyclonedx.parser.requirements import RequirementsParser


class TestRequirementsParser(TestCase):

    def test_simple(self):
        with open(os.path.join(os.path.dirname(__file__), 'fixtures/requirements-simple.txt')) as r:
            parser = RequirementsParser(
                requirements_content=r.read()
            )
            r.close()
        self.assertTrue(1, parser.component_count())

    def test_example_1(self):
        with open(os.path.join(os.path.dirname(__file__), 'fixtures/requirements-example-1.txt')) as r:
            parser = RequirementsParser(
                requirements_content=r.read()
            )
            r.close()
        self.assertTrue(3, parser.component_count())
