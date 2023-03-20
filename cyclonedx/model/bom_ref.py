# encoding: utf-8

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

from typing import Any, Optional
from uuid import uuid4


class BomRef:
    """
    An identifier that can be used to reference objects elsewhere in the BOM.

    This copies a similar pattern used in the CycloneDX Python Library.

    .. note::
        See https://github.com/CycloneDX/cyclonedx-php-library/blob/master/docs/dev/decisions/BomDependencyDataModel.md
    """

    def __init__(self, value: Optional[str] = None) -> None:
        self.value = value or str(uuid4())

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        self._value = value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BomRef):
            return other.value == self.value
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, BomRef):
            return self.value < other.value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.value)

    def __repr__(self) -> str:
        return f'<BomRef {self.value}>'

    def __str__(self) -> str:
        return self.value
