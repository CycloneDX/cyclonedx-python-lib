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

from os.path import isfile
from typing import Generator
from unittest import TestCase

from ddt import ddt, idata

from cyclonedx.schema import _res


def _dp_files() -> Generator:
    for bom in (_res.BOM_XML, _res.BOM_JSON, _res.BOM_JSON):
        for file in bom.values():
            if file is not None:
                yield file
    yield _res.SPDX_JSON
    yield _res.SPDX_XML
    yield _res.JSF


@ddt
class SchemaResTest(TestCase):

    @idata(_dp_files())
    def test_file_exists(self, file: str) -> None:
        self.assertTrue(isfile(file), file)
