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

"""
Set of classes and methods which allow for quick creation of a Bom instance from your environment or Python project.

Use a Parser instead of programmatically creating a Bom as a developer.
"""

from abc import ABC
from typing import List

from ..model.component import Component


class ParserWarning:
    _item: str
    _warning: str

    def __init__(self, item: str, warning: str) -> None:
        self._item = item
        self._warning = warning

    def get_item(self) -> str:
        return self._item

    def get_warning_message(self) -> str:
        return self._warning

    def __repr__(self) -> str:
        return '<ParserWarning item=\'{}\'>'.format(self._item)


class BaseParser(ABC):
    _components: List[Component] = []
    _warnings: List[ParserWarning] = []

    def __init__(self) -> None:
        """

        :rtype: object
        """
        self._components.clear()
        self._warnings.clear()

    def component_count(self) -> int:
        return len(self._components)

    def get_components(self) -> List[Component]:
        return self._components

    def get_warnings(self) -> List[ParserWarning]:
        return self._warnings

    def has_warnings(self) -> bool:
        return len(self._warnings) > 0
