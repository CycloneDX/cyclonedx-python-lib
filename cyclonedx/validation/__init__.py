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
from typing import TYPE_CHECKING, Any, Optional, Protocol, cast

if TYPE_CHECKING:
    from ..schema import OutputFormat, SchemaVersion


class ValidationError:
    """Validation failed with this specific error.

    Use :attr:`~data` to access the content.
    """

    data: Any

    def __init__(self, data: Any) -> None:
        self.data = data

    def __repr__(self) -> str:
        return repr(self.data)

    def __str__(self) -> str:
        return str(self.data)


class Validator(Protocol):
    """Validator protocol"""

    def validate_str(self, data: str) -> Optional[ValidationError]:
        """Validate a string"""
        ...


class BaseValidator(ABC):
    """BaseValidator"""

    def __init__(self, schema_version: 'SchemaVersion') -> None:
        self.__schema_version = schema_version
        if not self._schema_file:
            raise ValueError(f'unsupported schema: {schema_version}')

    @property
    def schema_version(self) -> 'SchemaVersion':
        """get the schema version."""
        return self.__schema_version

    @property
    @abstractmethod
    def _schema_file(self) -> Optional[str]:
        """get the schema file according to schema version."""
        ...


def get_instance(format: 'OutputFormat',
                 schema_version: 'SchemaVersion') -> Validator:
    """
    Helper method to quickly get the correct validation class/validator.

    Pass in your BOM and optionally an output format and schema version.

    :param format: OutputFormat
    :param schema_version: SchemaVersion
    :return:
    """
    import importlib

    try:
        module = importlib.import_module(f"cyclonedx.validation.{format.value.lower()}")
        output_klass = getattr(module, f"{format.value}{schema_version.value}")
    except (ImportError, AttributeError) as e:
        raise ValueError(f"Unknown format {format.value.lower()!r}: {e}") from None

    return cast(Validator, output_klass(schema_version=schema_version))
