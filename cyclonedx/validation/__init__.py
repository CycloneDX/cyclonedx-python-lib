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
from importlib import import_module
from typing import TYPE_CHECKING, Any, Literal, Optional, Protocol, Type, Union, overload

from ..schema import OutputFormat

if TYPE_CHECKING:
    from ..schema import SchemaVersion
    from .json import JsonValidator
    from .xml import XmlValidator


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
        """Validate a string

        :param data: the data string to validate
        :return: validation error
        :retval None: if `data` is valid
        :retval ValidationError:  if `data` is invalid
        """
        ...


class BaseValidator(ABC, Validator):
    """BaseValidator"""

    def __init__(self, schema_version: 'SchemaVersion') -> None:
        self.__schema_version = schema_version
        if not self._schema_file:
            raise ValueError(f'unsupported schema_version: {schema_version}')

    @property
    def schema_version(self) -> 'SchemaVersion':
        """get the schema version."""
        return self.__schema_version

    @property
    @abstractmethod
    def output_format(self) -> OutputFormat:
        """get the format."""
        ...

    @property
    @abstractmethod
    def _schema_file(self) -> Optional[str]:
        """get the schema file according to schema version."""
        ...


@overload
def get_instance(output_format: Literal[OutputFormat.JSON], schema_version: 'SchemaVersion') -> 'JsonValidator':
    ...


@overload
def get_instance(output_format: Literal[OutputFormat.XML], schema_version: 'SchemaVersion') -> 'XmlValidator':
    ...


@overload
def get_instance(output_format: OutputFormat, schema_version: 'SchemaVersion'
                 ) -> Union['JsonValidator', 'XmlValidator']:
    ...


def get_instance(output_format: OutputFormat, schema_version: 'SchemaVersion') -> BaseValidator:
    """get the default validator for a certain `OutputFormat`

    Raises error when no instance could be built.
    """
    # all exceptions are undocumented, as they are pure functional, and should be prevented by correct typing...
    if not isinstance(output_format, OutputFormat):
        raise TypeError(f"unexpected output_format: {output_format!r}")
    try:
        module = import_module(f'.{output_format.name.lower()}', __package__)
    except ImportError as error:
        raise ValueError(f'Unknown output_format: {output_format.name}') from error
    klass: Optional[Type[BaseValidator]] = getattr(module, f'{output_format.name.capitalize()}Validator', None)
    if klass is None:
        raise ValueError(f'Missing Validator for {output_format.name}')
    return klass(schema_version)
