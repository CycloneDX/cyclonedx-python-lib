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

from enum import Enum


class OutputFormat(str, Enum):
    JSON: str = 'Json'
    XML: str = 'Xml'


class SchemaVersion(str, Enum):
    V1_0: str = 'V1Dot0'
    V1_1: str = 'V1Dot1'
    V1_2: str = 'V1Dot2'
    V1_3: str = 'V1Dot3'
    V1_4: str = 'V1Dot4'

    def to_version(self) -> str:
        """
        Return as a version string - e.g. `1.4`

        Returns:
            `str` version
        """
        return f'{self.value[1]}.{self.value[5]}'
