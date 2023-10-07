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

from os import getenv, path
from os.path import join
from typing import Any, Generator, List, Optional, TypeVar, Union
from unittest import TestCase
from uuid import UUID

from sortedcontainers import SortedSet

_T = TypeVar('_T')

_TESTDATA_DIRECTORY = path.join(path.dirname(__file__), '_data')

SCHEMA_TESTDATA_DIRECTORY = path.join(_TESTDATA_DIRECTORY, 'schemaTestData')
OWN_DATA_DIRECTORY = path.join(_TESTDATA_DIRECTORY, 'own')
SNAPSHOTS_DIRECTORY = path.join(_TESTDATA_DIRECTORY, 'snapshots')

RECREATE_SNAPSHOTS = '1' == getenv('CDX_TEST_RECREATE_SNAPSHOTS')
if RECREATE_SNAPSHOTS:
    print('!!! WILL RECREATE ALL SNAPSHOTS !!!')


class SnapshotCompareMixin:

    @staticmethod
    def getSnapshotFile(snapshot_name: str) -> str:
        return join(SNAPSHOTS_DIRECTORY, f'{snapshot_name}.bin')

    @classmethod
    def writeSnapshot(cls, snapshot_name: str, data: str) -> None:
        with open(cls.getSnapshotFile(snapshot_name), 'w') as s:
            s.write(data)

    @classmethod
    def readSnapshot(cls, snapshot_name: str) -> str:
        with open(cls.getSnapshotFile(snapshot_name), 'r') as s:
            return s.read()

    def assertEqualSnapshot(self: Union[TestCase, 'SnapshotCompareMixin'], actual: str, snapshot_name: str) -> None:
        if RECREATE_SNAPSHOTS:
            self.writeSnapshot(snapshot_name, actual)
        _omd = self.maxDiff
        _omd = self.maxDiff
        self.maxDiff = None
        try:
            self.assertEqual(actual, self.readSnapshot(snapshot_name))
        finally:
            self.maxDiff = _omd


class DeepCompareMixin:
    def assertDeepEqual(self: Union[TestCase, 'DeepCompareMixin'], first: Any, second: Any,
                        msg: Optional[str] = None) -> None:
        """costly compare, but very verbose"""
        _omd = self.maxDiff
        self.maxDiff = None
        try:
            self.maxDiff = None
            dd1 = self.__deepDict(first)
            dd2 = self.__deepDict(second)
            self.assertDictEqual(dd1, dd2, msg)
        finally:
            self.maxDiff = _omd

    def __deepDict(self, o: Any) -> Any:
        if isinstance(o, (list, tuple)):
            return tuple(self.__deepDict(i) for i in o)
        if isinstance(o, dict):
            return {k: self.__deepDict(v) for k, v in o}
        if isinstance(o, (set, SortedSet)):
            return tuple(sorted((self.__deepDict(i) for i in o), key=repr))
        if hasattr(o, '__dict__'):
            return {k: self.__deepDict(v) for k, v in vars(o).items() if not (k.startswith('__') and k.endswith('__'))}
        return o


def reorder(items: List[_T], indexes: List[int]) -> List[_T]:
    """
    Return list of items in the order indicated by indexes.
    """
    reordered_items = []
    for i in range(len(items)):
        reordered_items.append(items[indexes[i]])
    return reordered_items


def uuid_generator(offset: int = 0, version: int = 4) -> Generator[UUID, None, None]:
    v = offset
    while True:
        v += 1
        yield UUID(int=v, version=version)
