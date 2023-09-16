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
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from ..schema import SchemaVersion


class MissingOptionalDependencyException(BaseException):
    pass


class ValidationError:
    def __init__(self, data: Any) -> None:
        self.data = data

    def __repr__(self) -> str:
        return repr(self.data)

    def __str__(self) -> str:
        return str(self.data)


class _BaseValidator(ABC):

    def __init__(self, schema_version: 'SchemaVersion') -> None:
        self.__schema_version = schema_version
        if not self._schema_file:
            raise NotImplementedError(f'not implemented for schema {schema_version}')

    @property
    @abstractmethod
    def _schema_file(self) -> Optional[str]:
        ...

    @property
    def schema_version(self) -> 'SchemaVersion':
        return self.__schema_version

    @abstractmethod
    def validate_str(self, data: str) -> Optional[ValidationError]:
        ...
