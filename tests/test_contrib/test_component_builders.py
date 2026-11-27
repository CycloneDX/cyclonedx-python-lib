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

import os
from tempfile import TemporaryDirectory
from unittest import TestCase

from cyclonedx.contrib.component.builders import ComponentBuilder
from cyclonedx.model import HashAlgorithm
from cyclonedx.model.component import ComponentType


class TestComponentBuilderMakeForFile(TestCase):

    def test_missing_file_raises_file_not_found(self) -> None:
        with TemporaryDirectory() as tmp:
            missing = os.path.join(tmp, 'missing.whl')
            with self.assertRaises(FileNotFoundError):
                ComponentBuilder().make_for_file(missing, name='missing')

    def test_existing_file(self) -> None:
        with TemporaryDirectory() as tmp:
            path = os.path.join(tmp, 'file.txt')
            with open(path, 'wb') as f:
                f.write(b'abc')
            component = ComponentBuilder().make_for_file(path, name='file')
        self.assertIs(ComponentType.FILE, component.type)
        self.assertEqual('file', component.name)
        (hash_,) = component.hashes
        self.assertIs(HashAlgorithm.SHA_1, hash_.alg)
        self.assertEqual('a9993e364706816aba3e25717850c26c9cd0d89d', hash_.content)
