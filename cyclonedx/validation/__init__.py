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

from abc import ABC, abstractmethod
from os.path import isfile
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from ..schema import SchemaVersion


class ValidationError:
    def __init__(self, data: Any) -> None:
        self.data = data


class _BaseValidator(ABC):

    @property
    @abstractmethod
    def _schema_file(self) -> str:
        ...

    def __init__(self, schema_version: 'SchemaVersion') -> None:
        self.schema_version = schema_version
        if not isfile(self._schema_file):
            raise NotImplementedError(f'not implemented for schema {schema_version}')

    @abstractmethod
    def validate_str(self, data: str) -> Optional[ValidationError]:
        ...
