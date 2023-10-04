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

from enum import Enum, auto, unique


@unique
class OutputFormat(Enum):
    """Output formats.

    Do not rely on the actual/literal values, just use enum cases.
    """
    JSON = auto()
    XML = auto()


@unique
class SchemaVersion(Enum):
    """
    Schema version.

    Cases are hashable.
    Cases are comparable(!=,>=,>,==,<,<=)

    Do not rely on the actual/literal values, just use enum cases.
    """
    V1_4 = (1, 4)
    V1_3 = (1, 3)
    V1_2 = (1, 2)
    V1_1 = (1, 1)
    V1_0 = (1, 0)

    @classmethod
    def from_version(cls, version: str) -> 'SchemaVersion':
        """Return instance from  a version string - e.g. `1.4`"""
        return cls(tuple(map(int, version.split('.')))[:2])

    def to_version(self) -> str:
        """Return as a version string - e.g. `1.4`"""
        return '.'.join(map(str, self.value))

    def __ne__(self, other: object) -> bool:
        return self.value != other.value \
            if isinstance(other, self.__class__) \
            else NotImplemented  # type:ignore[return-value]

    def __lt__(self, other: object) -> bool:
        return self.value < other.value \
            if isinstance(other, self.__class__) \
            else NotImplemented  # type:ignore[return-value]

    def __le__(self, other: object) -> bool:
        return self.value <= other.value \
            if isinstance(other, self.__class__) \
            else NotImplemented  # type:ignore[return-value]

    def __eq__(self, other: object) -> bool:
        return self.value == other.value \
            if isinstance(other, self.__class__) \
            else NotImplemented  # type:ignore[return-value]

    def __ge__(self, other: object) -> bool:
        return self.value >= other.value \
            if isinstance(other, self.__class__) \
            else NotImplemented  # type:ignore[return-value]

    def __gt__(self, other: object) -> bool:
        return self.value > other.value \
            if isinstance(other, self.__class__) \
            else NotImplemented  # type:ignore[return-value]

    def __hash__(self) -> int:
        return hash(self.name)
