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


from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any, Literal, Optional, Protocol, Union, overload

from ..schema import OutputFormat

if TYPE_CHECKING:  # pragma: no cover
    from ..schema import SchemaVersion
    from .json import JsonValidator
    from .xml import XmlValidator


def squeeze(text: str, size: int, replacement: str = ' ... ') -> str:
    """Replaces the middle of ``text`` with ``replacement``.

    :param size: the length of the output, -1 to make no squeezing.
    :return: potentially shorter text
    :retval: ``text`` if ``size`` is -1 (for easy pass-through)
    :retval: ``text`` if it is shorter than ``size``
    :retval: ``text`` with the middle of it replaced with ``replacement``,
             if ``text`` is longer, than ``size``

    Raises error if ``replacement`` is longer than ``size``, and replacement
    would happen.
    """
    if size == -1:
        return text

    if size < len(replacement):
        raise ValueError(f'squeeze: {size = } < {len(replacement) = }')

    if len(text) <= size:
        return text

    left_size = (size - len(replacement)) // 2
    right_size = size - len(replacement) - left_size
    right_offset = len(text) - right_size

    return f'{text[:left_size]}{replacement}{text[right_offset:]}'


class ValidationError:
    """Validation failed with this specific error.

    You can use :attr:`~data` to access the raw error object, but prefer
    other properties and functions, if possible.
    """

    data: Any
    """Raw error data from one of the validation libraries."""

    @property
    def message(self) -> str:
        """The error message."""
        return str(getattr(self.data, 'message', self))

    @property
    def path(self) -> str:
        """Path to the location of the problem in the document.

        An XPath/JSONPath string.
        """
        # only subclasses know how to extract this info
        return str(getattr(self.data, 'path', ''))

    def get_squeezed_message(self, *, context_limit: int = -1, max_size: int = -1, replacement: str = ' ... ') -> str:
        """Extracts, and sanitizes the error message.

        Messages can be quite big from underlying libraries, as they sometimes
        add context to the error message: both the input or the rule can be big.

        This can be amended both in a generic and library specific ways.

        :param max_size: squeeze message to this size.
        :param context_limit: limit of tolerated context length.
        :param replacement: to mark place of dropped text bit[s]

        With the defaults, no squeezing happens.
        """
        # subclasses may know how to do it better
        return squeeze(self.message, max_size, replacement)

    def __init__(self, data: Any) -> None:
        self.data = data

    def __repr__(self) -> str:
        return repr(self.data)

    def __str__(self) -> str:
        return str(self.data)


class SchemabasedValidator(Protocol):
    """Schema-based Validator protocol"""

    @overload
    def validate_str(self, data: str, *, all_errors: Literal[False] = ...) -> Optional[ValidationError]:
        """Validate a string

        :param data: the data string to validate
        :param all_errors: whether to return all errors or only the last error - if any
        :return: validation error
        :retval None: if ``data`` is valid
        :retval ValidationError:  if ``data`` is invalid
        """
        ...  # pragma: no cover

    @overload
    def validate_str(self, data: str, *, all_errors: Literal[True]) -> Optional[Iterable[ValidationError]]:
        """Validate a string

        :param data: the data string to validate
        :param all_errors: whether to return all errors or only the last error - if any
        :return: validation error
        :retval None: if ``data`` is valid
        :retval Iterable[ValidationError]:  if ``data`` is invalid
        """
        ...   # pragma: no cover

    def validate_str(
        self, data: str, *,
        all_errors: bool = False
    ) -> Union[None, ValidationError, Iterable[ValidationError]]:
        """Validate a string

        :param data: the data string to validate
        :param all_errors: whether to return all errors or only the last error - if any
        :return: validation error
        :retval None: if ``data`` is valid
        :retval ValidationError:  if ``data`` is invalid and ``all_errors`` is ``False``
        :retval Iterable[ValidationError]:  if ``data`` is invalid and ``all_errors`` is ``True``
        """
        ...  # pragma: no cover


class BaseSchemabasedValidator(ABC, SchemabasedValidator):
    """Base Schema-based Validator"""

    def __init__(self, schema_version: 'SchemaVersion') -> None:
        self.__schema_version = schema_version
        if not self._schema_file:
            raise ValueError(f'Unsupported schema_version: {schema_version!r}')

    @property
    def schema_version(self) -> 'SchemaVersion':
        """Get the schema version."""
        return self.__schema_version

    @property
    @abstractmethod
    def output_format(self) -> OutputFormat:
        """Get the format."""
        ...  # pragma: no cover

    @property
    @abstractmethod
    def _schema_file(self) -> Optional[str]:
        """Get the schema file according to schema version."""
        ...  # pragma: no cover


@overload
def make_schemabased_validator(output_format: Literal[OutputFormat.JSON], schema_version: 'SchemaVersion'
                               ) -> 'JsonValidator':
    ...  # pragma: no cover


@overload
def make_schemabased_validator(output_format: Literal[OutputFormat.XML], schema_version: 'SchemaVersion'
                               ) -> 'XmlValidator':
    ...  # pragma: no cover


@overload
def make_schemabased_validator(output_format: OutputFormat, schema_version: 'SchemaVersion'
                               ) -> Union['JsonValidator', 'XmlValidator']:
    ...  # pragma: no cover


def make_schemabased_validator(output_format: OutputFormat, schema_version: 'SchemaVersion'
                               ) -> 'BaseSchemabasedValidator':
    """Get the default Schema-based Validator for a certain :class:`OutputFormat`.

    Raises error when no instance could be made.
    """
    if TYPE_CHECKING:  # pragma: no cover
        Validator: type[BaseSchemabasedValidator]  # noqa:N806
    if OutputFormat.JSON is output_format:
        from .json import JsonValidator as Validator
    elif OutputFormat.XML is output_format:
        from .xml import XmlValidator as Validator
    else:
        raise ValueError(f'Unexpected output_format: {output_format!r}')
    return Validator(schema_version)
